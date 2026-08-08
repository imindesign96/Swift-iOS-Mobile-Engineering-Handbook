# Cross-reference Index

Index ánh xạ từ câu hỏi/symptom về knowledge area. Chỉ chapter đã hoàn chỉnh mới có link; mục planned ghi Phase để không tạo broken link.

## Production symptom → knowledge

| Symptom | Knowledge cần kiểm tra | Primary evidence |
|---|---|---|
| ViewController không `deinit` | Phase 02: ARC, closure capture, delegate, observer, task lifetime; Phase 06: Coordinator | `deinit` log, Memory Graph, Leaks |
| Memory tăng khi scroll | Phase 02: pressure vs leak; Phase 09: image decode/cache budget | Allocations, VM Tracker, image dimensions |
| UI freeze | Phase 03: MainActor; Phase 09: CPU/layout/image/disk | Time Profiler, hang stack, signpost |
| SwiftUI không update | Phase 04: state ownership, Observation, identity | state transition log, Instruments SwiftUI diagnostics |
| SwiftUI row mất state | Phase 04: ForEach/stable identity | diff input, identity log |
| API bị gọi lặp | Phase 03: Task lifecycle/reentrancy; Phase 05: cancellation/coalescing | request ID, task lifecycle log |
| Random logout khi token hết hạn | Phase 05: single-flight refresh; Phase 03: actor logical race | refresh correlation ID, 401 timeline |
| Double-tap tạo hai order | Phase 05: idempotency; Phase 06: state machine; Phase 10: Checkout | request/idempotency key, state transitions |
| Dữ liệu account cũ sau login | Phase 07: data partition/source of truth; Phase 05: auth lifecycle | account-scoped store keys, cache trace |
| Cache stale | Phase 05/07: HTTP/local cache, TTL, invalidation, sync | response headers, cache metadata |
| Wi‑Fi chạy, cellular lỗi | Phase 05/09: reachability assumption, DNS/TLS/size/timeout | URLSession metrics, structured network logs |
| Crash hiếm ở traffic lớn | Phase 03: race/ordering; Phase 09: crash clustering/symbolication | symbolicated stack, breadcrumbs, cohort |
| App bị kill không có crash thường | Phase 09: memory pressure/watchdog/background | MetricKit/organizer diagnostics, memory trend |
| Background upload gián đoạn | Phase 04 lifecycle; Phase 05 URLSession; Phase 09 background execution | background session events, task persistence |

## Concept → dependency chain

| Concept | Prerequisite chain | Used later |
|---|---|---|
| Optional | Type system | Codable, networking, persistence, UI state |
| Value semantics | Struct/class | CoW, Sendable, state modeling, performance |
| ARC | Reference semantics | closure capture, UIKit lifetime, Coordinator, cache |
| Protocol | Function/type system | Generics, DI, Repository, tests, modularization |
| `some` / `any` | Protocol + generics | SwiftUI, API design, type erasure |
| Suspension | Function + closure | Task, cancellation, actor reentrancy |
| Actor isolation | async/await + Task | auth refresh, cache, analytics, offline sync |
| Source of Truth | value/reference + state | SwiftUI, Repository, offline-first, conflict resolution |
| Idempotency | HTTP + state machine | payment, retry, offline queue |

## Completed chapter index

| Problem | Chapter | Interview surfaces |
|---|---|---|
| Swift source trở thành app chạy được thế nào? | [01 — Một chương trình Swift chạy như thế nào?](Phase-01-Swift-Foundation/01-how-a-swift-program-runs.md) | compile pipeline, `@main`, Debug vs Release, compiler vs language mode |
| Giá/unit cùng là `Int` nhưng bị dùng nhầm | [02 — `let`, `var`, type inference và type safety](Phase-01-Swift-Foundation/02-let-var-type-inference-and-type-safety.md) | let vs var, inference, strong typing, domain wrapper |
| Malformed deep link gây force-unwrap crash | [03 — Optional và nil safety](Phase-01-Swift-Foundation/03-optionals-and-nil-safety.md) | Optional, guard/if let, IUO, absence vs failure |
