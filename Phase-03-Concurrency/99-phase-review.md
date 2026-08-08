---
title: "Phase Review — Concurrency"
phase: "Concurrency"
difficulty: 5
importance: 5
interview_frequency: 5
status: complete
last_verified: 2026-08-09
swift_baseline: "Swift 6.3 toolchain; Swift 6 language mode"
levels:
  - L1
  - L2
  - L3
  - L4
  - L5
  - L6
prerequisites:
  - "All chapters in this phase"
used_later:
  - "Following phases"
competencies:
  - "Synthesis"
  - "Production"
  - "Interview"
tags:
  - "phase-review"
  - "concurrency"
---

# Phase Review — Concurrency

## Phase Summary

Phase hoàn thành mục tiêu: **quản lý isolation, task lifetime, cancellation và ordering thay vì suy nghĩ bằng thread thuần túy**. Review này không dạy lại từng định nghĩa; nó buộc người đọc nối knowledge graph, giải thích trade-off và xử lý production case bằng evidence.

## Chapter Map

1. [01 — Thread, shared mutable state và data race](01-thread-shared-mutable-state-va-data-race.md)
2. [02 — GCD: serial/concurrent, sync/async và QoS](02-gcd-serial-concurrent-sync-async-va-qos.md)
3. [03 — Deadlock, barrier, group, semaphore và OperationQueue](03-deadlock-barrier-group-semaphore-va-operationqueue.md)
4. [04 — Điều gì thực sự xảy ra tại `await`?](04-ieu-gi-thuc-su-xay-ra-tai-await.md)
5. [05 — Task và structured concurrency](05-task-va-structured-concurrency.md)
6. [06 — `async let` và TaskGroup](06-async-let-va-taskgroup.md)
7. [07 — Cancellation là cooperative contract](07-cancellation-la-cooperative-contract.md)
8. [08 — Actor và actor isolation](08-actor-va-actor-isolation.md)
9. [09 — MainActor, global actor và UI isolation](09-mainactor-global-actor-va-ui-isolation.md)
10. [10 — Sendable, `@Sendable` và strict concurrency](10-sendable-at-sendable-va-strict-concurrency.md)
11. [11 — Actor reentrancy và logical race](11-actor-reentrancy-va-logical-race.md)
12. [12 — Structured vs unstructured vs detached task](12-structured-vs-unstructured-vs-detached-task.md)
13. [13 — Task lifetime qua screen lifecycle](13-task-lifetime-qua-screen-lifecycle.md)
14. [14 — Migration từ callback/GCD sang async/await](14-migration-tu-callback-gcd-sang-async-await.md)
15. [15 — Priority inversion, thread explosion và performance](15-priority-inversion-thread-explosion-va-performance.md)
16. [16 — Reactive Programming với Combine: stream, demand, scheduling và cancellation](16-reactive-programming-voi-combine-stream-demand-scheduling-va-cancellation.md)

## Knowledge Map

```text
Thread, shared mutable state và data race → GCD: serial/concurrent, sync/async và QoS → Deadlock, barrier, group, semaphore và OperationQueue → Điều gì thực sự xảy ra tại `await`? → Task và structured concurrency → `async let` và TaskGroup
        ↓
Ownership / State / Failure / Lifecycle
        ↓
Production evidence + interview reasoning
```

Mỗi edge phải trả lời “vì sao concept trước là prerequisite của concept sau?”. Nếu không trả lời được, quay lại chapter gốc thay vì học thuộc review.

## Phase Cheat Sheet

```text
Goal       → quản lý isolation, task lifetime, cancellation và ordering thay vì suy nghĩ bằng thread thuần túy
Mental     → Task owner → suspension points → isolation domain → cancellation/order → observable state
Runtime    → Một async function có thể suspend và resume; await không phải lệnh chuyển sang background thread.
Memory     → Task và closure giữ capture trong lifetime của work; unstructured work dễ sống lâu hơn screen.
Concurrency→ Phân biệt data race được isolation ngăn chặn với logical race vẫn có thể xảy ra qua nhiều bước hợp lệ.
Evidence   → Strict Concurrency diagnostics, Swift Concurrency instrument, Thread Sanitizer khi phù hợp và structured logs theo task/request.
```

