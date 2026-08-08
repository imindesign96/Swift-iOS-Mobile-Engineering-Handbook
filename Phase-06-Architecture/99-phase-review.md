---
title: "Phase Review — Architecture"
phase: "Architecture"
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
  - "architecture"
---

# Phase Review — Architecture

## Phase Summary

Phase hoàn thành mục tiêu: **tạo dependency direction và ownership boundary vừa đủ cho complexity hiện tại**. Review này không dạy lại từng định nghĩa; nó buộc người đọc nối knowledge graph, giải thích trade-off và xử lý production case bằng evidence.

## Chapter Map

1. [01 — MVC và Massive ViewController](01-mvc-va-massive-viewcontroller.md)
2. [02 — MVVM và ranh giới trách nhiệm ViewModel](02-mvvm-va-ranh-gioi-trach-nhiem-viewmodel.md)
3. [03 — Coordinator và navigation ownership](03-coordinator-va-navigation-ownership.md)
4. [04 — Repository không chỉ là tên khác của API client](04-repository-khong-chi-la-ten-khac-cua-api-client.md)
5. [05 — Dependency Injection và constructor injection](05-dependency-injection-va-constructor-injection.md)
6. [06 — Service Locator và Singleton: trade-offs thật](06-service-locator-va-singleton-trade-offs-that.md)
7. [07 — UseCase/Interactor: khi nào đáng thêm một layer](07-usecase-interactor-khi-nao-ang-them-mot-layer.md)
8. [08 — Clean Architecture principles trên mobile](08-clean-architecture-principles-tren-mobile.md)
9. [09 — State machine thay cho Boolean explosion](09-state-machine-thay-cho-boolean-explosion.md)
10. [10 — SPM modularization và dependency direction](10-spm-modularization-va-dependency-direction.md)
11. [11 — Feature boundary và ngăn circular dependency](11-feature-boundary-va-ngan-circular-dependency.md)
12. [12 — Architecture Decision Record](12-architecture-decision-record.md)
13. [13 — Migration strategy không big-bang rewrite](13-migration-strategy-khong-big-bang-rewrite.md)
14. [14 — Refactoring Massive ViewController/Model/God Service](14-refactoring-massive-viewcontroller-model-god-service.md)

## Knowledge Map

```text
MVC và Massive ViewController → MVVM và ranh giới trách nhiệm ViewModel → Coordinator và navigation ownership → Repository không chỉ là tên khác của API client → Dependency Injection và constructor injection → Service Locator và Singleton: trade-offs thật
        ↓
Ownership / State / Failure / Lifecycle
        ↓
Production evidence + interview reasoning
```

Mỗi edge phải trả lời “vì sao concept trước là prerequisite của concept sau?”. Nếu không trả lời được, quay lại chapter gốc thay vì học thuộc review.

## Phase Cheat Sheet

```text
Goal       → tạo dependency direction và ownership boundary vừa đủ cho complexity hiện tại
Mental     → UI → application policy → repository boundary → remote/local implementation
Runtime    → Architecture không chạy thay framework; nó quyết định nơi state/work/lifetime được sở hữu và quan sát.
Memory     → Mỗi dependency phải có composition root và lifetime rõ; singleton vô tình biến lifetime thành toàn process.
Concurrency→ Isolation boundary nên đi cùng ownership boundary; đừng để nhiều layer cùng mutate một state.
Evidence   → Dependency graph, build metrics, ADR, code review và tests tại boundary.
```

## Review Questions

1. Với MVC và Massive ViewController, invariant, owner và evidence chính là gì?
2. Với MVVM và ranh giới trách nhiệm ViewModel, invariant, owner và evidence chính là gì?
3. Với Coordinator và navigation ownership, invariant, owner và evidence chính là gì?
4. Với Repository không chỉ là tên khác của API client, invariant, owner và evidence chính là gì?
5. Với Dependency Injection và constructor injection, invariant, owner và evidence chính là gì?
6. Với Service Locator và Singleton: trade-offs thật, invariant, owner và evidence chính là gì?
7. Với UseCase/Interactor: khi nào đáng thêm một layer, invariant, owner và evidence chính là gì?
8. Với Clean Architecture principles trên mobile, invariant, owner và evidence chính là gì?
9. Với State machine thay cho Boolean explosion, invariant, owner và evidence chính là gì?
10. Với SPM modularization và dependency direction, invariant, owner và evidence chính là gì?
11. Với Feature boundary và ngăn circular dependency, invariant, owner và evidence chính là gì?
12. Với Architecture Decision Record, invariant, owner và evidence chính là gì?
13. Với Migration strategy không big-bang rewrite, invariant, owner và evidence chính là gì?
14. Với Refactoring Massive ViewController/Model/God Service, invariant, owner và evidence chính là gì?

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

- [Swift Package Manager](https://www.swift.org/documentation/package-manager/) — truy cập 2026-08-09.
- [Organizing your code with local packages](https://developer.apple.com/documentation/xcode/organizing-your-code-with-local-packages) — truy cập 2026-08-09.
- [Swift API Design Guidelines](https://www.swift.org/documentation/api-design-guidelines/) — truy cập 2026-08-09.

## Completion Checklist

- [x] Phase summary, cheat sheet và knowledge map
- [x] Review/deep-dive questions
- [x] Coding exercises và debugging lab
- [x] Mini project/case study
- [x] Mock interview
- [x] Tất cả mandatory chapters có file complete
