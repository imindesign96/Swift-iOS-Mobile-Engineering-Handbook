# Phase 06 — Architecture

Phase này tập trung vào mục tiêu: **tạo dependency direction và ownership boundary vừa đủ cho complexity hiện tại**.

## Dependency map

```text
UI → application policy → repository boundary → remote/local implementation
      ↓
Runtime + Memory + Concurrency + Architecture
      ↓
Production evidence + Interview synthesis
```

## Learning outcomes

- Giải thích concept bằng behavior, constraint và trade-off.
- Xác định owner/state/failure/lifecycle cho Commerce flow.
- Dùng Dependency graph, build metrics, ADR, code review và tests tại boundary. thay vì đoán root cause.
- Hoàn thành coding exercise, debugging lab và mock interview của phase.

## Chapters — Complete

- [01 — MVC và Massive ViewController](01-mvc-va-massive-viewcontroller.md)
- [02 — MVVM và ranh giới trách nhiệm ViewModel](02-mvvm-va-ranh-gioi-trach-nhiem-viewmodel.md)
- [03 — Coordinator và navigation ownership](03-coordinator-va-navigation-ownership.md)
- [04 — Repository không chỉ là tên khác của API client](04-repository-khong-chi-la-ten-khac-cua-api-client.md)
- [05 — Dependency Injection và constructor injection](05-dependency-injection-va-constructor-injection.md)
- [06 — Service Locator và Singleton: trade-offs thật](06-service-locator-va-singleton-trade-offs-that.md)
- [07 — UseCase/Interactor: khi nào đáng thêm một layer](07-usecase-interactor-khi-nao-ang-them-mot-layer.md)
- [08 — Clean Architecture principles trên mobile](08-clean-architecture-principles-tren-mobile.md)
- [09 — State machine thay cho Boolean explosion](09-state-machine-thay-cho-boolean-explosion.md)
- [10 — SPM modularization và dependency direction](10-spm-modularization-va-dependency-direction.md)
- [11 — Feature boundary và ngăn circular dependency](11-feature-boundary-va-ngan-circular-dependency.md)
- [12 — Architecture Decision Record](12-architecture-decision-record.md)
- [13 — Migration strategy không big-bang rewrite](13-migration-strategy-khong-big-bang-rewrite.md)
- [14 — Refactoring Massive ViewController/Model/God Service](14-refactoring-massive-viewcontroller-model-god-service.md)
- [99 — Phase Review: Architecture](99-phase-review.md)

## Quality gate

Toàn bộ chapter có front matter `status: complete`, production case, debugging evidence, interview questions, exercises, cheat sheet, references và links nội bộ hợp lệ.
