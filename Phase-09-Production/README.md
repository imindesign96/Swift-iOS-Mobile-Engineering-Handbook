# Phase 09 — Production

Phase này tập trung vào mục tiêu: **đi từ symptom đến evidence, root cause và regression prevention**.

## Dependency map

```text
Symptom → evidence → hypotheses → measurement → root cause → fix → prevention
      ↓
Runtime + Memory + Concurrency + Architecture
      ↓
Production evidence + Interview synthesis
```

## Learning outcomes

- Giải thích concept bằng behavior, constraint và trade-off.
- Xác định owner/state/failure/lifecycle cho Commerce flow.
- Dùng Xcode Organizer, crash report/symbolication, Instruments, MetricKit và structured production telemetry. thay vì đoán root cause.
- Hoàn thành coding exercise, debugging lab và mock interview của phase.

## Chapters — Complete

- [01 — Structured, privacy-aware logging](01-structured-privacy-aware-logging.md)
- [02 — Crash report và symbolication](02-crash-report-va-symbolication.md)
- [03 — EXC_BAD_ACCESS, fatal error và index out of range](03-exc-bad-access-fatal-error-va-index-out-of-range.md)
- [04 — Hang, watchdog và stack evidence](04-hang-watchdog-va-stack-evidence.md)
- [05 — Memory leak investigation](05-memory-leak-investigation.md)
- [06 — Memory pressure và OS termination](06-memory-pressure-va-os-termination.md)
- [07 — Instruments workflow: measure before fix](07-instruments-workflow-measure-before-fix.md)
- [08 — Time Profiler và hot call tree](08-time-profiler-va-hot-call-tree.md)
- [09 — Allocations, Leaks và Memory Graph](09-allocations-leaks-va-memory-graph.md)
- [10 — Scroll hitch, layout và rendering diagnostics](10-scroll-hitch-layout-va-rendering-diagnostics.md)
- [11 — Image decoding, downsampling và cache budget](11-image-decoding-downsampling-va-cache-budget.md)
- [12 — App launch: pre-main/post-main](12-app-launch-pre-main-post-main.md)
- [13 — Battery và energy diagnostics](13-battery-va-energy-diagnostics.md)
- [14 — Network-only production failure](14-network-only-production-failure.md)
- [15 — Release-only và device-specific bugs](15-release-only-va-device-specific-bugs.md)
- [16 — Background execution và interrupted work](16-background-execution-va-interrupted-work.md)
- [17 — Concurrency incidents ở quy mô session lớn](17-concurrency-incidents-o-quy-mo-session-lon.md)
- [18 — Observability, SLO và incident response](18-observability-slo-va-incident-response.md)
- [99 — Phase Review: Production](99-phase-review.md)

## Quality gate

Toàn bộ chapter có front matter `status: complete`, production case, debugging evidence, interview questions, exercises, cheat sheet, references và links nội bộ hợp lệ.
