# Phase 07 — Persistence

Phase này tập trung vào mục tiêu: **chọn storage/source of truth theo lifetime, query, security và synchronization requirement**.

## Dependency map

```text
Domain intent → repository → local transaction/source of truth ↔ synchronization policy
      ↓
Runtime + Memory + Concurrency + Architecture
      ↓
Production evidence + Interview synthesis
```

## Learning outcomes

- Giải thích concept bằng behavior, constraint và trade-off.
- Xác định owner/state/failure/lifecycle cho Commerce flow.
- Dùng Database inspection, transaction logs, migration tests, file protection checks và memory/disk metrics. thay vì đoán root cause.
- Hoàn thành coding exercise, debugging lab và mock interview của phase.

## Chapters — Complete

- [01 — Chọn storage theo data, lifetime và security](01-chon-storage-theo-data-lifetime-va-security.md)
- [02 — UserDefaults: preference, không phải database](02-userdefaults-preference-khong-phai-database.md)
- [03 — Keychain và sensitive data lifecycle](03-keychain-va-sensitive-data-lifecycle.md)
- [04 — FileManager, atomic write và file coordination](04-filemanager-atomic-write-va-file-coordination.md)
- [05 — SQLite concepts, schema và transaction](05-sqlite-concepts-schema-va-transaction.md)
- [06 — Core Data mental model](06-core-data-mental-model.md)
- [07 — Managed Object Context và Core Data concurrency](07-managed-object-context-va-core-data-concurrency.md)
- [08 — SwiftData và ranh giới availability](08-swiftdata-va-ranh-gioi-availability.md)
- [09 — SwiftData vs Core Data theo constraint](09-swiftdata-vs-core-data-theo-constraint.md)
- [10 — Migration strategy và rollback thinking](10-migration-strategy-va-rollback-thinking.md)
- [11 — Persistent cache và invalidation](11-persistent-cache-va-invalidation.md)
- [12 — Offline-first synchronization](12-offline-first-synchronization.md)
- [13 — Conflict detection và resolution](13-conflict-detection-va-resolution.md)
- [14 — Logout/login và data isolation giữa account](14-logout-login-va-data-isolation-giua-account.md)
- [99 — Phase Review: Persistence](99-phase-review.md)

## Quality gate

Toàn bộ chapter có front matter `status: complete`, production case, debugging evidence, interview questions, exercises, cheat sheet, references và links nội bộ hợp lệ.
