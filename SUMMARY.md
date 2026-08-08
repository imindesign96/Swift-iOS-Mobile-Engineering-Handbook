# SUMMARY — Knowledge Map & Progress

Ký hiệu:

- ✅ chapter hoàn chỉnh, tiêu đề là liên kết;
- ◻ planned chapter, chưa tạo file cho đến khi vượt quality gate;
- `99` là phase review, chỉ hoàn chỉnh khi toàn phase hoàn chỉnh.

## Phase 01 — Swift Foundation

- ✅ [01 — Một chương trình Swift chạy như thế nào?](Phase-01-Swift-Foundation/01-how-a-swift-program-runs.md)
- ✅ [02 — `let`, `var`, type inference và strong typing](Phase-01-Swift-Foundation/02-let-var-type-inference-and-type-safety.md)
- ✅ [03 — Optional và nil safety](Phase-01-Swift-Foundation/03-optionals-and-nil-safety.md)
- ◻ 04 — Control flow, `switch` và pattern matching
- ◻ 05 — Function, parameter label và method
- ◻ 06 — Closure, capture và `@escaping`
- ◻ 07 — Enum và state modeling
- ◻ 08 — Struct, class, equality và identity
- ◻ 09 — Value semantics vs reference semantics
- ◻ 10 — Property, initialization và access control
- ◻ 11 — Extension và tổ chức capability
- ◻ 12 — Protocol và protocol-oriented design
- ◻ 13 — Generics, constraint và `associatedtype`
- ◻ 14 — `some` vs `any`: opaque và existential types
- ◻ 15 — Error handling, `throws` và `Result`
- ◻ 16 — Array, Set, Dictionary và collection semantics
- ◻ 17 — String, Unicode và indexing
- ◻ 18 — Codable fundamentals
- ◻ 99 — Phase Review: Swift Foundation

## Phase 02 — Memory & Runtime

- ◻ 01 — Stack/Heap: mental model hữu ích và giới hạn
- ◻ 02 — Copy, value semantics và mutation
- ◻ 03 — Copy-on-Write: khi copy chưa thực sự copy
- ◻ 04 — ARC và ownership graph
- ◻ 05 — `strong`, `weak`, `unowned` theo lifetime
- ◻ 06 — Closure capture, escaping và capture list
- ◻ 07 — Vì sao ViewController không `deinit`?
- ◻ 08 — Delegate, timer, observer và task lifetime
- ◻ 09 — `deinit` và lifecycle diagnostics
- ◻ 10 — Memory Graph, Leaks và Allocations
- ◻ 11 — Leak vs memory pressure
- ◻ 99 — Phase Review: Memory & Runtime

## Phase 03 — Concurrency

- ◻ 01 — Thread, shared mutable state và data race
- ◻ 02 — GCD: serial/concurrent, sync/async và QoS
- ◻ 03 — Deadlock, barrier, group, semaphore và OperationQueue
- ◻ 04 — Điều gì thực sự xảy ra tại `await`?
- ◻ 05 — Task và structured concurrency
- ◻ 06 — `async let` và TaskGroup
- ◻ 07 — Cancellation là cooperative contract
- ◻ 08 — Actor và actor isolation
- ◻ 09 — MainActor, global actor và UI isolation
- ◻ 10 — Sendable, `@Sendable` và strict concurrency
- ◻ 11 — Actor reentrancy và logical race
- ◻ 12 — Structured vs unstructured vs detached task
- ◻ 13 — Task lifetime qua screen lifecycle
- ◻ 14 — Migration từ callback/GCD sang async/await
- ◻ 15 — Priority inversion, thread explosion và performance
- ◻ 99 — Phase Review: Concurrency

## Phase 04 — iOS Platform

- ◻ 01 — App lifecycle và scene lifecycle
- ◻ 02 — UIView: hierarchy, layout và drawing
- ◻ 03 — UIViewController lifecycle và ownership
- ◻ 04 — Navigation: push, present và coordinator boundary
- ◻ 05 — Auto Layout và intrinsic content size
- ◻ 06 — Hugging, compression resistance và ambiguous layout
- ◻ 07 — UITableView reuse và scrolling lifecycle
- ◻ 08 — UICollectionView và compositional layout
- ◻ 09 — Diffable Data Source và stable identity
- ◻ 10 — Delegate pattern trong UIKit
- ◻ 11 — SwiftUI declarative mental model
- ◻ 12 — State, Binding và source of truth
- ◻ 13 — Observation và observable model ownership
- ◻ 14 — Environment và dependency flow
- ◻ 15 — View identity, ForEach và state lifetime
- ◻ 16 — NavigationStack và typed navigation
- ◻ 17 — `.task`, cancellation và view lifecycle
- ◻ 18 — Animation, transaction và rendering cost
- ◻ 19 — UIKit ↔ SwiftUI interoperability
- ◻ 99 — Phase Review: iOS Platform

## Phase 05 — Networking

- ◻ 01 — Một request từ iPhone đến server đi như thế nào?
- ◻ 02 — HTTP methods, headers, status và idempotency
- ◻ 03 — URLSession, URLRequest và response lifecycle
- ◻ 04 — Codable, CodingKeys và resilient decoding
- ◻ 05 — API client và Endpoint abstraction
- ◻ 06 — Error taxonomy: transport/HTTP/decode/business
- ◻ 07 — Timeout, retry, backoff và jitter
- ◻ 08 — Cancellation từ screen đến URLSession
- ◻ 09 — Access token, refresh token và Keychain boundary
- ◻ 10 — Single-flight token refresh
- ◻ 11 — Pagination, prefetch và duplicate requests
- ◻ 12 — HTTP caching, ETag và cache policy
- ◻ 13 — Kết hợp remote cache và offline data
- ◻ 14 — ATS, TLS và certificate pinning trade-offs
- ◻ 15 — Network diagnostics và privacy-aware logging
- ◻ 99 — Phase Review: Networking

