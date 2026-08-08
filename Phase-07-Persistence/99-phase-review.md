---
title: "Phase Review — Persistence"
phase: "Persistence"
difficulty: 5
importance: 5
interview_frequency: 5
status: complete
last_verified: 2026-08-09
swift_baseline: "Swift 6.3 toolchain; Swift 6 language mode"
levels:
  - L1
  - L2
  - L3
  - L4
  - L5
  - L6
prerequisites:
  - "All chapters in this phase"
used_later:
  - "Following phases"
competencies:
  - "Synthesis"
  - "Production"
  - "Interview"
tags:
  - "phase-review"
  - "persistence"
---

# Phase Review — Persistence

## Phase Summary

Phase hoàn thành mục tiêu: **chọn storage/source of truth theo lifetime, query, security và synchronization requirement**. Review này không dạy lại từng định nghĩa; nó buộc người đọc nối knowledge graph, giải thích trade-off và xử lý production case bằng evidence.

## Chapter Map

1. [01 — Chọn storage theo data, lifetime và security](01-chon-storage-theo-data-lifetime-va-security.md)
2. [02 — UserDefaults: preference, không phải database](02-userdefaults-preference-khong-phai-database.md)
3. [03 — Keychain và sensitive data lifecycle](03-keychain-va-sensitive-data-lifecycle.md)
4. [04 — FileManager, atomic write và file coordination](04-filemanager-atomic-write-va-file-coordination.md)
5. [05 — SQLite concepts, schema và transaction](05-sqlite-concepts-schema-va-transaction.md)
6. [06 — Core Data mental model](06-core-data-mental-model.md)
7. [07 — Managed Object Context và Core Data concurrency](07-managed-object-context-va-core-data-concurrency.md)
8. [08 — SwiftData và ranh giới availability](08-swiftdata-va-ranh-gioi-availability.md)
9. [09 — SwiftData vs Core Data theo constraint](09-swiftdata-vs-core-data-theo-constraint.md)
10. [10 — Migration strategy và rollback thinking](10-migration-strategy-va-rollback-thinking.md)
11. [11 — Persistent cache và invalidation](11-persistent-cache-va-invalidation.md)
12. [12 — Offline-first synchronization](12-offline-first-synchronization.md)
13. [13 — Conflict detection và resolution](13-conflict-detection-va-resolution.md)
14. [14 — Logout/login và data isolation giữa account](14-logout-login-va-data-isolation-giua-account.md)

## Knowledge Map

```text
Chọn storage theo data, lifetime và security → UserDefaults: preference, không phải database → Keychain và sensitive data lifecycle → FileManager, atomic write và file coordination → SQLite concepts, schema và transaction → Core Data mental model
        ↓
Ownership / State / Failure / Lifecycle
        ↓
Production evidence + interview reasoning
```

Mỗi edge phải trả lời “vì sao concept trước là prerequisite của concept sau?”. Nếu không trả lời được, quay lại chapter gốc thay vì học thuộc review.

## Phase Cheat Sheet

```text
Goal       → chọn storage/source of truth theo lifetime, query, security và synchronization requirement
Mental     → Domain intent → repository → local transaction/source of truth ↔ synchronization policy
Runtime    → Disk I/O, context/transaction và migration có lifecycle riêng; synchronous work sai chỗ có thể block UI.
Memory     → Context/object graph/cache giữ resident data; fetch giới hạn và fault/batch strategy cần phù hợp workload.
Concurrency→ Context/model access phải tuân isolation; sync cần ordering, idempotency và conflict policy.
Evidence   → Database inspection, transaction logs, migration tests, file protection checks và memory/disk metrics.
```

## Review Questions

1. Với Chọn storage theo data, lifetime và security, invariant, owner và evidence chính là gì?
2. Với UserDefaults: preference, không phải database, invariant, owner và evidence chính là gì?
3. Với Keychain và sensitive data lifecycle, invariant, owner và evidence chính là gì?
4. Với FileManager, atomic write và file coordination, invariant, owner và evidence chính là gì?
5. Với SQLite concepts, schema và transaction, invariant, owner và evidence chính là gì?
6. Với Core Data mental model, invariant, owner và evidence chính là gì?
7. Với Managed Object Context và Core Data concurrency, invariant, owner và evidence chính là gì?
8. Với SwiftData và ranh giới availability, invariant, owner và evidence chính là gì?
9. Với SwiftData vs Core Data theo constraint, invariant, owner và evidence chính là gì?
10. Với Migration strategy và rollback thinking, invariant, owner và evidence chính là gì?
11. Với Persistent cache và invalidation, invariant, owner và evidence chính là gì?
12. Với Offline-first synchronization, invariant, owner và evidence chính là gì?
13. Với Conflict detection và resolution, invariant, owner và evidence chính là gì?
14. Với Logout/login và data isolation giữa account, invariant, owner và evidence chính là gì?

## Deep-dive Questions

1. Constraint nào làm best practice trong phase không còn đúng?
2. Vẽ owner/state/task graph cho Product Detail hoặc Checkout.
3. Phân biệt documented behavior và implementation inference trong một API.
4. Một compile-time guarantee nào vẫn không bảo vệ business invariant?
5. Thiết kế metric và regression test cho failure mode hiếm.

## Coding Exercises

### Easy

Viết một Commerce model/flow nhỏ dùng ba concept của phase và unit test invariant.

### Medium

Refactor code có multiple sources of truth thành state transition với dependency rõ.

### Hard

Thêm cancellation, retry hoặc lifecycle interruption; chứng minh stale work không commit kết quả.

## Debugging Lab

```text
Bug report → repeated flow → symptom không deterministic
Evidence   → logs/trace/graph phù hợp
Task       → hypotheses → root cause → fix → regression prevention
```

Không được bắt đầu bằng sửa code. Nộp kèm graph, evidence trước/sau và lý do loại bỏ từng hypothesis.

## Mini Project — Global Commerce

Xây/refactor một vertical slice gồm UI event, state owner, repository boundary, test và privacy-aware logging. Scope nhỏ nhưng phải có happy path, failure, cancellation/lifecycle và metric.

## Mock Interview

- 5 phút Foundation: định nghĩa bằng behavior.
- 10 phút Middle: mechanism, ownership, trade-off.
- 15 phút Senior: production variant, migration và observability.
- Rubric: correctness, depth, reasoning, production awareness, communication.

## References

- [SwiftData](https://developer.apple.com/documentation/swiftdata) — truy cập 2026-08-09.
- [Core Data](https://developer.apple.com/documentation/coredata) — truy cập 2026-08-09.
- [Keychain Services](https://developer.apple.com/documentation/security/keychain-services) — truy cập 2026-08-09.

## Completion Checklist

- [x] Phase summary, cheat sheet và knowledge map
- [x] Review/deep-dive questions
- [x] Coding exercises và debugging lab
- [x] Mini project/case study
- [x] Mock interview
- [x] Tất cả mandatory chapters có file complete
