---
title: "Phase Review — Global Interview"
phase: "Global Interview"
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
  - "global-interview"
---

# Phase Review — Global Interview

## Phase Summary

Phase hoàn thành mục tiêu: **tổng hợp kiến thức thành câu trả lời đúng, có chiều sâu và production awareness**. Review này không dạy lại từng định nghĩa; nó buộc người đọc nối knowledge graph, giải thích trade-off và xử lý production case bằng evidence.

## Chapter Map

1. [01 — Swift Core review](01-swift-core-review.md)
2. [02 — Memory review](02-memory-review.md)
3. [03 — Concurrency review](03-concurrency-review.md)
4. [04 — UIKit review](04-uikit-review.md)
5. [05 — SwiftUI review](05-swiftui-review.md)
6. [06 — Networking review](06-networking-review.md)
7. [07 — Persistence review](07-persistence-review.md)
8. [08 — Architecture review](08-architecture-review.md)
9. [09 — Testing review](09-testing-review.md)
10. [10 — Performance & Security review](10-performance-and-security-review.md)
11. [11 — Production scenario interview](11-production-scenario-interview.md)
12. [12 — Swift coding interview](12-swift-coding-interview.md)
13. [13 — iOS engineering coding](13-ios-engineering-coding.md)
14. [14 — Mobile System Design interview](14-mobile-system-design-interview.md)
15. [15 — Behavioral engineering](15-behavioral-engineering.md)
16. [16 — Mock interview Junior/Middle/Senior](16-mock-interview-junior-middle-senior.md)
17. [17 — Interview question bank & coverage map](17-interview-question-bank-and-coverage-map.md)

## Knowledge Map

```text
Swift Core review → Memory review → Concurrency review → UIKit review → SwiftUI review → Networking review
        ↓
Ownership / State / Failure / Lifecycle
        ↓
Production evidence + interview reasoning
```

Mỗi edge phải trả lời “vì sao concept trước là prerequisite của concept sau?”. Nếu không trả lời được, quay lại chapter gốc thay vì học thuộc review.

## Phase Cheat Sheet

```text
Goal       → tổng hợp kiến thức thành câu trả lời đúng, có chiều sâu và production awareness
Mental     → Clarify → 30-second thesis → mechanism/trade-off → example → production evidence → senior extension
Runtime    → Câu trả lời framework/runtime phải tách documented behavior khỏi inference và tránh slogan.
Memory     → Khi object graph xuất hiện, luôn nói creator, owner, release và expected deinit.
Concurrency→ Khi async xuất hiện, luôn nói task owner, isolation, cancellation, lifetime và ordering.
Evidence   → Timed mock, rubric correctness/depth/reasoning/production/communication và feedback log.
```

## Review Questions

1. Với Swift Core review, invariant, owner và evidence chính là gì?
2. Với Memory review, invariant, owner và evidence chính là gì?
3. Với Concurrency review, invariant, owner và evidence chính là gì?
4. Với UIKit review, invariant, owner và evidence chính là gì?
5. Với SwiftUI review, invariant, owner và evidence chính là gì?
6. Với Networking review, invariant, owner và evidence chính là gì?
7. Với Persistence review, invariant, owner và evidence chính là gì?
8. Với Architecture review, invariant, owner và evidence chính là gì?
9. Với Testing review, invariant, owner và evidence chính là gì?
10. Với Performance & Security review, invariant, owner và evidence chính là gì?
11. Với Production scenario interview, invariant, owner và evidence chính là gì?
12. Với Swift coding interview, invariant, owner và evidence chính là gì?
13. Với iOS engineering coding, invariant, owner và evidence chính là gì?
14. Với Mobile System Design interview, invariant, owner và evidence chính là gì?
15. Với Behavioral engineering, invariant, owner và evidence chính là gì?
16. Với Mock interview Junior/Middle/Senior, invariant, owner và evidence chính là gì?
17. Với Interview question bank & coverage map, invariant, owner và evidence chính là gì?

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

- [The Swift Programming Language](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/) — truy cập 2026-08-09.
- [Apple Developer Documentation](https://developer.apple.com/documentation/) — truy cập 2026-08-09.
- [Swift Evolution](https://www.swift.org/swift-evolution/) — truy cập 2026-08-09.

## Completion Checklist

- [x] Phase summary, cheat sheet và knowledge map
- [x] Review/deep-dive questions
- [x] Coding exercises và debugging lab
- [x] Mini project/case study
- [x] Mock interview
- [x] Tất cả mandatory chapters có file complete
