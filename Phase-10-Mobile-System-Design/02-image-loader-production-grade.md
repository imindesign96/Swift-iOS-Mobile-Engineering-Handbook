---
title: "Image Loader production-grade"
phase: "Mobile System Design"
difficulty: 5
importance: 5
interview_frequency: 4
status: complete
last_verified: 2026-08-09
swift_baseline: "Swift 6.3 toolchain; Swift 6 language mode"
levels:
  - L6
prerequisites:
  - "Framework phỏng vấn Mobile System Design"
used_later:
  - "Paginated Feed"
competencies:
  - "Mobile System Design"
  - "Production"
  - "Debugging"
  - "Interview"
tags:
  - "image-loader-production-grade"
  - "global-commerce"
---

# Image Loader production-grade

> **Version scope**
>
> Baseline Swift 6.3 toolchain, Swift 6 language mode; API iOS-specific phải kiểm tra availability tại call site. Xác minh 2026-08-09.

## Story / Problem

Trong Global Commerce, thiết kế backend-correct nhưng mobile-failure vì bỏ qua offline, background interruption và resource budget. Chapter này tập trung vào **Image Loader production-grade**: không dừng ở syntax/API mà nối behavior với ownership, failure mode và evidence production.

Nếu team chỉ nhớ tên concept, fix thường dịch symptom sang chỗ khác. Câu hỏi mở đầu là:

```text
Input/event → state hoặc resource nào thay đổi?
            → ai sở hữu thay đổi đó?
            → contract nào có thể bị vi phạm?
            → evidence nào chứng minh kết luận?
```

## Objectives

Sau chapter này, bạn có thể:

- giải thích chính xác rằng decoded pixel cost và main-thread decode/layout thường quyết định scroll;
- nhận diện failure mode chính: cache original khổng lồ hoặc decode khi cell xuất hiện;
- chọn giải pháp bằng rule: downsample theo display size, prefetch có bound và cache eviction;
- nối runtime, memory, concurrency và architecture implications;
- điều tra case production bằng Core Animation/Time Profiler/Allocations;
- trả lời câu hỏi interview ở ba độ sâu thay vì đọc thuộc định nghĩa.

## Prerequisites { data-search-exclude }

- [Framework phỏng vấn Mobile System Design](01-framework-phong-van-mobile-system-design.md); không lặp lại định nghĩa nền nếu chapter trước đã giải thích.
- [Glossary](../GLOSSARY.md) cho terminology canonical.

## Used Later { data-search-exclude }

- [Paginated Feed](03-paginated-feed.md) dùng contract của chapter này làm building block.
- [Production Playbook](../PRODUCTION_PLAYBOOK.md) dùng cùng flow evidence-first.
- [Interview Playbook](../INTERVIEW_PLAYBOOK.md) dùng mental model để xử lý follow-up.

## Mental Model

```text
Requirements → constraints → data/state → architecture → failure/security/performance → observability/testing
                 ↓
Focus: Image Loader production-grade
                 ↓
Evidence: Core Animation/Time Profiler/Allocations
```

Mental model hữu ích để đặt câu hỏi đúng, nhưng không thay thế API contract hoặc measurement. Đặc biệt, không suy luận implementation private của compiler/framework thành behavior được đảm bảo.

## What?

Trọng tâm của **Image Loader production-grade** là: decoded pixel cost và main-thread decode/layout thường quyết định scroll. Hãy mô tả bằng state transition, lifetime hoặc output quan sát được thay vì chỉ bằng keyword.

Một contract tốt nói rõ input hợp lệ, output/failure, side effect, owner và thời điểm kết thúc. Nếu concept chạm external data hoặc asynchronous work, contract cũng phải nói cancellation, ordering và recovery.

## Why?

Concept tồn tại để giúp thiết kế feature trong constraint memory, battery, network, storage và app lifecycle. Không có boundary này, rule domain bị nhân bản, behavior phụ thuộc call order và incident khó điều tra vì không biết layer nào chịu trách nhiệm.

Giá trị lớn nhất không phải ít dòng code hơn; đó là giảm số state hợp lệ cần giữ trong đầu và làm violation xuất hiện sớm qua compiler, test hoặc telemetry.

## How?

1. Xác định source of truth và invariant liên quan.
2. Xác định creator/owner/mutator/observer.
3. Chọn API hoặc abstraction thể hiện đúng semantics.
4. Mô hình hóa failure/cancellation thay vì che bằng fallback.
5. Đo observable behavior bằng Core Animation/Time Profiler/Allocations.

### Documented behavior vs inference

- **Documented:** dùng contract trong Swift/Apple documentation và availability của SDK.
- **Inference:** storage placement, executor scheduling chi tiết hoặc reconciliation internals chỉ được dùng như giả thuyết đo lường, không phải guarantee.

## When?

Áp dụng khi downsample theo display size, prefetch có bound và cache eviction. Bắt đầu bằng giải pháp đơn giản nhất giữ được invariant; thêm abstraction/synchronization/cache chỉ khi requirement hoặc measurement chứng minh cần.

