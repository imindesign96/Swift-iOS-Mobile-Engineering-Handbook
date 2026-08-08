---
title: "Phase Review — Networking"
phase: "Networking"
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
  - "networking"
---

# Phase Review — Networking

## Phase Summary

Phase hoàn thành mục tiêu: **xây networking boundary có error taxonomy, cancellation, auth, retry và cache policy**. Review này không dạy lại từng định nghĩa; nó buộc người đọc nối knowledge graph, giải thích trade-off và xử lý production case bằng evidence.

## Chapter Map

1. [01 — Một request từ iPhone đến server đi như thế nào?](01-mot-request-tu-iphone-en-server-i-nhu-the-nao.md)
2. [02 — HTTP methods, headers, status và idempotency](02-http-methods-headers-status-va-idempotency.md)
3. [03 — URLSession, URLRequest và response lifecycle](03-urlsession-urlrequest-va-response-lifecycle.md)
4. [04 — Codable, CodingKeys và resilient decoding](04-codable-codingkeys-va-resilient-decoding.md)
5. [05 — API client và Endpoint abstraction](05-api-client-va-endpoint-abstraction.md)
6. [06 — Error taxonomy: transport/HTTP/decode/business](06-error-taxonomy-transport-http-decode-business.md)
7. [07 — Timeout, retry, backoff và jitter](07-timeout-retry-backoff-va-jitter.md)
8. [08 — Cancellation từ screen đến URLSession](08-cancellation-tu-screen-en-urlsession.md)
9. [09 — Access token, refresh token và Keychain boundary](09-access-token-refresh-token-va-keychain-boundary.md)
10. [10 — Single-flight token refresh](10-single-flight-token-refresh.md)
11. [11 — Pagination, prefetch và duplicate requests](11-pagination-prefetch-va-duplicate-requests.md)
12. [12 — HTTP caching, ETag và cache policy](12-http-caching-etag-va-cache-policy.md)
13. [13 — Kết hợp remote cache và offline data](13-ket-hop-remote-cache-va-offline-data.md)
14. [14 — ATS, TLS và certificate pinning trade-offs](14-ats-tls-va-certificate-pinning-trade-offs.md)
15. [15 — Network diagnostics và privacy-aware logging](15-network-diagnostics-va-privacy-aware-logging.md)

## Knowledge Map

```text
Một request từ iPhone đến server đi như thế nào? → HTTP methods, headers, status và idempotency → URLSession, URLRequest và response lifecycle → Codable, CodingKeys và resilient decoding → API client và Endpoint abstraction → Error taxonomy: transport/HTTP/decode/business
        ↓
Ownership / State / Failure / Lifecycle
        ↓
Production evidence + interview reasoning
```

Mỗi edge phải trả lời “vì sao concept trước là prerequisite của concept sau?”. Nếu không trả lời được, quay lại chapter gốc thay vì học thuộc review.

## Phase Cheat Sheet

```text
Goal       → xây networking boundary có error taxonomy, cancellation, auth, retry và cache policy
Mental     → View → ViewModel → Repository → API Client → URLSession → HTTP server → mapped result
Runtime    → URLSession quản lý task/connection theo configuration; HTTP response và transport completion là hai lớp evidence khác nhau.
Memory     → Response body, decoded models và image data cần budget; cache/request registry không được tăng vô hạn.
Concurrency→ Request phải có owner, cancellation, ordering và single-flight khi chia sẻ refresh/cache work.
Evidence   → Network Instruments, URLSession metrics, server correlation ID và privacy-aware structured logs.
```

## Review Questions

1. Với Một request từ iPhone đến server đi như thế nào?, invariant, owner và evidence chính là gì?
2. Với HTTP methods, headers, status và idempotency, invariant, owner và evidence chính là gì?
3. Với URLSession, URLRequest và response lifecycle, invariant, owner và evidence chính là gì?
4. Với Codable, CodingKeys và resilient decoding, invariant, owner và evidence chính là gì?
5. Với API client và Endpoint abstraction, invariant, owner và evidence chính là gì?
6. Với Error taxonomy: transport/HTTP/decode/business, invariant, owner và evidence chính là gì?
7. Với Timeout, retry, backoff và jitter, invariant, owner và evidence chính là gì?
8. Với Cancellation từ screen đến URLSession, invariant, owner và evidence chính là gì?
9. Với Access token, refresh token và Keychain boundary, invariant, owner và evidence chính là gì?
10. Với Single-flight token refresh, invariant, owner và evidence chính là gì?
11. Với Pagination, prefetch và duplicate requests, invariant, owner và evidence chính là gì?
12. Với HTTP caching, ETag và cache policy, invariant, owner và evidence chính là gì?
13. Với Kết hợp remote cache và offline data, invariant, owner và evidence chính là gì?
14. Với ATS, TLS và certificate pinning trade-offs, invariant, owner và evidence chính là gì?
15. Với Network diagnostics và privacy-aware logging, invariant, owner và evidence chính là gì?

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

- [URLSession](https://developer.apple.com/documentation/foundation/urlsession) — truy cập 2026-08-09.
- [URLRequest](https://developer.apple.com/documentation/foundation/urlrequest) — truy cập 2026-08-09.
- [Loading data from your app](https://developer.apple.com/documentation/foundation/loading-data-from-your-app) — truy cập 2026-08-09.

## Completion Checklist

- [x] Phase summary, cheat sheet và knowledge map
- [x] Review/deep-dive questions
- [x] Coding exercises và debugging lab
- [x] Mini project/case study
- [x] Mock interview
- [x] Tất cả mandatory chapters có file complete
