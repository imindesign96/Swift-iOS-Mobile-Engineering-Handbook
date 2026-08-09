---
title: "CloudKit: sync, account, conflict và offline boundary"
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
  - "Offline-first synchronization"
  - "Conflict detection và resolution"
used_later:
  - "BackgroundTasks và background URLSession"
competencies:
  - "iOS Platform"
  - "Persistence"
  - "System Design"
  - "Production"
tags:
  - "cloudkit"
  - "cksyncengine"
  - "icloud"
  - "conflict-resolution"
---

# CloudKit: sync, account, conflict và offline boundary

> **Version scope**
>
> Bao phủ lựa chọn `NSPersistentCloudKitContainer`, `CKSyncEngine` và CloudKit base APIs. Capability/schema/environment khác theo app; test development và production container carefully vì schema deployment có tính vận hành. Xác minh 2026-08-09.

## Story / Problem

User sửa cùng ghi chú trên iPhone và iPad offline. Khi online, một bản biến mất. Sau khi đổi iCloud account, dữ liệu của account cũ còn trên màn hình. Team đã thêm CloudKit rồi giả định “iCloud tự sync”, nhưng chưa chọn local source of truth, conflict policy, account isolation, tombstone và progress semantics.

```text
Local mutation → durable local store/outbox → CloudKit sync → remote changes
       ↑                                                   ↓
       └──────────── merge/conflict/account policy ────────┘
```

## Objectives

Sau chapter này, bạn có thể:

- chọn CloudKit integration level theo control/complexity;
- phân biệt public, private, shared database và account requirement;
- thiết kế local-first projection, pending changes, tombstone và conflict policy;
- dùng CKSyncEngine state/event theo durable lifecycle;
- xử lý iCloud sign-in/out/switch mà không trộn dữ liệu;
- debug schema, entitlement, throttling, partial failure và “sync eventually” UX.

## Prerequisites

- [Offline-first synchronization](../Phase-07-Persistence/12-offline-first-synchronization.md).
- [Conflict detection và resolution](../Phase-07-Persistence/13-conflict-detection-va-resolution.md).
- [Account data isolation](../Phase-07-Persistence/14-logout-login-va-data-isolation-giua-account.md).

## Used Later

- [BackgroundTasks](../Phase-09-Production/22-bgtaskscheduler-background-urlsession-energy-va-debugging.md) phân biệt system-managed sync và app-scheduled maintenance.
- [Mobile System Design interview](../Phase-11-Interview/14-mobile-system-design-interview.md).

## Mental Model

```text
CloudKit = remote record transfer/service, không thay domain model
Local DB = responsive source of truth cho UI/offline
Sync     = eventually consistent state machine
Engine state/change tokens = durable progress, không disposable cache
```

System conditions quyết định lúc periodic sync chạy. “Save local thành công” không có nghĩa mọi device đã thấy. UI cần biểu diễn local/pending/synced/conflicted khi product yêu cầu, không spinner vô hạn hứa realtime.

## What?

Ba lựa chọn phổ biến:

- `NSPersistentCloudKitContainer`: managed Core Data mirroring, ít control hơn nhưng nhanh cho model phù hợp;
- `CKSyncEngine`: giữ local model/control, engine schedule fetch/send và phát event; app cung cấp record changes/conflict policy;
- `CKDatabase`/operations: control thấp tầng lớn nhất và cũng nhiều trách nhiệm nhất về tokens, subscriptions, batching, retry, conflicts.

Private database cần iCloud account và dữ liệu thuộc user; shared database hỗ trợ sharing; public database có accessibility/security/quota khác. Chọn dựa ownership, sharing, web/backend need, migration, observability và conflict semantics—not vì “Apple native”.

## Why?

Network, battery, sign-in và throttle làm cadence không xác định. Record save có partial failure. Cùng record có thể đổi ở nhiều device; deletion cần tombstone/change event. Retry mù có thể ghi đè server record mới. Nếu cache không partition theo account, sign-out làm lộ dữ liệu user trước.

## How?

```swift
import CloudKit

enum SyncStatus: Equatable {
    case localOnly
    case pending
    case synced(Date)
    case conflicted
    case accountUnavailable
}

struct SyncedNote: Identifiable, Equatable {
    let id: UUID
    var text: String
    var modifiedAt: Date
    var status: SyncStatus
}
```

UI mutate local record trong transaction và thêm pending change/outbox. Sync layer chuyển domain record sang `CKRecord` tại boundary. Record name ổn định theo domain ID; system fields/change tag phải được giữ nếu strategy yêu cầu optimistic concurrency.

### CKSyncEngine contract

