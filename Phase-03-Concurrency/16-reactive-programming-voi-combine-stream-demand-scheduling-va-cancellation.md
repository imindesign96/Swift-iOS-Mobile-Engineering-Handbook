---
title: "Reactive Programming với Combine: stream, demand, scheduling và cancellation"
phase: "Concurrency"
difficulty: 3
importance: 5
interview_frequency: 4
status: complete
last_verified: 2026-08-09
swift_baseline: "Swift 6.3 toolchain; Swift 6 language mode"
levels:
  - L2
prerequisites:
  - "Priority inversion, thread explosion và performance"
used_later:
  - "Phase Review: Concurrency"
competencies:
  - "Concurrency"
  - "Production"
  - "Debugging"
  - "Interview"
tags:
  - "reactive-programming-voi-combine-stream-demand-scheduling-va-cancellation"
  - "global-commerce"
---

# Reactive Programming với Combine: stream, demand, scheduling và cancellation

> **Version scope**
>
> Baseline Swift 6.3 toolchain, Swift 6 language mode; API iOS-specific phải kiểm tra availability tại call site. Xác minh 2026-08-09.

## Story / Problem

Trong Global Commerce, nhiều request Commerce hoàn tất khác thứ tự, tạo duplicate work hoặc ghi đè state mới bằng response cũ. Chapter này tập trung vào **Reactive Programming với Combine: stream, demand, scheduling và cancellation**: không dừng ở syntax/API mà nối behavior với ownership, failure mode và evidence production.

Nếu team chỉ nhớ tên concept, fix thường dịch symptom sang chỗ khác. Câu hỏi mở đầu là:

```text
Input/event → state hoặc resource nào thay đổi?
            → ai sở hữu thay đổi đó?
            → contract nào có thể bị vi phạm?
            → evidence nào chứng minh kết luận?
```

## Objectives

Sau chapter này, bạn có thể:

- giải thích chính xác rằng Reactive Programming mô hình hóa value, completion và failure theo thời gian; Combine nối Publisher, operator, Subscriber và Subscription thành một contract có demand/cancellation;
- nhận diện failure mode chính: pipeline giữ subscription sai lifetime, scheduler hop mơ hồ, nested subscription hoặc bridge async/await làm mất cancellation;
- chọn giải pháp bằng rule: dùng Combine khi feature cần compose nhiều event stream hoặc operator theo thời gian; dùng async/await cho one-shot flow và AsyncSequence cho stream tuần tự đơn giản;
- nối runtime, memory, concurrency và architecture implications;
- điều tra case production bằng Combine event trace, subscription lifetime, scheduler assertion và deterministic virtual-time test;
- trả lời câu hỏi interview ở ba độ sâu thay vì đọc thuộc định nghĩa.

## Prerequisites { data-search-exclude }

- [Priority inversion, thread explosion và performance](15-priority-inversion-thread-explosion-va-performance.md); không lặp lại định nghĩa nền nếu chapter trước đã giải thích.
- [Glossary](../GLOSSARY.md) cho terminology canonical.

## Used Later { data-search-exclude }

- [Phase Review: Concurrency](99-phase-review.md) dùng contract của chapter này làm building block.
- [Production Playbook](../PRODUCTION_PLAYBOOK.md) dùng cùng flow evidence-first.
- [Interview Playbook](../INTERVIEW_PLAYBOOK.md) dùng mental model để xử lý follow-up.

## Mental Model

```text
Task owner → suspension points → isolation domain → cancellation/order → observable state
                 ↓
Focus: Reactive Programming với Combine: stream, demand, scheduling và cancellation
                 ↓
Evidence: Combine event trace, subscription lifetime, scheduler assertion và deterministic virtual-time test
```

Mental model hữu ích để đặt câu hỏi đúng, nhưng không thay thế API contract hoặc measurement. Đặc biệt, không suy luận implementation private của compiler/framework thành behavior được đảm bảo.

## What?

