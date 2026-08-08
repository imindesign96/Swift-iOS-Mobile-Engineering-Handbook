# Phase 07 — Persistence

Phase này chọn storage theo dữ liệu và lifetime thay vì theo API quen tay.

```text
Repository
  ├── Remote
  └── Local Store → UserDefaults / Keychain / File / SQLite / Core Data / SwiftData
```

Các chapter sẽ xác định source of truth, migration, context isolation, cache invalidation, offline strategy và conflict resolution. Security và concurrency là yêu cầu xuyên suốt, không phải phần bổ sung cuối phase.

Roadmap chi tiết nằm trong [SUMMARY](../SUMMARY.md).

