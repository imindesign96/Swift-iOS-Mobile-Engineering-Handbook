---
title: "Phase Review — Testing"
phase: "Testing"
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
  - "testing"
---

# Phase Review — Testing

## Phase Summary

Phase hoàn thành mục tiêu: **đặt confidence ở đúng boundary với test deterministic và failure dễ chẩn đoán**. Review này không dạy lại từng định nghĩa; nó buộc người đọc nối knowledge graph, giải thích trade-off và xử lý production case bằng evidence.

## Chapter Map

1. [01 — Test strategy và test pyramid trên iOS](01-test-strategy-va-test-pyramid-tren-ios.md)
2. [02 — XCTest và Swift Testing](02-xctest-va-swift-testing.md)
3. [03 — Mock, Stub, Fake và Spy](03-mock-stub-fake-va-spy.md)
4. [04 — Dependency Injection tạo testability](04-dependency-injection-tao-testability.md)
5. [05 — Async test không sleep](05-async-test-khong-sleep.md)
6. [06 — ViewModel testing theo state transition](06-viewmodel-testing-theo-state-transition.md)
7. [07 — Networking test với URLProtocol/fake transport](07-networking-test-voi-urlprotocol-fake-transport.md)
8. [08 — Repository integration test](08-repository-integration-test.md)
9. [09 — UI test cho critical user flow](09-ui-test-cho-critical-user-flow.md)
10. [10 — Flaky test: nguyên nhân và containment](10-flaky-test-nguyen-nhan-va-containment.md)
11. [11 — Snapshot testing: value và brittleness](11-snapshot-testing-value-va-brittleness.md)
12. [12 — TDD và design feedback](12-tdd-va-design-feedback.md)
13. [13 — Code coverage: tín hiệu và giới hạn](13-code-coverage-tin-hieu-va-gioi-han.md)
14. [14 — Regression test từ production incident](14-regression-test-tu-production-incident.md)

## Knowledge Map

```text
Test strategy và test pyramid trên iOS → XCTest và Swift Testing → Mock, Stub, Fake và Spy → Dependency Injection tạo testability → Async test không sleep → ViewModel testing theo state transition
        ↓
Ownership / State / Failure / Lifecycle
        ↓
Production evidence + interview reasoning
```

Mỗi edge phải trả lời “vì sao concept trước là prerequisite của concept sau?”. Nếu không trả lời được, quay lại chapter gốc thay vì học thuộc review.

## Phase Cheat Sheet

```text
Goal       → đặt confidence ở đúng boundary với test deterministic và failure dễ chẩn đoán
Mental     → Risk → observable behavior → controlled dependency → assertion/evidence → regression signal
Runtime    → Test runner và concurrency scheduler vẫn có timing; test không được dựa vào sleep hoặc order ngẫu nhiên.
Memory     → Test double và SUT cần teardown/lifetime rõ để phát hiện leak và tránh state rò giữa test.
Concurrency→ Await observable completion, kiểm soát clock/transport, và bảo vệ test khỏi data race/flakiness.
Evidence   → Swift Testing, XCTest, test plans, result bundles, sanitizer và performance metrics.
```

## Review Questions

1. Với Test strategy và test pyramid trên iOS, invariant, owner và evidence chính là gì?
2. Với XCTest và Swift Testing, invariant, owner và evidence chính là gì?
3. Với Mock, Stub, Fake và Spy, invariant, owner và evidence chính là gì?
4. Với Dependency Injection tạo testability, invariant, owner và evidence chính là gì?
5. Với Async test không sleep, invariant, owner và evidence chính là gì?
6. Với ViewModel testing theo state transition, invariant, owner và evidence chính là gì?
7. Với Networking test với URLProtocol/fake transport, invariant, owner và evidence chính là gì?
8. Với Repository integration test, invariant, owner và evidence chính là gì?
9. Với UI test cho critical user flow, invariant, owner và evidence chính là gì?
10. Với Flaky test: nguyên nhân và containment, invariant, owner và evidence chính là gì?
11. Với Snapshot testing: value và brittleness, invariant, owner và evidence chính là gì?
12. Với TDD và design feedback, invariant, owner và evidence chính là gì?
13. Với Code coverage: tín hiệu và giới hạn, invariant, owner và evidence chính là gì?
14. Với Regression test từ production incident, invariant, owner và evidence chính là gì?

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

- [Swift Testing](https://developer.apple.com/documentation/testing) — truy cập 2026-08-09.
- [XCTest](https://developer.apple.com/documentation/xctest) — truy cập 2026-08-09.
- [Testing and performance](https://developer.apple.com/documentation/technologyoverviews/testing-and-performance) — truy cập 2026-08-09.

## Completion Checklist

- [x] Phase summary, cheat sheet và knowledge map
- [x] Review/deep-dive questions
- [x] Coding exercises và debugging lab
- [x] Mini project/case study
- [x] Mock interview
- [x] Tất cả mandatory chapters có file complete
