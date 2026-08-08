---
title: "Phase Review — iOS Platform"
phase: "iOS Platform"
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
  - "ios-platform"
---

# Phase Review — iOS Platform

## Phase Summary

Phase hoàn thành mục tiêu: **đặt UI state và work đúng lifecycle trong UIKit lẫn SwiftUI**. Review này không dạy lại từng định nghĩa; nó buộc người đọc nối knowledge graph, giải thích trade-off và xử lý production case bằng evidence.

## Chapter Map

1. [01 — App lifecycle và scene lifecycle](01-app-lifecycle-va-scene-lifecycle.md)
2. [02 — UIView: hierarchy, layout và drawing](02-uiview-hierarchy-layout-va-drawing.md)
3. [03 — UIViewController lifecycle và ownership](03-uiviewcontroller-lifecycle-va-ownership.md)
4. [04 — Navigation: push, present và coordinator boundary](04-navigation-push-present-va-coordinator-boundary.md)
5. [05 — Auto Layout và intrinsic content size](05-auto-layout-va-intrinsic-content-size.md)
6. [06 — Hugging, compression resistance và ambiguous layout](06-hugging-compression-resistance-va-ambiguous-layout.md)
7. [07 — UITableView reuse và scrolling lifecycle](07-uitableview-reuse-va-scrolling-lifecycle.md)
8. [08 — UICollectionView và compositional layout](08-uicollectionview-va-compositional-layout.md)
9. [09 — Diffable Data Source và stable identity](09-diffable-data-source-va-stable-identity.md)
10. [10 — Delegate pattern trong UIKit](10-delegate-pattern-trong-uikit.md)
11. [11 — SwiftUI declarative mental model](11-swiftui-declarative-mental-model.md)
12. [12 — State, Binding và source of truth](12-state-binding-va-source-of-truth.md)
13. [13 — Observation và observable model ownership](13-observation-va-observable-model-ownership.md)
14. [14 — Environment và dependency flow](14-environment-va-dependency-flow.md)
15. [15 — View identity, ForEach và state lifetime](15-view-identity-foreach-va-state-lifetime.md)
16. [16 — NavigationStack và typed navigation](16-navigationstack-va-typed-navigation.md)
17. [17 — `.task`, cancellation và view lifecycle](17-task-cancellation-va-view-lifecycle.md)
18. [18 — Animation, transaction và rendering cost](18-animation-transaction-va-rendering-cost.md)
19. [19 — UIKit ↔ SwiftUI interoperability](19-uikit-to-swiftui-interoperability.md)
20. [20 — Human Interface Guidelines, accessibility và adaptive UI](20-human-interface-guidelines-accessibility-va-adaptive-ui.md)
21. [21 — App Extensions: Notification Service Extension và WidgetKit](21-app-extensions-notification-service-extension-va-widgetkit.md)
22. [22 — CoreLocation: permission, accuracy, background và energy](22-corelocation-permission-accuracy-background-va-energy.md)
23. [23 — Universal Links: AASA, routing, fallback và security](23-universal-links-aasa-routing-fallback-va-security.md)
24. [24 — WKWebView bridge: Cookie, LocalStorage và native-web data contract](24-wkwebview-bridge-cookie-localstorage-va-native-web-data-contract.md)
25. [25 — Human Interface Guidelines in practice: navigation, modality, controls và feedback](25-human-interface-guidelines-in-practice-navigation-modality-controls-va-feedback.md)

## Knowledge Map

```text
App lifecycle và scene lifecycle → UIView: hierarchy, layout và drawing → UIViewController lifecycle và ownership → Navigation: push, present và coordinator boundary → Auto Layout và intrinsic content size → Hugging, compression resistance và ambiguous layout
        ↓
Ownership / State / Failure / Lifecycle
        ↓
Production evidence + interview reasoning
```

