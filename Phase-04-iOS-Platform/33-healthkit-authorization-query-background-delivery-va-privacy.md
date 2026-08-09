---
title: "HealthKit: authorization, query, background delivery và privacy"
phase: "iOS Platform"
difficulty: 5
importance: 3
interview_frequency: 3
status: complete
last_verified: 2026-08-09
swift_baseline: "Swift 6.3 toolchain; Swift 6 language mode"
levels:
  - L4
  - L5
prerequisites:
  - "CoreLocation: permission, accuracy, background và energy"
  - "Offline-first synchronization"
used_later:
  - "App Store release engineering: signing, privacy, review và rollback"
competencies:
  - "iOS Platform"
  - "Privacy"
  - "Persistence"
  - "Production"
tags:
  - "healthkit"
  - "health-data"
  - "authorization"
  - "background-delivery"
---

# HealthKit: authorization, query, background delivery và privacy

> **Version scope**
>
> HealthKit behavior khác theo platform, data type và authorization window. Chapter không thay thế medical/regulatory review. Chỉ enable capability/data types có product purpose hợp lệ và kiểm tra App Review policy hiện hành. Xác minh 2026-08-09.

## Story / Problem

Ứng dụng fitness hỏi toàn bộ quyền HealthKit ngay first launch, rồi hiển thị “Không có dữ liệu” khi user từ chối read access. Một background observer gọi completion trước khi lưu anchor, khiến lần sau mất sample. Team đang coi HealthKit như database thông thường, trong khi framework cố tình giới hạn khả năng suy ra trạng thái quyền đọc và dữ liệu có thể được sửa/xóa từ app khác.

```text
Fine-grained authorization → query/anchor → local projection
                                  ↑              ↓
                   observer/background event → checkpoint
```

## Objectives

Sau chapter này, bạn có thể:

- xin quyền đọc/ghi tối thiểu theo value moment và data type;
- hiểu giới hạn privacy: app không luôn phân biệt denied read với không có data;
- chọn sample, statistics, anchored và observer query đúng mục đích;
- thiết kế background delivery có durable anchor và completion ordering;
- xử lý duplicate, deletion, multiple sources, units và partial history;
- thiết kế storage/log/export không làm rò rỉ health data.

## Prerequisites

- [CoreLocation permission](22-corelocation-permission-accuracy-background-va-energy.md) cho progressive permission.
- [Offline-first synchronization](../Phase-07-Persistence/12-offline-first-synchronization.md) cho cursor/anchor và reconciliation.
- [Structured privacy-aware logging](../Phase-09-Production/01-structured-privacy-aware-logging.md).

## Used Later

- [App Store release engineering](../Phase-09-Production/21-app-store-release-engineering-signing-privacy-review-va-rollback.md) audit HealthKit capability, purpose string và privacy disclosure.
- [BackgroundTasks](../Phase-09-Production/22-bgtaskscheduler-background-urlsession-energy-va-debugging.md) phân biệt HealthKit wake với generic scheduler.

## Mental Model

```text
HealthKit store = user-controlled multi-source repository
Authorization   = per type + read/write direction + có thể thay đổi
Anchor          = durable cursor, không phải timestamp tự chế
Local cache     = projection có thể rebuild/reconcile
```

HealthKit bảo vệ privacy bằng cách không cho app suy ra chính xác một số trạng thái read denial. Vì thế “query trả rỗng” không chứng minh user không có dữ liệu. User/app khác có thể thêm, sửa hoặc xóa sample ngoài lifecycle app của bạn.

## What?

App thêm HealthKit capability và purpose strings cho read/write. Kiểm tra availability, tạo chính xác `HKObjectType` cần dùng và request authorization gần feature. Quyền read và share khác nhau; `authorizationStatus(for:)` hữu ích cho write status nhưng không được dùng để suy đoán read permission đầy đủ.

Query snapshot trả dữ liệu hiện tại. Statistics query aggregate số liệu. Anchored query lấy changes kể từ anchor gồm additions/deletions. Observer query báo có thay đổi và có thể đăng ký background delivery; khi wake, app chạy anchored query, commit data + anchor durably rồi mới gọi completion.

## Why?

Fetch toàn history mỗi wake tốn pin và có thể duplicate. Dùng timestamp làm cursor bỏ sót deletion hoặc sample backdated. Aggregate thủ công có thể double-count nhiều source/device. Upload health data raw lên backend mà không có consent/retention policy mở rộng blast radius và có thể vi phạm expectation/policy.

## How?

```swift
import HealthKit

actor HealthAuthorizationService {
    private let store = HKHealthStore()

    func requestStepAccess() async throws {
        guard HKHealthStore.isHealthDataAvailable() else { return }
        let steps = HKQuantityType(.stepCount)
        try await store.requestAuthorization(toShare: [], read: [steps])
    }
}
```

