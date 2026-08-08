# Phase 05 — Networking

Phase này đi từ HTTP đến networking layer có cancellation, retry, authentication và cache policy.

```text
View → ViewModel → Repository → API Client → URLSession → Server
                                         ↘ error taxonomy / retry / auth
```

Đích đến là phân biệt transport, HTTP, decode và business error; coalesce token refresh thành một operation; retry có backoff, jitter, cancellation và idempotency; đồng thời không log dữ liệu nhạy cảm.

Roadmap chi tiết nằm trong [SUMMARY](../SUMMARY.md).