Trọng tâm của **Reactive Programming với Combine: stream, demand, scheduling và cancellation** là: Reactive Programming mô hình hóa value, completion và failure theo thời gian; Combine nối Publisher, operator, Subscriber và Subscription thành một contract có demand/cancellation. Hãy mô tả bằng state transition, lifetime hoặc output quan sát được thay vì chỉ bằng keyword.

Một contract tốt nói rõ input hợp lệ, output/failure, side effect, owner và thời điểm kết thúc. Nếu concept chạm external data hoặc asynchronous work, contract cũng phải nói cancellation, ordering và recovery.

## Why?

Concept tồn tại để giúp quản lý isolation, task lifetime, cancellation và ordering thay vì suy nghĩ bằng thread thuần túy. Không có boundary này, rule domain bị nhân bản, behavior phụ thuộc call order và incident khó điều tra vì không biết layer nào chịu trách nhiệm.

Giá trị lớn nhất không phải ít dòng code hơn; đó là giảm số state hợp lệ cần giữ trong đầu và làm violation xuất hiện sớm qua compiler, test hoặc telemetry.

## How?

1. Xác định source of truth và invariant liên quan.
2. Xác định creator/owner/mutator/observer.
3. Chọn API hoặc abstraction thể hiện đúng semantics.
4. Mô hình hóa failure/cancellation thay vì che bằng fallback.
5. Đo observable behavior bằng Combine event trace, subscription lifetime, scheduler assertion và deterministic virtual-time test.

## Technical Deep Dive

### Stream contract và lifecycle

Một Combine pipeline có bốn chiều phải đọc cùng nhau: `Output`, `Failure`, thời gian và lifetime. `Publisher` không phải collection đã có sẵn; subscription khởi tạo quan hệ, Subscriber tạo demand, upstream phát value/completion và cancellation cắt quan hệ đó. `AnyCancellable` vì vậy là ownership token. Store nó ở scope quá ngắn làm pipeline dừng sớm; store toàn app làm feature và capture sống quá lâu.

Phân biệt `subscribe(on:)` với `receive(on:)`: cái đầu ảnh hưởng nơi subscription/request/cancel diễn ra, cái sau chuyển delivery downstream. Không rải scheduler operator để chữa warning UI. Hãy xác định upstream có thread-safety contract gì, operator nào làm work nặng, và chỉ hop về main ngay trước UI state.

Với search-as-you-type, `debounce` giảm input burst, `removeDuplicates` bỏ query giống nhau, `map` tạo request publisher và `switchToLatest` hủy generation cũ. `flatMap` không mặc định thay thế request cũ; chọn sai operator có thể để response cũ ghi đè query mới. Error completion cũng kết thúc pipeline, vì vậy retry/catch phải phản ánh recovery policy chứ không chỉ giữ UI im lặng.

### Combine, async/await và AsyncSequence

- One-shot request tuyến tính: ưu tiên `async throws`.
- Nhiều value theo thời gian, cần debounce/combine/share: Combine thường diễn đạt tốt.
- Stream được consume tuần tự bằng structured task: `AsyncSequence` thường đơn giản hơn.
- Khi bridge `Publisher.values` hoặc `Future`, kiểm tra cancellation, buffering và việc một API có eager hay lazy hay không.

Test operator theo virtual/test scheduler hoặc dependency clock; assertion phải cover value order, completion, cancellation và scheduler-sensitive state.

### Documented behavior vs inference

- **Documented:** dùng contract trong Swift/Apple documentation và availability của SDK.
- **Inference:** storage placement, executor scheduling chi tiết hoặc reconciliation internals chỉ được dùng như giả thuyết đo lường, không phải guarantee.

## When?

Áp dụng khi dùng Combine khi feature cần compose nhiều event stream hoặc operator theo thời gian; dùng async/await cho one-shot flow và AsyncSequence cho stream tuần tự đơn giản. Bắt đầu bằng giải pháp đơn giản nhất giữ được invariant; thêm abstraction/synchronization/cache chỉ khi requirement hoặc measurement chứng minh cần.