Mỗi edge phải trả lời “vì sao concept trước là prerequisite của concept sau?”. Nếu không trả lời được, quay lại chapter gốc thay vì học thuộc review.

## Phase Cheat Sheet

```text
Goal       → đặt UI state và work đúng lifecycle trong UIKit lẫn SwiftUI
Mental     → Event/state mutation → lifecycle/observation → UI description/layout → visible frame
Runtime    → UIKit vận hành qua object lifecycle; SwiftUI đánh giá description và reconcile phần UI bị ảnh hưởng, không đơn giản là vẽ lại mọi thứ.
Memory     → Controller/model/task ownership phải khớp screen lifetime; cell/view reuse không phải object mới cho mỗi item.
Concurrency→ UI state được cô lập phù hợp; work nặng không nên bị giữ trên MainActor chỉ vì kết quả cuối cập nhật UI.
Evidence   → View Debugger, constraint logs, SwiftUI Instruments, Time Profiler và lifecycle logging.
```

## Review Questions

1. Với App lifecycle và scene lifecycle, invariant, owner và evidence chính là gì?
2. Với UIView: hierarchy, layout và drawing, invariant, owner và evidence chính là gì?
3. Với UIViewController lifecycle và ownership, invariant, owner và evidence chính là gì?
4. Với Navigation: push, present và coordinator boundary, invariant, owner và evidence chính là gì?
5. Với Auto Layout và intrinsic content size, invariant, owner và evidence chính là gì?
6. Với Hugging, compression resistance và ambiguous layout, invariant, owner và evidence chính là gì?
7. Với UITableView reuse và scrolling lifecycle, invariant, owner và evidence chính là gì?
8. Với UICollectionView và compositional layout, invariant, owner và evidence chính là gì?
9. Với Diffable Data Source và stable identity, invariant, owner và evidence chính là gì?
10. Với Delegate pattern trong UIKit, invariant, owner và evidence chính là gì?
11. Với SwiftUI declarative mental model, invariant, owner và evidence chính là gì?
12. Với State, Binding và source of truth, invariant, owner và evidence chính là gì?
13. Với Observation và observable model ownership, invariant, owner và evidence chính là gì?
14. Với Environment và dependency flow, invariant, owner và evidence chính là gì?
15. Với View identity, ForEach và state lifetime, invariant, owner và evidence chính là gì?
16. Với NavigationStack và typed navigation, invariant, owner và evidence chính là gì?
17. Với `.task`, cancellation và view lifecycle, invariant, owner và evidence chính là gì?
18. Với Animation, transaction và rendering cost, invariant, owner và evidence chính là gì?
19. Với UIKit ↔ SwiftUI interoperability, invariant, owner và evidence chính là gì?
20. Với Human Interface Guidelines, accessibility và adaptive UI, invariant, owner và evidence chính là gì?
21. Với App Extensions: Notification Service Extension và WidgetKit, invariant, owner và evidence chính là gì?
22. Với CoreLocation: permission, accuracy, background và energy, invariant, owner và evidence chính là gì?
23. Với Universal Links: AASA, routing, fallback và security, invariant, owner và evidence chính là gì?
24. Với WKWebView bridge: Cookie, LocalStorage và native-web data contract, invariant, owner và evidence chính là gì?
25. Với Human Interface Guidelines in practice: navigation, modality, controls và feedback, invariant, owner và evidence chính là gì?

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

- [UIKit](https://developer.apple.com/documentation/uikit) — truy cập 2026-08-09.
- [SwiftUI](https://developer.apple.com/documentation/swiftui) — truy cập 2026-08-09.
- [Observation](https://developer.apple.com/documentation/observation) — truy cập 2026-08-09.

## Completion Checklist

- [x] Phase summary, cheat sheet và knowledge map
- [x] Review/deep-dive questions
- [x] Coding exercises và debugging lab
- [x] Mini project/case study
- [x] Mock interview
- [x] Tất cả mandatory chapters có file complete