Khởi tạo engine sớm cho private/shared database, persist opaque engine state khi nhận state-update event, add pending database/record-zone changes khi local mutation commit và cung cấp batch đúng scope. Engine xử lý một số transient errors/retry, nhưng app vẫn xử lý domain conflict như `serverRecordChanged`, deletion, account change và invalid data.

Đừng đánh dấu local item synced chỉ vì đưa vào pending list. Chuyển status sau sent-change success tương ứng; partial failures map theo record. Khi fetch remote, áp change idempotently vào local DB rồi cập nhật UI qua observation.

### Conflict policy

Last-write-wins chỉ chấp nhận khi clock/semantic loss đã được đánh giá. Có thể merge field-level, append-only log, CRDT-like rule hoặc surface conflict cho user. Business invariant như unique ownership/quota có thể cần authoritative backend thay vì CloudKit client merge.

### Account lifecycle

Theo dõi account change. Sign-out/switch phải dừng hoặc generation-gate work cũ, xóa/lock local private projection theo retention policy, reset engine/account state đúng contract và rebuild cho account mới. Không dùng iCloud identifier như app authentication thay thế nếu product có account riêng mà chưa thiết kế linking.

### Schema và operations

Development schema cần deploy có chủ đích; field/type/index migration và backward compatibility phải được review như API change. Asset/file có lifecycle, quota và retry riêng. Tôn trọng `CKError` retry-after, batch limits và partial errors; log operation/record class/error code không log user content.

## Production Case

### Context

Notes sync giữa iPhone/iPad bằng CKSyncEngine.

### Symptom

Sau switch iCloud account, note cũ lóe lên; edit offline đôi khi bị remote copy ghi đè.

### Investigation

Trace account generation, local transaction, pending change, engine state version và change tag. Repository singleton reuse database file; fetch callback account cũ commit sau switch. Conflict handler luôn chọn server record.

### Root Cause

Thiếu account-scoped storage/generation và conflict policy mặc định làm mất local edit.

### Fix

Partition local store theo account scope, cancel/generation-check event, reset engine state đúng account và merge field/version theo ADR.

### Prevention

Multi-device matrix: offline/offline edit, delete/update, sign-out giữa sync, rate limit, partial failure, schema mixed-version và process kill khi persist engine state.

## Interview Questions

### Foundation

**CloudKit có phải local database không?** Không; nó vận chuyển/lưu remote records, app vẫn cần local model/cache cho offline và UI responsiveness.

### Middle

**Khi nào chọn CKSyncEngine thay vì Core Data mirroring?** Khi cần local model/control/conflict mapping rõ hơn nhưng muốn engine điều phối send/fetch/retry.

### Senior

**Thiết kế account-safe CloudKit sync?** Partition local state, durable engine state/outbox, generation gating, conflict/tombstone, schema rollout, retry-after, partial failure và eventual-consistency UX.

## Exercises

### Easy

So sánh ba integration option theo control, complexity và conflict ownership.

### Medium

Thiết kế local transaction atomically lưu note + pending change.

### Hard

Viết ADR conflict policy cho cùng record sửa offline ở ba device và delete/update race.

### Debugging Lab

Switch account giữa fetch và local commit; chứng minh callback cũ không ghi vào store mới.

## Cheat Sheet

```text
local store          → UI/offline source of truth
pending changes      → durable, idempotent intent
CKSyncEngine state   → persist across launches
sent/fetched events  → apply per record, handle partial failure
conflict             → explicit domain policy
account switch       → partition + cancel/generation + rebuild
periodic sync        → indeterminate cadence
schema               → versioned production contract
```

## Chapter Summary

1. CloudKit không loại bỏ local data/sync architecture.
2. Integration level quyết định phần complexity app sở hữu.
3. Pending changes và engine state phải durable.
4. Conflict, tombstone và partial failure cần policy explicit.
5. Account switch và schema deployment là production-critical lifecycle.

## Related Chapters

- [Offline-first synchronization](../Phase-07-Persistence/12-offline-first-synchronization.md)
- [Conflict resolution](../Phase-07-Persistence/13-conflict-detection-va-resolution.md)
- [Account isolation](../Phase-07-Persistence/14-logout-login-va-data-isolation-giua-account.md)

## References

- [Apple — Deciding whether CloudKit is right for your app](https://developer.apple.com/documentation/cloudkit/deciding-whether-cloudkit-is-right-for-your-app)
- [Apple — CloudKit](https://developer.apple.com/documentation/cloudkit)
- [Apple — CKSyncEngine](https://developer.apple.com/documentation/cloudkit/cksyncengine-5sie5)
- [Apple — Syncing a Core Data Store with CloudKit](https://developer.apple.com/documentation/coredata/syncing-a-core-data-store-with-cloudkit)