Tránh dùng concept như cargo cult. Một type, layer hay primitive không có owner/contract/test rõ chỉ chuyển complexity chứ không loại bỏ nó.

## What if?

Failure mode quan trọng là pipeline giữ subscription sai lifetime, scheduler hop mơ hồ, nested subscription hoặc bridge async/await làm mất cancellation. Consequence có thể là state stale, duplicate work, leak, crash, UI hitch hoặc test flaky tùy boundary.

Khi assumption có thể thay đổi qua `await`, lifecycle callback, network retry hoặc migration, hãy revalidate state trước khi commit kết quả.

### Review questions

1. Observable behavior nào định nghĩa Reactive Programming với Combine: stream, demand, scheduling và cancellation?
2. Owner của state/resource là ai và lifetime kết thúc khi nào?
3. Pipeline giữ subscription sai lifetime, scheduler hop mơ hồ, nested subscription hoặc bridge async/await làm mất cancellation tạo evidence gì?
4. Rule chọn giải pháp là gì, và constraint nào khiến rule đổi?

## Implementation Example

```swift
import Combine
import Foundation

final class ProductSearchModel {
    @Published var query = ""
    @Published private(set) var products: [Product] = []
    private var cancellables = Set<AnyCancellable>()

    init(search: @escaping (String) -> AnyPublisher<[Product], Error>) {
        $query
            .debounce(for: .milliseconds(300), scheduler: DispatchQueue.main)
            .removeDuplicates()
            .map(search)
            .switchToLatest() // hủy subscription của query cũ
            .replaceError(with: [])
            .receive(on: DispatchQueue.main)
            .assign(to: &$products)
    }
}
```

Ví dụ Swift chạy trong executable/test target hoặc iOS target tương ứng. Ví dụ Ruby mô tả `Fastfile` versioned. Mục tiêu là minh họa contract thực tế, không giả lập framework bằng toy code.

## iOS Runtime Behavior { data-search-exclude }

Một async function có thể suspend và resume; await không phải lệnh chuyển sang background thread. Với **Reactive Programming với Combine: stream, demand, scheduling và cancellation**, hãy log hoặc đo transition ở boundary thay vì suy luận từ UI cuối cùng.

Một callback xuất hiện không chứng minh object còn owner đúng; một UI update đúng không chứng minh request cũ đã bị cancel; một compile success cũng không chứng minh logical ordering đúng.

## Memory Implications { data-search-exclude }

Task và closure giữ capture trong lifetime của work; unstructured work dễ sống lâu hơn screen.

```text
Who creates? → Who owns? → Who releases? → Expected deinit/eviction?
```

Nếu không có reference object trong chapter, câu hỏi vẫn hữu ích cho buffer, cache, task capture và framework object được ví dụ tạo ra.

## Concurrency Implications { data-search-exclude }

Phân biệt data race được isolation ngăn chặn với logical race vẫn có thể xảy ra qua nhiều bước hợp lệ.

```text
Task owner? → isolation? → cancellation? → lifetime? → ordering?
```

Data-race freedom không tự động bảo đảm business invariant nhiều bước. Sau suspension, response hoặc lifecycle change, state có thể đã thuộc generation khác.

## Architecture Notes { data-search-exclude }

Đặt task ownership ở layer gắn với lifecycle; repository/actor sở hữu state chia sẻ, UI state thuộc MainActor. Dependency hướng vào contract ổn định; implementation details nằm phía ngoài. Composition root tạo concrete dependencies và quyết định lifetime.

Không thêm layer chỉ vì chapter nhắc đến pattern. Hãy yêu cầu layer mới có ít nhất một giá trị: hấp thụ volatility, bảo vệ invariant, tạo test seam hoặc quản lý lifetime.

## Production Case { data-search-exclude }

### Context

Feature Commerce áp dụng **Reactive Programming với Combine: stream, demand, scheduling và cancellation** trong flow có network, UI lifecycle và cache.

### Symptom

User báo behavior không ổn định; telemetry cho thấy pipeline giữ subscription sai lifetime, scheduler hop mơ hồ, nested subscription hoặc bridge async/await làm mất cancellation.

