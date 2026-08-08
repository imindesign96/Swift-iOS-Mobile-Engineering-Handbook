# Phase 02 — Memory & Runtime

Phase này tập trung vào mục tiêu: **lý luận object graph bằng creator, owner, release và expected deinit**.

## Dependency map

```text
Creator → strong ownership graph → release edges → reference count về 0 → deinit
      ↓
Runtime + Memory + Concurrency + Architecture
      ↓
Production evidence + Interview synthesis
```

## Learning outcomes

- Giải thích concept bằng behavior, constraint và trade-off.
- Xác định owner/state/failure/lifecycle cho Commerce flow.
- Dùng Xcode Memory Graph, Instruments Leaks/Allocations, deinit probe và repeated-flow measurement. thay vì đoán root cause.
- Hoàn thành coding exercise, debugging lab và mock interview của phase.

## Chapters — Complete

- [01 — Stack/Heap: mental model hữu ích và giới hạn](01-stack-heap-mental-model-huu-ich-va-gioi-han.md)
- [02 — Copy, value semantics và mutation](02-copy-value-semantics-va-mutation.md)
- [03 — Copy-on-Write: khi copy chưa thực sự copy](03-copy-on-write-khi-copy-chua-thuc-su-copy.md)
- [04 — ARC và ownership graph](04-arc-va-ownership-graph.md)
- [05 — `strong`, `weak`, `unowned` theo lifetime](05-strong-weak-unowned-theo-lifetime.md)
- [06 — Closure capture, escaping và capture list](06-closure-capture-escaping-va-capture-list.md)
- [07 — Vì sao ViewController không `deinit`?](07-vi-sao-viewcontroller-khong-deinit.md)
- [08 — Delegate, timer, observer và task lifetime](08-delegate-timer-observer-va-task-lifetime.md)
- [09 — `deinit` và lifecycle diagnostics](09-deinit-va-lifecycle-diagnostics.md)
- [10 — Memory Graph, Leaks và Allocations](10-memory-graph-leaks-va-allocations.md)
- [11 — Leak vs memory pressure](11-leak-vs-memory-pressure.md)
- [99 — Phase Review: Memory & Runtime](99-phase-review.md)

## Quality gate

Toàn bộ chapter có front matter `status: complete`, production case, debugging evidence, interview questions, exercises, cheat sheet, references và links nội bộ hợp lệ.
