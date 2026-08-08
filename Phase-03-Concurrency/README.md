# Phase 03 — Concurrency

Phase này tập trung vào mục tiêu: **quản lý isolation, task lifetime, cancellation và ordering thay vì suy nghĩ bằng thread thuần túy**.

## Dependency map

```text
Task owner → suspension points → isolation domain → cancellation/order → observable state
      ↓
Runtime + Memory + Concurrency + Architecture
      ↓
Production evidence + Interview synthesis
```

## Learning outcomes

- Giải thích concept bằng behavior, constraint và trade-off.
- Xác định owner/state/failure/lifecycle cho Commerce flow.
- Dùng Strict Concurrency diagnostics, Swift Concurrency instrument, Thread Sanitizer khi phù hợp và structured logs theo task/request. thay vì đoán root cause.
- Hoàn thành coding exercise, debugging lab và mock interview của phase.

## Chapters — Complete

- [01 — Thread, shared mutable state và data race](01-thread-shared-mutable-state-va-data-race.md)
- [02 — GCD: serial/concurrent, sync/async và QoS](02-gcd-serial-concurrent-sync-async-va-qos.md)
- [03 — Deadlock, barrier, group, semaphore và OperationQueue](03-deadlock-barrier-group-semaphore-va-operationqueue.md)
- [04 — Điều gì thực sự xảy ra tại `await`?](04-ieu-gi-thuc-su-xay-ra-tai-await.md)
- [05 — Task và structured concurrency](05-task-va-structured-concurrency.md)
- [06 — `async let` và TaskGroup](06-async-let-va-taskgroup.md)
- [07 — Cancellation là cooperative contract](07-cancellation-la-cooperative-contract.md)
- [08 — Actor và actor isolation](08-actor-va-actor-isolation.md)
- [09 — MainActor, global actor và UI isolation](09-mainactor-global-actor-va-ui-isolation.md)
- [10 — Sendable, `@Sendable` và strict concurrency](10-sendable-at-sendable-va-strict-concurrency.md)
- [11 — Actor reentrancy và logical race](11-actor-reentrancy-va-logical-race.md)
- [12 — Structured vs unstructured vs detached task](12-structured-vs-unstructured-vs-detached-task.md)
- [13 — Task lifetime qua screen lifecycle](13-task-lifetime-qua-screen-lifecycle.md)
- [14 — Migration từ callback/GCD sang async/await](14-migration-tu-callback-gcd-sang-async-await.md)
- [15 — Priority inversion, thread explosion và performance](15-priority-inversion-thread-explosion-va-performance.md)
- [99 — Phase Review: Concurrency](99-phase-review.md)

## Quality gate

Toàn bộ chapter có front matter `status: complete`, production case, debugging evidence, interview questions, exercises, cheat sheet, references và links nội bộ hợp lệ.