### Hypotheses

1. Contract bị hiểu sai tại call site.
2. Owner/lifetime không khớp feature scope.
3. Ordering hoặc external input phá invariant.
4. Resource budget/policy thiếu bound.

### Investigation

Dùng Combine event trace, subscription lifetime, scheduler assertion và deterministic virtual-time test; thêm correlation ID/generation an toàn, tái hiện repeated flow và so sánh expected transition với actual transition.

### Root Cause

Root cause chỉ được kết luận khi evidence chỉ ra nơi invariant bị phá, không phải nơi symptom cuối cùng xuất hiện.

### Fix

Áp dụng rule **dùng Combine khi feature cần compose nhiều event stream hoặc operator theo thời gian; dùng async/await cho one-shot flow và AsyncSequence cho stream tuần tự đơn giản**, thu hẹp mutation/ownership và làm failure/cancellation explicit.

### Prevention

Thêm regression test tại boundary, metric cho failure mode, review checklist về owner/state và documentation cho constraint quyết định.

## Debug / Instruments { data-search-exclude }

Primary evidence: **Combine event trace, subscription lifetime, scheduler assertion và deterministic virtual-time test**.

1. Tái hiện trên build/device gần production.
2. Đánh dấu user flow bằng signpost hoặc correlation ID không chứa PII.
3. Thu trace/log trước khi sửa.
4. Đặt hypothesis có thể bị bác bỏ.
5. Đo lại cùng workload và thêm regression protection.

## Myth vs Reality { data-search-exclude }

> **Myth:** Chỉ cần dùng đúng API/pattern tên **Reactive Programming với Combine: stream, demand, scheduling và cancellation** là code an toàn.
>
> **Reality:** Safety đến từ semantics, owner, invariant, lifecycle và evidence; API chỉ là một phần của contract.

## Common Mistakes { data-search-exclude }

- Pipeline giữ subscription sai lifetime, scheduler hop mơ hồ, nested subscription hoặc bridge async/await làm mất cancellation → behavior chỉ sai ở scale/lifecycle edge.
- Che failure bằng default hoặc retry → mất root-cause signal.
- Nhiều layer cùng mutate state → source of truth không còn rõ.
- Tối ưu trước khi đo → tăng complexity nhưng không cải thiện bottleneck.

## Best Practices { data-search-exclude }

- Dùng combine khi feature cần compose nhiều event stream hoặc operator theo thời gian; dùng async/await cho one-shot flow và asyncsequence cho stream tuần tự đơn giản.
- Ghi assumption và availability cạnh boundary version-sensitive.
- Dùng immutable value và explicit state transition khi phù hợp.
- Log category/correlation an toàn; không log token, PII hoặc payment payload.
- Đo trước/sau trên cùng workload và giữ regression test.

## Interview Questions { data-search-exclude }

### Foundation

**Hỏi:** Reactive Programming với Combine: stream, demand, scheduling và cancellation giải quyết vấn đề gì?

**30-second:** Reactive programming mô hình hóa value, completion và failure theo thời gian; combine nối publisher, operator, subscriber và subscription thành một contract có demand/cancellation. Chọn nó khi dùng Combine khi feature cần compose nhiều event stream hoặc operator theo thời gian; dùng async/await cho one-shot flow và AsyncSequence cho stream tuần tự đơn giản; rủi ro chính là pipeline giữ subscription sai lifetime, scheduler hop mơ hồ, nested subscription hoặc bridge async/await làm mất cancellation.

### Junior

**Hỏi:** Cho một ví dụ Commerce và common mistake.

**2–3 minute:** Nêu input/state, owner, code contract, failure path và test. Dùng ví dụ ở trên, sau đó giải thích vì sao pipeline giữ subscription sai lifetime, scheduler hop mơ hồ, nested subscription hoặc bridge async/await làm mất cancellation phá invariant.

### Middle

**Hỏi:** Concept ảnh hưởng memory/concurrency/testability thế nào?