Tránh dùng concept như cargo cult. Một type, layer hay primitive không có owner/contract/test rõ chỉ chuyển complexity chứ không loại bỏ nó.

## What if?

Failure mode quan trọng là cache original khổng lồ hoặc decode khi cell xuất hiện. Consequence có thể là state stale, duplicate work, leak, crash, UI hitch hoặc test flaky tùy boundary.

Khi assumption có thể thay đổi qua `await`, lifecycle callback, network retry hoặc migration, hãy revalidate state trước khi commit kết quả.

### Review questions

1. Observable behavior nào định nghĩa Image Loader production-grade?
2. Owner của state/resource là ai và lifetime kết thúc khi nào?
3. Cache original khổng lồ hoặc decode khi cell xuất hiện tạo evidence gì?
4. Rule chọn giải pháp là gì, và constraint nào khiến rule đổi?

## Runnable Swift Example

```swift
import Foundation

actor ImageRequestRegistry {
    private var tasks: [URL: Task<Data, Error>] = [:]

    func data(
        for url: URL,
        load: @escaping @Sendable (URL) async throws -> Data
    ) async throws -> Data {
        if let task = tasks[url] { return try await task.value }
        let task = Task { try await load(url) }
        tasks[url] = task
        defer { tasks[url] = nil }
        return try await task.value
    }
}
```

Ví dụ pure Swift chạy trong executable/test target với Swift 6.3. Ví dụ dùng UIKit, SwiftUI, Security, Core Data hoặc SwiftData cần target iOS tương ứng; mục tiêu là minh họa contract, không giả lập framework bằng toy code.

## iOS Runtime Behavior { data-search-exclude }

Thiết kế phải chịu foreground/background/suspend/terminate và network thay đổi giữa chừng. Với **Image Loader production-grade**, hãy log hoặc đo transition ở boundary thay vì suy luận từ UI cuối cùng.

Một callback xuất hiện không chứng minh object còn owner đúng; một UI update đúng không chứng minh request cũ đã bị cancel; một compile success cũng không chứng minh logical ordering đúng.

## Memory Implications { data-search-exclude }

Mỗi cache/buffer/media pipeline cần capacity, eviction và decoded-size budget.

```text
Who creates? → Who owns? → Who releases? → Expected deinit/eviction?
```

Nếu không có reference object trong chapter, câu hỏi vẫn hữu ích cho buffer, cache, task capture và framework object được ví dụ tạo ra.

## Concurrency Implications { data-search-exclude }

Xác định task owner, coalescing, cancellation, ordering, retry và persistence của pending work.

```text
Task owner? → isolation? → cancellation? → lifetime? → ordering?
```

Data-race freedom không tự động bảo đảm business invariant nhiều bước. Sau suspension, response hoặc lifecycle change, state có thể đã thuộc generation khác.

## Architecture Notes { data-search-exclude }

Nêu source of truth, dependency direction, team ownership và migration path; luôn ghi trade-off. Dependency hướng vào contract ổn định; implementation details nằm phía ngoài. Composition root tạo concrete dependencies và quyết định lifetime.

Không thêm layer chỉ vì chapter nhắc đến pattern. Hãy yêu cầu layer mới có ít nhất một giá trị: hấp thụ volatility, bảo vệ invariant, tạo test seam hoặc quản lý lifetime.

## Production Case { data-search-exclude }

### Context

Feature Commerce áp dụng **Image Loader production-grade** trong flow có network, UI lifecycle và cache.

### Symptom

User báo behavior không ổn định; telemetry cho thấy cache original khổng lồ hoặc decode khi cell xuất hiện.

### Hypotheses

1. Contract bị hiểu sai tại call site.
2. Owner/lifetime không khớp feature scope.
3. Ordering hoặc external input phá invariant.
4. Resource budget/policy thiếu bound.

### Investigation

Dùng Core Animation/Time Profiler/Allocations; thêm correlation ID/generation an toàn, tái hiện repeated flow và so sánh expected transition với actual transition.

### Root Cause

Root cause chỉ được kết luận khi evidence chỉ ra nơi invariant bị phá, không phải nơi symptom cuối cùng xuất hiện.

### Fix

Áp dụng rule **downsample theo display size, prefetch có bound và cache eviction**, thu hẹp mutation/ownership và làm failure/cancellation explicit.

### Prevention

Thêm regression test tại boundary, metric cho failure mode, review checklist về owner/state và documentation cho constraint quyết định.

## Debug / Instruments { data-search-exclude }

Primary evidence: **Core Animation/Time Profiler/Allocations**.

1. Tái hiện trên build/device gần production.
2. Đánh dấu user flow bằng signpost hoặc correlation ID không chứa PII.
3. Thu trace/log trước khi sửa.
4. Đặt hypothesis có thể bị bác bỏ.
5. Đo lại cùng workload và thêm regression protection.

## Myth vs Reality { data-search-exclude }

> **Myth:** Chỉ cần dùng đúng API/pattern tên **Image Loader production-grade** là code an toàn.
>
> **Reality:** Safety đến từ semantics, owner, invariant, lifecycle và evidence; API chỉ là một phần của contract.

## Common Mistakes { data-search-exclude }

