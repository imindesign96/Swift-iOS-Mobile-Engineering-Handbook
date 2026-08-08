# Phase 04 — iOS Platform

Phase này tập trung vào mục tiêu: **đặt UI state và work đúng lifecycle trong UIKit lẫn SwiftUI**.

## Dependency map

```text
Event/state mutation → lifecycle/observation → UI description/layout → visible frame
      ↓
Runtime + Memory + Concurrency + Architecture
      ↓
Production evidence + Interview synthesis
```

## Learning outcomes

- Giải thích concept bằng behavior, constraint và trade-off.
- Xác định owner/state/failure/lifecycle cho Commerce flow.
- Dùng View Debugger, constraint logs, SwiftUI Instruments, Time Profiler và lifecycle logging. thay vì đoán root cause.
- Hoàn thành coding exercise, debugging lab và mock interview của phase.

## Chapters — Complete

- [01 — App lifecycle và scene lifecycle](01-app-lifecycle-va-scene-lifecycle.md)
- [02 — UIView: hierarchy, layout và drawing](02-uiview-hierarchy-layout-va-drawing.md)
- [03 — UIViewController lifecycle và ownership](03-uiviewcontroller-lifecycle-va-ownership.md)
- [04 — Navigation: push, present và coordinator boundary](04-navigation-push-present-va-coordinator-boundary.md)
- [05 — Auto Layout và intrinsic content size](05-auto-layout-va-intrinsic-content-size.md)
- [06 — Hugging, compression resistance và ambiguous layout](06-hugging-compression-resistance-va-ambiguous-layout.md)
- [07 — UITableView reuse và scrolling lifecycle](07-uitableview-reuse-va-scrolling-lifecycle.md)
- [08 — UICollectionView và compositional layout](08-uicollectionview-va-compositional-layout.md)
- [09 — Diffable Data Source và stable identity](09-diffable-data-source-va-stable-identity.md)
- [10 — Delegate pattern trong UIKit](10-delegate-pattern-trong-uikit.md)
- [11 — SwiftUI declarative mental model](11-swiftui-declarative-mental-model.md)
- [12 — State, Binding và source of truth](12-state-binding-va-source-of-truth.md)
- [13 — Observation và observable model ownership](13-observation-va-observable-model-ownership.md)
- [14 — Environment và dependency flow](14-environment-va-dependency-flow.md)
- [15 — View identity, ForEach và state lifetime](15-view-identity-foreach-va-state-lifetime.md)
- [16 — NavigationStack và typed navigation](16-navigationstack-va-typed-navigation.md)
- [17 — `.task`, cancellation và view lifecycle](17-task-cancellation-va-view-lifecycle.md)
- [18 — Animation, transaction và rendering cost](18-animation-transaction-va-rendering-cost.md)
- [19 — UIKit ↔ SwiftUI interoperability](19-uikit-to-swiftui-interoperability.md)
- [20 — Human Interface Guidelines, accessibility và adaptive UI](20-human-interface-guidelines-accessibility-va-adaptive-ui.md)
- [21 — App Extensions: Notification Service Extension và WidgetKit](21-app-extensions-notification-service-extension-va-widgetkit.md)
- [22 — CoreLocation: permission, accuracy, background và energy](22-corelocation-permission-accuracy-background-va-energy.md)
- [23 — Universal Links: AASA, routing, fallback và security](23-universal-links-aasa-routing-fallback-va-security.md)
- [24 — WKWebView bridge: Cookie, LocalStorage và native-web data contract](24-wkwebview-bridge-cookie-localstorage-va-native-web-data-contract.md)
- [99 — Phase Review: iOS Platform](99-phase-review.md)

## Quality gate

Toàn bộ chapter có front matter `status: complete`, production case, debugging evidence, interview questions, exercises, cheat sheet, references và links nội bộ hợp lệ.