Không diễn giải `requestAuthorization` success là user bật mọi toggle; nó cho biết flow request hoàn tất. UI nên tiếp tục hoạt động với trạng thái limited/empty và hướng dẫn Settings/Health app khi feature thực sự cần.

### Query selection

- sample query: danh sách có predicate/sort/limit;
- statistics/statistics collection: sum/average theo interval, ưu tiên system aggregation;
- anchored query: incremental additions/deletions với persisted anchor;
- observer query: invalidation signal, sau đó fetch changes.

Unit conversion dùng `HKUnit` tương thích với quantity type; domain nên giữ canonical unit/value và source metadata khi cần audit. Deduplicate bằng HealthKit object UUID/anchor semantics, không bằng timestamp-value tuple dễ collision.

### Background delivery ordering

Đăng ký observer sớm theo lifecycle framework yêu cầu. Update handler phải khởi động bounded reconciliation. Completion chỉ gọi sau khi xử lý cần thiết hoặc durable queue/checkpoint đã ghi; nếu gọi sớm rồi process chết, event có thể mất khỏi workflow của app. Nếu work dài cần upload, persist local changes trước và giao upload cho mechanism phù hợp; không giữ HealthKit callback vô hạn.

### Privacy architecture

Xin type tối thiểu, mô tả rõ user benefit và không chặn toàn app nếu feature phụ. Health data không vào generic analytics/crash breadcrumb. Encrypt data at rest/in transit theo threat model, tách access role, retention/deletion/export, account logout và backup policy. Không dùng absence của sample để suy ra bệnh/trạng thái. Medical interpretation cần domain expert và disclaimer/regulatory review.

## Production Case

### Context

App tổng hợp bước chân mỗi ngày và đồng bộ opt-in lên backend.

### Symptom

Một số ngày có số bước gấp đôi; background update đôi khi mất sau app termination.

### Investigation

Team kiểm tra source/device, sample UUID, anchor version và completion timestamp. Code cộng mọi sample từ Apple Watch và iPhone thay vì dùng statistics semantics; completion chạy trước transaction lưu samples + anchor.

### Root Cause

Aggregation sai với overlapping sources và checkpoint không atomic.

### Fix

Dùng HealthKit statistics phù hợp, lưu result/anchor trong một durable transaction, completion sau commit; upload đọc từ outbox idempotent.

### Prevention

Test multiple source, deletion, backdated sample, limited history, revoked permission, kill giữa fetch/commit và duplicate background callback.

## Interview Questions

### Foundation

**Query rỗng có nghĩa user từ chối read không?** Không chắc; privacy model cố tình hạn chế phân biệt denied với no data trong nhiều trường hợp.

### Middle

**Observer query và anchored query phối hợp thế nào?** Observer báo thay đổi; anchored query lấy additions/deletions kể từ durable anchor.

### Senior

**Thiết kế HealthKit sync production?** Progressive authorization, type/unit semantics, observer + atomic anchor, source/deletion handling, offline outbox, privacy/retention, device tests và observability không chứa health data.

## Exercises

### Easy

Lập permission matrix read/write cho ba data type và value moment.

### Medium

Thiết kế anchored-sync store có atomic data + anchor commit.

### Hard

Viết threat model và retention/export/delete workflow cho backend nhận health aggregates.

### Debugging Lab

Thêm/xóa sample từ nguồn khác, kill app giữa fetch/commit, chạy lại và chứng minh không mất/đúp dữ liệu.

## Cheat Sheet

```text
authorization     → fine-grained, mutable, privacy-limited visibility
empty read        → không chứng minh denied/no-data
observer          → invalidation signal
anchored query    → incremental additions + deletions
anchor            → persist atomically cùng projection
completion        → sau durable acceptance
health data       → minimize access/log/retention
```

## Chapter Summary

1. HealthKit là user-controlled, multi-source và privacy-preserving store.
2. Quyền phải xin tối thiểu; read denial không luôn quan sát được.
3. Observer + anchored query tạo incremental sync đúng hơn timestamp.
4. Data và anchor phải commit atomic trước completion.
5. Privacy, retention và medical interpretation là architecture constraint.

## Related Chapters

- [Offline-first synchronization](../Phase-07-Persistence/12-offline-first-synchronization.md)
- [Account data isolation](../Phase-07-Persistence/14-logout-login-va-data-isolation-giua-account.md)
- [Privacy-aware logging](../Phase-09-Production/01-structured-privacy-aware-logging.md)

## References

- [Apple — HealthKit](https://developer.apple.com/documentation/healthkit)
- [Apple — Authorizing access to health data](https://developer.apple.com/documentation/healthkit/authorizing-access-to-health-data)
- [Apple — Reading data from HealthKit](https://developer.apple.com/documentation/healthkit/reading-data-from-healthkit)
- [Apple — Executing Observer Queries](https://developer.apple.com/documentation/healthkit/executing-observer-queries)
