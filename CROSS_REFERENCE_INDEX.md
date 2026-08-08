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

Xem [Handbook Coverage Matrix](HANDBOOK_COVERAGE.md) để tra toàn bộ 183 chapter và các chiều runtime/memory/concurrency/production/interview.