Trả lời bằng object/task graph, isolation/cancellation, boundary DI và evidence **Combine event trace, subscription lifetime, scheduler assertion và deterministic virtual-time test**.

### Senior

**Hỏi:** Constraint nào khiến bạn chọn giải pháp khác?

Deep Dive phải so sánh complexity, lifecycle, scale, migration, operability và rollback; không biến best practice thành luật tuyệt đối.

### Production

**Hỏi:** Symptom chỉ xảy ra trên 0,1% session. Bạn điều tra thế nào?

Clarify impact → thu evidence → hypothesis → controlled measurement → root cause → mitigation/fix → regression metric.

## Exercises { data-search-exclude }

### Easy

Viết một ví dụ nhỏ minh họa **Reactive Programming với Combine: stream, demand, scheduling và cancellation** và test happy path lẫn edge case.

### Medium

Refactor một call site đang gặp **pipeline giữ subscription sai lifetime, scheduler hop mơ hồ, nested subscription hoặc bridge async/await làm mất cancellation** để contract/owner rõ hơn.

### Hard

Thiết kế state transition có cancellation/lifecycle interruption và chứng minh không publish stale result.

### Debugging Lab

Bug report: repeated Commerce flow tạo symptom liên quan **Reactive Programming với Combine: stream, demand, scheduling và cancellation**. Thu evidence bằng Combine event trace, subscription lifetime, scheduler assertion và deterministic virtual-time test, vẽ owner/state graph, xác định root cause và thêm regression test.

### Engineering / Design Exercise

Viết ADR một trang: context, options, decision, consequences và revisit conditions cho lựa chọn trong chapter.

## Cheat Sheet { data-search-exclude }

```text
Concept   → Reactive Programming mô hình hóa value, completion và failure theo thời gian; Combine nối Publisher, operator, Subscriber và Subscription thành một contract có demand/cancellation
Use when  → dùng Combine khi feature cần compose nhiều event stream hoặc operator theo thời gian; dùng async/await cho one-shot flow và AsyncSequence cho stream tuần tự đơn giản
Risk      → pipeline giữ subscription sai lifetime, scheduler hop mơ hồ, nested subscription hoặc bridge async/await làm mất cancellation
Evidence  → Combine event trace, subscription lifetime, scheduler assertion và deterministic virtual-time test
Remember  → owner + state + failure + lifecycle + measurement
```

## Chapter Summary { data-search-exclude }

1. Problem: API/pattern không đủ nếu semantics và owner mơ hồ.
2. Mental model: Task owner → suspension points → isolation domain → cancellation/order → observable state.
3. Usage rule: dùng Combine khi feature cần compose nhiều event stream hoặc operator theo thời gian; dùng async/await cho one-shot flow và AsyncSequence cho stream tuần tự đơn giản.
4. Mistake nguy hiểm: pipeline giữ subscription sai lifetime, scheduler hop mơ hồ, nested subscription hoặc bridge async/await làm mất cancellation.
5. Production lesson: kết luận bằng Combine event trace, subscription lifetime, scheduler assertion và deterministic virtual-time test, rồi bảo vệ bằng test và metric.

## Related Chapters { data-search-exclude }

- [Priority inversion, thread explosion và performance](15-priority-inversion-thread-explosion-va-performance.md)
- [Phase Review: Concurrency](99-phase-review.md)
- [Cross-reference Index](../CROSS_REFERENCE_INDEX.md)

## References { data-search-exclude }

- [Concurrency — The Swift Programming Language](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/concurrency/) — truy cập 2026-08-09.
- [Swift Concurrency](https://developer.apple.com/documentation/swift/concurrency) — truy cập 2026-08-09.
- [Migrating to Swift 6](https://www.swift.org/migration/documentation/migrationguide/) — truy cập 2026-08-09.
- [Combine](https://developer.apple.com/documentation/combine) — truy cập 2026-08-09.
- [Publisher](https://developer.apple.com/documentation/combine/publisher) — truy cập 2026-08-09.

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
