---
title: "Phase Review — Memory & Runtime"
phase: "Memory & Runtime"
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
  - "memory-and-runtime"
---

# Phase Review — Memory & Runtime

## Phase Summary

Phase hoàn thành mục tiêu: **lý luận object graph bằng creator, owner, release và expected deinit**. Review này không dạy lại từng định nghĩa; nó buộc người đọc nối knowledge graph, giải thích trade-off và xử lý production case bằng evidence.

## Chapter Map

1. [01 — Stack/Heap: mental model hữu ích và giới hạn](01-stack-heap-mental-model-huu-ich-va-gioi-han.md)
2. [02 — Copy, value semantics và mutation](02-copy-value-semantics-va-mutation.md)
3. [03 — Copy-on-Write: khi copy chưa thực sự copy](03-copy-on-write-khi-copy-chua-thuc-su-copy.md)
4. [04 — ARC và ownership graph](04-arc-va-ownership-graph.md)
5. [05 — `strong`, `weak`, `unowned` theo lifetime](05-strong-weak-unowned-theo-lifetime.md)
6. [06 — Closure capture, escaping và capture list](06-closure-capture-escaping-va-capture-list.md)
7. [07 — Vì sao ViewController không `deinit`?](07-vi-sao-viewcontroller-khong-deinit.md)
8. [08 — Delegate, timer, observer và task lifetime](08-delegate-timer-observer-va-task-lifetime.md)
9. [09 — `deinit` và lifecycle diagnostics](09-deinit-va-lifecycle-diagnostics.md)
10. [10 — Memory Graph, Leaks và Allocations](10-memory-graph-leaks-va-allocations.md)
11. [11 — Leak vs memory pressure](11-leak-vs-memory-pressure.md)

## Knowledge Map

```text
Stack/Heap: mental model hữu ích và giới hạn → Copy, value semantics và mutation → Copy-on-Write: khi copy chưa thực sự copy → ARC và ownership graph → `strong`, `weak`, `unowned` theo lifetime → Closure capture, escaping và capture list
        ↓
Ownership / State / Failure / Lifecycle
        ↓
Production evidence + interview reasoning
```

Mỗi edge phải trả lời “vì sao concept trước là prerequisite của concept sau?”. Nếu không trả lời được, quay lại chapter gốc thay vì học thuộc review.

## Phase Cheat Sheet

```text
Goal       → lý luận object graph bằng creator, owner, release và expected deinit
Mental     → Creator → strong ownership graph → release edges → reference count về 0 → deinit
Runtime    → ARC chèn retain/release theo semantics của chương trình; graph ownership, không phải một dòng weak, quyết định lifetime.
Memory     → Vẽ graph strong/weak/unowned và phân biệt leak với legitimate memory pressure.
Concurrency→ Task, callback và actor có thể kéo dài lifetime; cancellation không đồng nghĩa object được giải phóng ngay.
Evidence   → Xcode Memory Graph, Instruments Leaks/Allocations, deinit probe và repeated-flow measurement.
```

## Review Questions

1. Với Stack/Heap: mental model hữu ích và giới hạn, invariant, owner và evidence chính là gì?
2. Với Copy, value semantics và mutation, invariant, owner và evidence chính là gì?
3. Với Copy-on-Write: khi copy chưa thực sự copy, invariant, owner và evidence chính là gì?
4. Với ARC và ownership graph, invariant, owner và evidence chính là gì?
5. Với `strong`, `weak`, `unowned` theo lifetime, invariant, owner và evidence chính là gì?
6. Với Closure capture, escaping và capture list, invariant, owner và evidence chính là gì?
7. Với Vì sao ViewController không `deinit`?, invariant, owner và evidence chính là gì?
8. Với Delegate, timer, observer và task lifetime, invariant, owner và evidence chính là gì?
9. Với `deinit` và lifecycle diagnostics, invariant, owner và evidence chính là gì?
10. Với Memory Graph, Leaks và Allocations, invariant, owner và evidence chính là gì?
11. Với Leak vs memory pressure, invariant, owner và evidence chính là gì?

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

- [Automatic Reference Counting](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/automaticreferencecounting/) — truy cập 2026-08-09.
- [Gathering information about memory use](https://developer.apple.com/documentation/xcode/gathering-information-about-memory-use) — truy cập 2026-08-09.
- [Memory safety](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/memorysafety/) — truy cập 2026-08-09.

## Completion Checklist

- [x] Phase summary, cheat sheet và knowledge map
- [x] Review/deep-dive questions
- [x] Coding exercises và debugging lab
- [x] Mini project/case study
- [x] Mock interview
- [x] Tất cả mandatory chapters có file complete
