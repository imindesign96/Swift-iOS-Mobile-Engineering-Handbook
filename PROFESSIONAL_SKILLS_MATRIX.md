# Professional Skills Coverage Matrix

> Audit ngày 2026-08-09; đối chiếu nguyên văn 13 yêu cầu năng lực với 11 Phase của handbook.

## Kết quả

| Yêu cầu | Trạng thái | Chapter canonical | Evidence scope |
|---|---|---|---|
| ネイティブ機能の深い理解（Notification Service Extension / Widget / CoreLocation / Universal Link など） | ✅ Đã bổ sung | [App Extensions: Notification Service Extension và WidgetKit](Phase-04-iOS-Platform/21-app-extensions-notification-service-extension-va-widgetkit.md)<br>[CoreLocation: permission, accuracy, background và energy](Phase-04-iOS-Platform/22-corelocation-permission-accuracy-background-va-energy.md)<br>[Universal Links: AASA, routing, fallback và security](Phase-04-iOS-Platform/23-universal-links-aasa-routing-fallback-va-security.md) | Extension lifecycle/budget; notification fallback; Widget timeline; permission/accuracy/energy; AASA/routing/security. |
| ユーザーインターフェースガイドラインの深い理解 | ✅ Đã bổ sung | [Human Interface Guidelines, accessibility và adaptive UI](Phase-04-iOS-Platform/20-human-interface-guidelines-accessibility-va-adaptive-ui.md) | HIG, adaptive layout, Dynamic Type, VoiceOver, accessibility audit và device-trait matrix. |
| アーキテクチャ設計に関する深い知識 | ✅ Đã có sâu | [MVC và Massive ViewController](Phase-06-Architecture/01-mvc-va-massive-viewcontroller.md)<br>[MVVM và ranh giới trách nhiệm ViewModel](Phase-06-Architecture/02-mvvm-va-ranh-gioi-trach-nhiem-viewmodel.md)<br>[Clean Architecture principles trên mobile](Phase-06-Architecture/08-clean-architecture-principles-tren-mobile.md)<br>[SPM modularization và dependency direction](Phase-06-Architecture/10-spm-modularization-va-dependency-direction.md)<br>[Architecture Decision Record](Phase-06-Architecture/12-architecture-decision-record.md) | Phase 06 cover responsibility, dependency direction, state, modules, ADR và incremental migration; Phase 10 áp dụng ở system scale. |
| WKWebViewを用いたWebサイトとのデータ連携経験（CookieやLocalStorageを含む） | ✅ Đã bổ sung | [WKWebView bridge: Cookie, LocalStorage và native-web data contract](Phase-04-iOS-Platform/24-wkwebview-bridge-cookie-localstorage-va-native-web-data-contract.md) | WKWebsiteDataStore, WKHTTPCookieStore, origin-scoped LocalStorage, versioned bridge, ownership và navigation security. |
| Reactive programmingの経験 | ✅ Đã bổ sung | [Reactive Programming với Combine: stream, demand, scheduling và cancellation](Phase-03-Concurrency/16-reactive-programming-voi-combine-stream-demand-scheduling-va-cancellation.md) | Combine Publisher/Subscriber/Subscription, demand, operators, scheduler, cancellation và bridge sang async/await. |
| E2Eテストの自動化経験 | ✅ Đã bổ sung | [E2E automation với XCUITest: fixtures, stability và CI](Phase-08-Testing/15-e2e-automation-voi-xcuitest-fixtures-stability-va-ci.md) | XCUITest fixtures, accessibility identifiers, deterministic wait, xcresult evidence, sharding và flake policy. |
| CI/CD（Bitrise, fastlane等）を用いた自動化経験 | ✅ Đã bổ sung | [iOS CI/CD với Bitrise và fastlane](Phase-09-Production/19-ios-ci-cd-voi-bitrise-va-fastlane.md) | Bitrise workflows, fastlane verify/release lanes, signing/secrets, artifacts, quality gates và release safety. |
| SwiftUI 経験 | ✅ Đã có sâu | [SwiftUI declarative mental model](Phase-04-iOS-Platform/11-swiftui-declarative-mental-model.md)<br>[State, Binding và source of truth](Phase-04-iOS-Platform/12-state-binding-va-source-of-truth.md)<br>[Observation và observable model ownership](Phase-04-iOS-Platform/13-observation-va-observable-model-ownership.md)<br>[NavigationStack và typed navigation](Phase-04-iOS-Platform/16-navigationstack-va-typed-navigation.md)<br>[UIKit ↔ SwiftUI interoperability](Phase-04-iOS-Platform/19-uikit-to-swiftui-interoperability.md) | Phase 04 cover mental model, state/observation/environment/identity/navigation/task/animation/interoperability; Phase 11 review. |
| サーバーサイド、フロントエンドなどandroid、iOS以外の開発知識 | ✅ Đã bổ sung | [Cross-platform collaboration: backend, web, Android và API contracts](Phase-10-Mobile-System-Design/18-cross-platform-collaboration-backend-web-android-va-api-contracts.md) | Backend/web/Android lifecycle differences, OpenAPI schema, error/auth/time/money/idempotency, compatibility và rollout. |
| マネジメントまたは技術リード経験 | ✅ Đã bổ sung | [Engineering management và technical leadership](Phase-11-Interview/18-engineering-management-va-technical-leadership.md) | Role/decision rights, delegation, ADR, mentoring, stakeholder/incident operating system và team-level outcomes. |
| 開発生産性の可視化やデータドリブンな改善経験 | ✅ Đã bổ sung | [Developer productivity metrics và data-driven improvement](Phase-09-Production/20-developer-productivity-metrics-va-data-driven-improvement.md) | DORA throughput/instability, mobile CI/DevEx metrics, anti-gaming rules và hypothesis-driven improvement loop. |
| 社外勉強会や登壇、コミュニティ活動経験 | ✅ Đã bổ sung | [Technical speaking, study groups và community contribution](Phase-11-Interview/19-technical-speaking-study-groups-va-community-contribution.md) | Audience/outcomes, proposal, rehearsal, confidentiality, study-group operation, feedback và reusable artifacts. |
| OSSのリリース・コントリビュート経験 | ✅ Đã bổ sung | [OSS contribution, release và maintainer workflow](Phase-11-Interview/20-oss-contribution-release-va-maintainer-workflow.md) | Governance-first contribution, CI/API compatibility, SemVer, changelog, provenance, security và maintainer workflow. |

## Cách đọc trạng thái

- **Đã có sâu:** catalog trước audit đã có nhiều chapter canonical, production case, exercises và Phase Review.
- **Đã bổ sung:** audit phát hiện coverage thiếu hoặc chỉ gián tiếp; handbook đã thêm chapter chuyên sâu, code, failure modes, debugging evidence, interview prompts và references chính thức.
- Một năng lực chỉ được tính khi chapter có `status: complete`, đủ quality-gate sections và vượt content floor của validator.

## Coverage distribution

```text
Phase 03  Reactive Programming
Phase 04  HIG · App Extensions · CoreLocation · Universal Links · WKWebView · SwiftUI
Phase 06  Architecture foundations and migration
Phase 08  E2E automation
Phase 09  CI/CD · Developer Productivity
Phase 10  Cross-platform/API contracts · system-scale architecture
Phase 11  Leadership · Community · OSS · interview synthesis
```