## Phase 06 — Architecture

- ◻ 01 — MVC và Massive ViewController
- ◻ 02 — MVVM và ranh giới trách nhiệm ViewModel
- ◻ 03 — Coordinator và navigation ownership
- ◻ 04 — Repository không chỉ là tên khác của API client
- ◻ 05 — Dependency Injection và constructor injection
- ◻ 06 — Service Locator và Singleton: trade-offs thật
- ◻ 07 — UseCase/Interactor: khi nào đáng thêm một layer
- ◻ 08 — Clean Architecture principles trên mobile
- ◻ 09 — State machine thay cho Boolean explosion
- ◻ 10 — SPM modularization và dependency direction
- ◻ 11 — Feature boundary và ngăn circular dependency
- ◻ 12 — Architecture Decision Record
- ◻ 13 — Migration strategy không big-bang rewrite
- ◻ 14 — Refactoring Massive ViewController/Model/God Service
- ◻ 99 — Phase Review: Architecture

## Phase 07 — Persistence

- ◻ 01 — Chọn storage theo data, lifetime và security
- ◻ 02 — UserDefaults: preference, không phải database
- ◻ 03 — Keychain và sensitive data lifecycle
- ◻ 04 — FileManager, atomic write và file coordination
- ◻ 05 — SQLite concepts, schema và transaction
- ◻ 06 — Core Data mental model
- ◻ 07 — Managed Object Context và Core Data concurrency
- ◻ 08 — SwiftData và ranh giới availability
- ◻ 09 — SwiftData vs Core Data theo constraint
- ◻ 10 — Migration strategy và rollback thinking
- ◻ 11 — Persistent cache và invalidation
- ◻ 12 — Offline-first synchronization
- ◻ 13 — Conflict detection và resolution
- ◻ 14 — Logout/login và data isolation giữa account
- ◻ 99 — Phase Review: Persistence

## Phase 08 — Testing

- ◻ 01 — Test strategy và test pyramid trên iOS
- ◻ 02 — XCTest và Swift Testing
- ◻ 03 — Mock, Stub, Fake và Spy
- ◻ 04 — Dependency Injection tạo testability
- ◻ 05 — Async test không sleep
- ◻ 06 — ViewModel testing theo state transition
- ◻ 07 — Networking test với URLProtocol/fake transport
- ◻ 08 — Repository integration test
- ◻ 09 — UI test cho critical user flow
- ◻ 10 — Flaky test: nguyên nhân và containment
- ◻ 11 — Snapshot testing: value và brittleness
- ◻ 12 — TDD và design feedback
- ◻ 13 — Code coverage: tín hiệu và giới hạn
- ◻ 14 — Regression test từ production incident
- ◻ 99 — Phase Review: Testing

## Phase 09 — Production

- ◻ 01 — Structured, privacy-aware logging
- ◻ 02 — Crash report và symbolication
- ◻ 03 — EXC_BAD_ACCESS, fatal error và index out of range
- ◻ 04 — Hang, watchdog và stack evidence
- ◻ 05 — Memory leak investigation
- ◻ 06 — Memory pressure và OS termination
- ◻ 07 — Instruments workflow: measure before fix
- ◻ 08 — Time Profiler và hot call tree
- ◻ 09 — Allocations, Leaks và Memory Graph
- ◻ 10 — Scroll hitch, layout và rendering diagnostics
- ◻ 11 — Image decoding, downsampling và cache budget
- ◻ 12 — App launch: pre-main/post-main
- ◻ 13 — Battery và energy diagnostics
- ◻ 14 — Network-only production failure
- ◻ 15 — Release-only và device-specific bugs
- ◻ 16 — Background execution và interrupted work
- ◻ 17 — Concurrency incidents ở quy mô session lớn
- ◻ 18 — Observability, SLO và incident response
- ◻ 99 — Phase Review: Production

## Phase 10 — Mobile System Design

- ◻ 01 — Framework phỏng vấn Mobile System Design
- ◻ 02 — Image Loader production-grade
- ◻ 03 — Paginated Feed
- ◻ 04 — Chat với ordering và offline queue
- ◻ 05 — Download Manager hỗ trợ resume/background
- ◻ 06 — Offline-first app và conflict resolution
- ◻ 07 — Video Feed và resource budgeting
- ◻ 08 — Authentication system và single refresh
- ◻ 09 — Notification routing
- ◻ 10 — Analytics SDK privacy-aware
- ◻ 11 — Feature Flag system
- ◻ 12 — Networking SDK
- ◻ 13 — Caching layer
- ◻ 14 — Search autocomplete
- ◻ 15 — Modular architecture cho nhiều team
- ◻ 16 — UIKit → SwiftUI migration
- ◻ 17 — Commerce Checkout state machine
- ◻ 99 — Phase Review: Mobile System Design

## Phase 11 — Interview

- ◻ 01 — Swift Core review
- ◻ 02 — Memory review
- ◻ 03 — Concurrency review
- ◻ 04 — UIKit review
- ◻ 05 — SwiftUI review
- ◻ 06 — Networking review
- ◻ 07 — Persistence review
- ◻ 08 — Architecture review
- ◻ 09 — Testing review
- ◻ 10 — Performance & Security review
- ◻ 11 — Production scenario interview
- ◻ 12 — Swift coding interview
- ◻ 13 — iOS engineering coding
- ◻ 14 — Mobile System Design interview
- ◻ 15 — Behavioral engineering
- ◻ 16 — Mock interview Junior/Middle/Senior
- ◻ 17 — Interview question bank & coverage map
- ◻ 99 — Final Capstone & Handbook Review
