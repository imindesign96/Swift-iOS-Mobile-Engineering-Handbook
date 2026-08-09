# Cross-reference Index

## Production symptom → knowledge path

| Symptom | Start here | Continue with |
|---|---|---|
| ViewController không `deinit` | [ARC & ownership](Phase-02-Memory-Runtime/04-arc-va-ownership-graph.md) | Closure capture → delegate/timer/task lifetime → Memory Graph |
| UI freeze / hang | [MainActor](Phase-03-Concurrency/09-mainactor-global-actor-va-ui-isolation.md) | Time Profiler → decoding/image/disk work → responsiveness |
| SwiftUI không update đúng | [State & Binding](Phase-04-iOS-Platform/12-state-binding-va-source-of-truth.md) | Observation → identity → task lifecycle |
| Duplicate API | [Task lifetime](Phase-03-Concurrency/13-task-lifetime-qua-screen-lifecycle.md) | Pagination → reentrancy → state machine/idempotency |
| Token refresh race | [Single-flight refresh](Phase-05-Networking/10-single-flight-token-refresh.md) | Actor reentrancy → retry → Keychain boundary |
| Scroll lag | [Image diagnostics](Phase-09-Production/11-image-decoding-downsampling-va-cache-budget.md) | Reuse → prefetch → rendering cost |
| Stale data | [Persistent cache](Phase-07-Persistence/11-persistent-cache-va-invalidation.md) | Repository → HTTP cache → synchronization |
| Previous account data | [Account isolation](Phase-07-Persistence/14-logout-login-va-data-isolation-giua-account.md) | Keychain → repository/cache reset → regression test |
| Rare concurrency crash | [Strict concurrency](Phase-03-Concurrency/10-sendable-at-sendable-va-strict-concurrency.md) | Actor isolation → reentrancy → production correlation |
| OS kill không crash log | [Memory pressure](Phase-09-Production/06-memory-pressure-va-os-termination.md) | Allocations → image/cache budget → Organizer metrics |
| Web/native session lệch | [WKWebView bridge](Phase-04-iOS-Platform/24-wkwebview-bridge-cookie-localstorage-va-native-web-data-contract.md) | Cookie store → LocalStorage origin → bridge contract → logout regression |
| Deep link không mở app | [Universal Links](Phase-04-iOS-Platform/23-universal-links-aasa-routing-fallback-va-security.md) | AASA/entitlement → scene delivery → typed route → security fallback |
| E2E flaky trên CI | [E2E automation](Phase-08-Testing/15-e2e-automation-voi-xcuitest-fixtures-stability-va-ci.md) | Fixture/identifier → semantic wait → xcresult → flake taxonomy |
| Release/signing không ổn định | [iOS CI/CD](Phase-09-Production/19-ios-ci-cd-voi-bitrise-va-fastlane.md) | Toolchain pin → tests → readonly signing → immutable artifact |
| Team chậm nhưng không rõ bottleneck | [Developer productivity](Phase-09-Production/20-developer-productivity-metrics-va-data-driven-improvement.md) | Value stream → DORA/DevEx baseline → experiment → guardrail |
| Purchase thành công nhưng chưa mở quyền | [StoreKit 2](Phase-04-iOS-Platform/26-storekit-2-iap-subscription-verification-server-contract.md) | Verification → entitlement reconciliation → server notification/ledger → refund |
| APNs trả 200 nhưng user không thấy | [APNs end-to-end](Phase-04-iOS-Platform/27-apns-push-notification-end-to-end.md) | Token/environment → topic/push type → permission/presentation → route telemetry |
| Chuỗi bị cắt / sai plural / RTL | [Localization](Phase-04-iOS-Platform/28-localization-string-catalog-pluralization-rtl-va-testing.md) | String Catalog → locale/time zone → adaptive layout → localization test matrix |
| Live Activity stale hoặc không kết thúc | [App Intents & ActivityKit](Phase-04-iOS-Platform/29-app-intents-shortcuts-live-activities-va-activitykit.md) | Token rotation → version ordering → stale/end policy → account isolation |
| Camera giật hoặc memory tăng | [AVFoundation](Phase-04-iOS-Platform/30-avfoundation-camera-media-pipeline.md) | Session queue → buffer backpressure → orientation/audio → device profiling |
| BLE reconnect tạo duplicate command | [CoreBluetooth & Core NFC](Phase-04-iOS-Platform/31-corebluetooth-va-corenfc-device-connectivity.md) | State machine → framing/ack → idempotency → restoration/hardware test |
| Map tự nhảy / search result cũ | [MapKit](Phase-04-iOS-Platform/32-mapkit-search-directions-camera-va-location-experience.md) | Camera owner → debounce/cancel/generation → route staleness |
| Health sample mất hoặc đếm đôi | [HealthKit](Phase-04-iOS-Platform/33-healthkit-authorization-query-background-delivery-va-privacy.md) | Authorization privacy → observer/anchor → atomic checkpoint → source aggregation |
| CloudKit mất edit / lộ account cũ | [CloudKit](Phase-04-iOS-Platform/34-cloudkit-sync-account-conflict-va-offline-boundary.md) | Local outbox → conflict policy → account partition → engine state |
| App Store reject hoặc không thể rollback | [App Store release engineering](Phase-09-Production/21-app-store-release-engineering-signing-privacy-review-va-rollback.md) | Signing/entitlements → privacy manifest → TestFlight/review → pause/kill switch/fix-forward |
| Background job không chạy hoặc upload mất | [BackgroundTasks & background URLSession](Phase-09-Production/22-bgtaskscheduler-background-urlsession-energy-va-debugging.md) | Mechanism selection → expiration/checkpoint → persistent transfer identity → device evidence |

## Canonical Phase Reviews

- [Swift Foundation review](Phase-01-Swift-Foundation/99-phase-review.md)
- [Memory & Runtime review](Phase-02-Memory-Runtime/99-phase-review.md)
- [Concurrency review](Phase-03-Concurrency/99-phase-review.md)
- [iOS Platform review](Phase-04-iOS-Platform/99-phase-review.md)
- [Networking review](Phase-05-Networking/99-phase-review.md)
- [Architecture review](Phase-06-Architecture/99-phase-review.md)
- [Persistence review](Phase-07-Persistence/99-phase-review.md)
- [Testing review](Phase-08-Testing/99-phase-review.md)
- [Production review](Phase-09-Production/99-phase-review.md)
- [Mobile System Design review](Phase-10-Mobile-System-Design/99-phase-review.md)
- [Global Interview review](Phase-11-Interview/99-phase-review.md)

## Full coverage

Xem [Handbook Coverage Matrix](HANDBOOK_COVERAGE.md) để tra toàn bộ 208 chapter; xem [Professional Skills Matrix](PROFESSIONAL_SKILLS_MATRIX.md) để đối chiếu 13 yêu cầu năng lực tiếng Nhật.