## Review Questions

1. Với Thread, shared mutable state và data race, invariant, owner và evidence chính là gì?
2. Với GCD: serial/concurrent, sync/async và QoS, invariant, owner và evidence chính là gì?
3. Với Deadlock, barrier, group, semaphore và OperationQueue, invariant, owner và evidence chính là gì?
4. Với Điều gì thực sự xảy ra tại `await`?, invariant, owner và evidence chính là gì?
5. Với Task và structured concurrency, invariant, owner và evidence chính là gì?
6. Với `async let` và TaskGroup, invariant, owner và evidence chính là gì?
7. Với Cancellation là cooperative contract, invariant, owner và evidence chính là gì?
8. Với Actor và actor isolation, invariant, owner và evidence chính là gì?
9. Với MainActor, global actor và UI isolation, invariant, owner và evidence chính là gì?
10. Với Sendable, `@Sendable` và strict concurrency, invariant, owner và evidence chính là gì?
11. Với Actor reentrancy và logical race, invariant, owner và evidence chính là gì?
12. Với Structured vs unstructured vs detached task, invariant, owner và evidence chính là gì?
13. Với Task lifetime qua screen lifecycle, invariant, owner và evidence chính là gì?
14. Với Migration từ callback/GCD sang async/await, invariant, owner và evidence chính là gì?
15. Với Priority inversion, thread explosion và performance, invariant, owner và evidence chính là gì?
16. Với Reactive Programming với Combine: stream, demand, scheduling và cancellation, invariant, owner và evidence chính là gì?

## Deep-dive Questions

1. Constraint nào làm best practice trong phase không còn đúng?
2. Vẽ owner/state/task graph cho Product Detail hoặc Checkout.
3. Phân biệt documented behavior và implementation inference trong một API.
4. Một compile-time guarantee nào vẫn không bảo vệ business invariant?
5. Thiết kế metric và regression test cho failure mode hiếm.

## Coding Exercises

### Easy

Viết một Commerce model/flow nhỏ dùng ba concept của phase và unit test invariant.

### Medium

Refactor code có multiple sources of truth thành state transition với dependency rõ.

### Hard

Thêm cancellation, retry hoặc lifecycle interruption; chứng minh stale work không commit kết quả.

## Debugging Lab

```text
Bug report → repeated flow → symptom không deterministic
Evidence   → logs/trace/graph phù hợp
Task       → hypotheses → root cause → fix → regression prevention
```

Không được bắt đầu bằng sửa code. Nộp kèm graph, evidence trước/sau và lý do loại bỏ từng hypothesis.

## Mini Project — Global Commerce

Xây/refactor một vertical slice gồm UI event, state owner, repository boundary, test và privacy-aware logging. Scope nhỏ nhưng phải có happy path, failure, cancellation/lifecycle và metric.

## Mock Interview

- 5 phút Foundation: định nghĩa bằng behavior.
- 10 phút Middle: mechanism, ownership, trade-off.
- 15 phút Senior: production variant, migration và observability.
- Rubric: correctness, depth, reasoning, production awareness, communication.

## References

- [Concurrency — The Swift Programming Language](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/concurrency/) — truy cập 2026-08-09.
- [Swift Concurrency](https://developer.apple.com/documentation/swift/concurrency) — truy cập 2026-08-09.
- [Migrating to Swift 6](https://www.swift.org/migration/documentation/migrationguide/) — truy cập 2026-08-09.

## Completion Checklist

- [x] Phase summary, cheat sheet và knowledge map
- [x] Review/deep-dive questions
- [x] Coding exercises và debugging lab
- [x] Mini project/case study
- [x] Mock interview
- [x] Tất cả mandatory chapters có file complete
