# Phase 03 — Concurrency

Phase này nối tư duy thread/GCD với Swift Concurrency hiện đại. Mục tiêu là quản lý lifetime và isolation của work, không chỉ thêm `async`/`await` cho code cũ.

```text
Thread → shared mutable state → data race
                            ↓
async/await → Task → structured concurrency → cancellation
                            ↓
                  Actor → isolation → Sendable
                            ↓
                 reentrancy → logical race
```

Mọi ví dụ async phải trả lời: task nào sở hữu work, state thuộc isolation domain nào, work có bị cancel không, có sống lâu hơn screen không và ordering có thể đổi không.

Roadmap chi tiết nằm trong [SUMMARY](../SUMMARY.md).

