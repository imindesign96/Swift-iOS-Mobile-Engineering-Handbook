# Phase 05 — Networking

Phase này tập trung vào mục tiêu: **xây networking boundary có error taxonomy, cancellation, auth, retry và cache policy**.

## Dependency map

```text
View → ViewModel → Repository → API Client → URLSession → HTTP server → mapped result
      ↓
Runtime + Memory + Concurrency + Architecture
      ↓
Production evidence + Interview synthesis
```

## Learning outcomes

- Giải thích concept bằng behavior, constraint và trade-off.
- Xác định owner/state/failure/lifecycle cho Commerce flow.
- Dùng Network Instruments, URLSession metrics, server correlation ID và privacy-aware structured logs. thay vì đoán root cause.
- Hoàn thành coding exercise, debugging lab và mock interview của phase.

## Chapters — Complete

- [01 — Một request từ iPhone đến server đi như thế nào?](01-mot-request-tu-iphone-en-server-i-nhu-the-nao.md)
- [02 — HTTP methods, headers, status và idempotency](02-http-methods-headers-status-va-idempotency.md)
- [03 — URLSession, URLRequest và response lifecycle](03-urlsession-urlrequest-va-response-lifecycle.md)
- [04 — Codable, CodingKeys và resilient decoding](04-codable-codingkeys-va-resilient-decoding.md)
- [05 — API client và Endpoint abstraction](05-api-client-va-endpoint-abstraction.md)
- [06 — Error taxonomy: transport/HTTP/decode/business](06-error-taxonomy-transport-http-decode-business.md)
- [07 — Timeout, retry, backoff và jitter](07-timeout-retry-backoff-va-jitter.md)
- [08 — Cancellation từ screen đến URLSession](08-cancellation-tu-screen-en-urlsession.md)
- [09 — Access token, refresh token và Keychain boundary](09-access-token-refresh-token-va-keychain-boundary.md)
- [10 — Single-flight token refresh](10-single-flight-token-refresh.md)
- [11 — Pagination, prefetch và duplicate requests](11-pagination-prefetch-va-duplicate-requests.md)
- [12 — HTTP caching, ETag và cache policy](12-http-caching-etag-va-cache-policy.md)
- [13 — Kết hợp remote cache và offline data](13-ket-hop-remote-cache-va-offline-data.md)
- [14 — ATS, TLS và certificate pinning trade-offs](14-ats-tls-va-certificate-pinning-trade-offs.md)
- [15 — Network diagnostics và privacy-aware logging](15-network-diagnostics-va-privacy-aware-logging.md)
- [99 — Phase Review: Networking](99-phase-review.md)

## Quality gate

Toàn bộ chapter có front matter `status: complete`, production case, debugging evidence, interview questions, exercises, cheat sheet, references và links nội bộ hợp lệ.
