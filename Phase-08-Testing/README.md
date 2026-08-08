# Phase 08 — Testing

Phase này tập trung vào mục tiêu: **đặt confidence ở đúng boundary với test deterministic và failure dễ chẩn đoán**.

## Dependency map

```text
Risk → observable behavior → controlled dependency → assertion/evidence → regression signal
      ↓
Runtime + Memory + Concurrency + Architecture
      ↓
Production evidence + Interview synthesis
```

## Learning outcomes

- Giải thích concept bằng behavior, constraint và trade-off.
- Xác định owner/state/failure/lifecycle cho Commerce flow.
- Dùng Swift Testing, XCTest, test plans, result bundles, sanitizer và performance metrics. thay vì đoán root cause.
- Hoàn thành coding exercise, debugging lab và mock interview của phase.

## Chapters — Complete

- [01 — Test strategy và test pyramid trên iOS](01-test-strategy-va-test-pyramid-tren-ios.md)
- [02 — XCTest và Swift Testing](02-xctest-va-swift-testing.md)
- [03 — Mock, Stub, Fake và Spy](03-mock-stub-fake-va-spy.md)
- [04 — Dependency Injection tạo testability](04-dependency-injection-tao-testability.md)
- [05 — Async test không sleep](05-async-test-khong-sleep.md)
- [06 — ViewModel testing theo state transition](06-viewmodel-testing-theo-state-transition.md)
- [07 — Networking test với URLProtocol/fake transport](07-networking-test-voi-urlprotocol-fake-transport.md)
- [08 — Repository integration test](08-repository-integration-test.md)
- [09 — UI test cho critical user flow](09-ui-test-cho-critical-user-flow.md)
- [10 — Flaky test: nguyên nhân và containment](10-flaky-test-nguyen-nhan-va-containment.md)
- [11 — Snapshot testing: value và brittleness](11-snapshot-testing-value-va-brittleness.md)
- [12 — TDD và design feedback](12-tdd-va-design-feedback.md)
- [13 — Code coverage: tín hiệu và giới hạn](13-code-coverage-tin-hieu-va-gioi-han.md)
- [14 — Regression test từ production incident](14-regression-test-tu-production-incident.md)
- [15 — E2E automation với XCUITest: fixtures, stability và CI](15-e2e-automation-voi-xcuitest-fixtures-stability-va-ci.md)
- [99 — Phase Review: Testing](99-phase-review.md)

## Quality gate

Toàn bộ chapter có front matter `status: complete`, production case, debugging evidence, interview questions, exercises, cheat sheet, references và links nội bộ hợp lệ.