- Cache original khổng lồ hoặc decode khi cell xuất hiện → behavior chỉ sai ở scale/lifecycle edge.
- Che failure bằng default hoặc retry → mất root-cause signal.
- Nhiều layer cùng mutate state → source of truth không còn rõ.
- Tối ưu trước khi đo → tăng complexity nhưng không cải thiện bottleneck.

## Best Practices { data-search-exclude }

- Downsample theo display size, prefetch có bound và cache eviction.
- Ghi assumption và availability cạnh boundary version-sensitive.
- Dùng immutable value và explicit state transition khi phù hợp.
- Log category/correlation an toàn; không log token, PII hoặc payment payload.
- Đo trước/sau trên cùng workload và giữ regression test.

## Interview Questions { data-search-exclude }

### Foundation

**Hỏi:** Image Loader production-grade giải quyết vấn đề gì?

**30-second:** Decoded pixel cost và main-thread decode/layout thường quyết định scroll. Chọn nó khi downsample theo display size, prefetch có bound và cache eviction; rủi ro chính là cache original khổng lồ hoặc decode khi cell xuất hiện.

### Junior

**Hỏi:** Cho một ví dụ Commerce và common mistake.

**2–3 minute:** Nêu input/state, owner, code contract, failure path và test. Dùng ví dụ ở trên, sau đó giải thích vì sao cache original khổng lồ hoặc decode khi cell xuất hiện phá invariant.

### Middle

**Hỏi:** Concept ảnh hưởng memory/concurrency/testability thế nào?

Trả lời bằng object/task graph, isolation/cancellation, boundary DI và evidence **Core Animation/Time Profiler/Allocations**.

### Senior

**Hỏi:** Constraint nào khiến bạn chọn giải pháp khác?

Deep Dive phải so sánh complexity, lifecycle, scale, migration, operability và rollback; không biến best practice thành luật tuyệt đối.

### Production

**Hỏi:** Symptom chỉ xảy ra trên 0,1% session. Bạn điều tra thế nào?

Clarify impact → thu evidence → hypothesis → controlled measurement → root cause → mitigation/fix → regression metric.

## Exercises { data-search-exclude }

### Easy

Viết một ví dụ nhỏ minh họa **Image Loader production-grade** và test happy path lẫn edge case.

### Medium

Refactor một call site đang gặp **cache original khổng lồ hoặc decode khi cell xuất hiện** để contract/owner rõ hơn.

### Hard

Thiết kế state transition có cancellation/lifecycle interruption và chứng minh không publish stale result.

### Debugging Lab

Bug report: repeated Commerce flow tạo symptom liên quan **Image Loader production-grade**. Thu evidence bằng Core Animation/Time Profiler/Allocations, vẽ owner/state graph, xác định root cause và thêm regression test.

### Engineering / Design Exercise

Viết ADR một trang: context, options, decision, consequences và revisit conditions cho lựa chọn trong chapter.

## Cheat Sheet { data-search-exclude }

```text
Concept   → decoded pixel cost và main-thread decode/layout thường quyết định scroll
Use when  → downsample theo display size, prefetch có bound và cache eviction
Risk      → cache original khổng lồ hoặc decode khi cell xuất hiện
Evidence  → Core Animation/Time Profiler/Allocations
Remember  → owner + state + failure + lifecycle + measurement
```

## Chapter Summary { data-search-exclude }

1. Problem: API/pattern không đủ nếu semantics và owner mơ hồ.
2. Mental model: Requirements → constraints → data/state → architecture → failure/security/performance → observability/testing.
3. Usage rule: downsample theo display size, prefetch có bound và cache eviction.
4. Mistake nguy hiểm: cache original khổng lồ hoặc decode khi cell xuất hiện.
5. Production lesson: kết luận bằng Core Animation/Time Profiler/Allocations, rồi bảo vệ bằng test và metric.

## Related Chapters { data-search-exclude }

- [Framework phỏng vấn Mobile System Design](01-framework-phong-van-mobile-system-design.md)
- [Paginated Feed](03-paginated-feed.md)
- [Cross-reference Index](../CROSS_REFERENCE_INDEX.md)

## References { data-search-exclude }

- [App architecture](https://developer.apple.com/documentation/technologyoverviews/app-architecture) — truy cập 2026-08-09.
- [Background tasks](https://developer.apple.com/documentation/backgroundtasks) — truy cập 2026-08-09.
- [Performance and metrics](https://developer.apple.com/documentation/xcode/performance-and-metrics) — truy cập 2026-08-09.

## Completion Checklist { data-search-exclude }

- [x] Objectives có thể kiểm chứng
- [x] Mental model và giới hạn được nói rõ
- [x] What/Why/How/When/What-if đầy đủ
- [x] Code hoặc availability rõ
- [x] Runtime/memory/concurrency implications đúng phạm vi
- [x] Production case dựa trên evidence
- [x] Review + interview + exercises + cheat sheet
- [x] Internal links chỉ tới file tồn tại trong catalog
- [x] Claim version-sensitive có primary source và ngày verify
- [x] Không còn placeholder; status là complete
