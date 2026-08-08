---
title: "Phase Review — Production"
phase: "Production"
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
  - "production"
---

# Phase Review — Production

## Phase Summary

Phase hoàn thành mục tiêu: **đi từ symptom đến evidence, root cause và regression prevention**. Review này không dạy lại từng định nghĩa; nó buộc người đọc nối knowledge graph, giải thích trade-off và xử lý production case bằng evidence.

## Chapter Map

1. [01 — Structured, privacy-aware logging](01-structured-privacy-aware-logging.md)
2. [02 — Crash report và symbolication](02-crash-report-va-symbolication.md)
3. [03 — EXC_BAD_ACCESS, fatal error và index out of range](03-exc-bad-access-fatal-error-va-index-out-of-range.md)
4. [04 — Hang, watchdog và stack evidence](04-hang-watchdog-va-stack-evidence.md)
5. [05 — Memory leak investigation](05-memory-leak-investigation.md)
6. [06 — Memory pressure và OS termination](06-memory-pressure-va-os-termination.md)
7. [07 — Instruments workflow: measure before fix](07-instruments-workflow-measure-before-fix.md)
8. [08 — Time Profiler và hot call tree](08-time-profiler-va-hot-call-tree.md)
9. [09 — Allocations, Leaks và Memory Graph](09-allocations-leaks-va-memory-graph.md)
10. [10 — Scroll hitch, layout và rendering diagnostics](10-scroll-hitch-layout-va-rendering-diagnostics.md)
11. [11 — Image decoding, downsampling và cache budget](11-image-decoding-downsampling-va-cache-budget.md)
12. [12 — App launch: pre-main/post-main](12-app-launch-pre-main-post-main.md)
13. [13 — Battery và energy diagnostics](13-battery-va-energy-diagnostics.md)
14. [14 — Network-only production failure](14-network-only-production-failure.md)
15. [15 — Release-only và device-specific bugs](15-release-only-va-device-specific-bugs.md)
16. [16 — Background execution và interrupted work](16-background-execution-va-interrupted-work.md)
17. [17 — Concurrency incidents ở quy mô session lớn](17-concurrency-incidents-o-quy-mo-session-lon.md)
18. [18 — Observability, SLO và incident response](18-observability-slo-va-incident-response.md)

## Knowledge Map

```text
Structured, privacy-aware logging → Crash report và symbolication → EXC_BAD_ACCESS, fatal error và index out of range → Hang, watchdog và stack evidence → Memory leak investigation → Memory pressure và OS termination
        ↓
Ownership / State / Failure / Lifecycle
        ↓
Production evidence + interview reasoning
```

Mỗi edge phải trả lời “vì sao concept trước là prerequisite của concept sau?”. Nếu không trả lời được, quay lại chapter gốc thay vì học thuộc review.

## Phase Cheat Sheet

```text
Goal       → đi từ symptom đến evidence, root cause và regression prevention
Mental     → Symptom → evidence → hypotheses → measurement → root cause → fix → prevention
Runtime    → Crash/hang/termination/performance regression tạo artifact khác nhau; trước hết phải phân loại đúng tín hiệu.
Memory     → Tách leak, peak working set, decoded resource cost và OS pressure; đo repeated flow trên device phù hợp.
Concurrency→ Thu thập ordering, isolation, cancellation và correlation context mà không log dữ liệu nhạy cảm.
Evidence   → Xcode Organizer, crash report/symbolication, Instruments, MetricKit và structured production telemetry.
```

## Review Questions

1. Với Structured, privacy-aware logging, invariant, owner và evidence chính là gì?
2. Với Crash report và symbolication, invariant, owner và evidence chính là gì?
3. Với EXC_BAD_ACCESS, fatal error và index out of range, invariant, owner và evidence chính là gì?
4. Với Hang, watchdog và stack evidence, invariant, owner và evidence chính là gì?
5. Với Memory leak investigation, invariant, owner và evidence chính là gì?
6. Với Memory pressure và OS termination, invariant, owner và evidence chính là gì?
7. Với Instruments workflow: measure before fix, invariant, owner và evidence chính là gì?
8. Với Time Profiler và hot call tree, invariant, owner và evidence chính là gì?
9. Với Allocations, Leaks và Memory Graph, invariant, owner và evidence chính là gì?
10. Với Scroll hitch, layout và rendering diagnostics, invariant, owner và evidence chính là gì?
11. Với Image decoding, downsampling và cache budget, invariant, owner và evidence chính là gì?
12. Với App launch: pre-main/post-main, invariant, owner và evidence chính là gì?
13. Với Battery và energy diagnostics, invariant, owner và evidence chính là gì?
14. Với Network-only production failure, invariant, owner và evidence chính là gì?
15. Với Release-only và device-specific bugs, invariant, owner và evidence chính là gì?
16. Với Background execution và interrupted work, invariant, owner và evidence chính là gì?
17. Với Concurrency incidents ở quy mô session lớn, invariant, owner và evidence chính là gì?
18. Với Observability, SLO và incident response, invariant, owner và evidence chính là gì?

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

- [Performance and metrics](https://developer.apple.com/documentation/xcode/performance-and-metrics) — truy cập 2026-08-09.
- [Diagnosing issues using crash reports](https://developer.apple.com/documentation/xcode/diagnosing-issues-using-crash-reports-and-device-logs) — truy cập 2026-08-09.
- [MetricKit](https://developer.apple.com/documentation/metrickit) — truy cập 2026-08-09.

## Completion Checklist

- [x] Phase summary, cheat sheet và knowledge map
- [x] Review/deep-dive questions
- [x] Coding exercises và debugging lab
- [x] Mini project/case study
- [x] Mock interview
- [x] Tất cả mandatory chapters có file complete
