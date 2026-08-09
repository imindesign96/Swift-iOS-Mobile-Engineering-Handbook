---
title: "StoreKit 2: IAP, subscription, verification và server contract"
phase: "iOS Platform"
difficulty: 5
importance: 5
interview_frequency: 5
status: complete
last_verified: 2026-08-09
swift_baseline: "Swift 6.3 toolchain; Swift 6 language mode"
levels:
  - L4
  - L5
prerequisites:
  - "Error taxonomy: transport/HTTP/decode/business"
  - "Keychain và sensitive data lifecycle"
used_later:
  - "App Store release engineering: signing, privacy, review và rollback"
  - "Commerce Checkout state machine"
competencies:
  - "iOS Platform"
  - "Security"
  - "Production"
  - "System Design"
tags:
  - "storekit-2"
  - "in-app-purchase"
  - "subscription"
  - "transaction-verification"
---

# StoreKit 2: IAP, subscription, verification và server contract

> **Version scope**
>
> Dùng StoreKit 2 và signed transaction JWS. API thay đổi theo SDK nên phải giữ availability check và test lại bằng StoreKit Configuration, Sandbox và TestFlight. Xác minh 2026-08-09.

## Story / Problem

Người dùng mua gói Premium và App Store báo thành công, nhưng app vẫn khóa tính năng. Một người khác đã refund mà backend vẫn cho truy cập. Sau khi cài lại app, nút “Restore” không trả lại entitlement. Đây không phải ba bug rời nhau: team chưa định nghĩa **entitlement là state được suy ra từ transaction đã xác minh**, và chưa nói rõ app hay server là authority trong từng chế độ kinh doanh.

```text
Product metadata → purchase result → verified transaction → entitlement
                                      ↓
                    App Store Server Notifications V2 / Server API
```

Không lưu `isPremium = true` như sự thật vĩnh viễn. Nó chỉ là projection/cache có thể tái tạo từ transaction history, subscription status và business policy.

## Objectives

Sau chapter này, bạn có thể:

- triển khai load product, purchase, verification, finish và transaction listener;
- khôi phục giao dịch bằng entitlement reconciliation và `AppStore.sync()` đúng ngữ cảnh;
- mô hình hóa subscription state gồm active, grace period, billing retry, expired, revoked và upgraded;
- thiết kế contract giữa client, App Store Server Notifications V2 và backend;
- phân biệt receipt/transaction hợp lệ với quyền truy cập hợp lệ theo business rule;
- điều tra duplicate delivery, refund, pending Ask to Buy và account mismatch mà không cấp quyền sai.

## Prerequisites

- [Error taxonomy](../Phase-05-Networking/06-error-taxonomy-transport-http-decode-business.md) để tách lỗi StoreKit, verification, network và business.
- [Keychain và sensitive data lifecycle](../Phase-07-Persistence/03-keychain-va-sensitive-data-lifecycle.md) cho account binding; không lưu transaction như secret tự chế.
- [Commerce Checkout state machine](../Phase-10-Mobile-System-Design/17-commerce-checkout-state-machine.md) cho idempotency và state transition.

## Used Later

- [App Store release engineering](../Phase-09-Production/21-app-store-release-engineering-signing-privacy-review-va-rollback.md) kiểm tra product configuration và TestFlight release gate.
- [Observability, SLO và incident response](../Phase-09-Production/18-observability-slo-va-incident-response.md) theo dõi purchase success nhưng entitlement activation thất bại.

## Mental Model

```text
Transaction = signed event từ App Store
Entitlement = kết luận business hiện tại từ verified events + thời gian + revocation
UI state     = projection của entitlement, không phải authority
```

`VerificationResult.verified` chứng minh signed data vượt qua verification của StoreKit; nó không tự quyết định SKU có mở feature nào, user app-account nào sở hữu quyền, hay server đã hoàn tất fulfillment chưa. Consumable, non-consumable, non-renewing và auto-renewable subscription có lifecycle khác nhau.

## What?

Flow chuẩn gồm sáu phần:

1. Lấy `Product` theo product ID từ configuration do team quản lý.
2. Gọi `purchase(options:)`, có thể gắn `appAccountToken` ổn định nhưng không chứa PII.
3. Xử lý `.success`, `.pending` và `.userCancelled` riêng biệt.
4. Chỉ nhận `Transaction` từ case `.verified`; case `.unverified` không cấp quyền.
5. Fulfill entitlement idempotently rồi gọi `transaction.finish()`.
6. Chạy listener `Transaction.updates` suốt app session để nhận purchase/renewal/refund đến ngoài flow màn hình.

`Transaction.currentEntitlements` là nguồn reconciliation phía client cho non-consumable và subscription hiện tại. Product bị refund/revoke không xuất hiện như entitlement hợp lệ. Với dịch vụ có backend, server lưu ledger theo `originalTransactionId`/transaction ID, xác minh signed data, xử lý notification V2 idempotently và trả entitlement projection cho app.

## Why?

Purchase không phải một request-response bình thường. User có thể hoàn tất thanh toán sau khi app bị terminate; Ask to Buy để transaction ở pending; renewal và refund xảy ra khi app không chạy; notification server có thể retry hoặc đến khác thứ tự. Nếu chỉ unlock trong callback của nút Buy, hệ thống mất tính khôi phục và tạo gian lận kiểu replay/client patch.

## How?

```swift
import StoreKit

actor EntitlementStore {
    private(set) var activeProductIDs: Set<String> = []

    func listen() async {
        for await result in Transaction.updates {
            guard case .verified(let transaction) = result else { continue }
            await apply(transaction)
            await transaction.finish()
        }
    }

    func reconcile() async {
        var current: Set<String> = []
        for await result in Transaction.currentEntitlements {
            guard case .verified(let transaction) = result,
                  transaction.revocationDate == nil else { continue }
            current.insert(transaction.productID)
        }
        activeProductIDs = current
    }

    private func apply(_ transaction: Transaction) async {
        if transaction.revocationDate == nil {
            activeProductIDs.insert(transaction.productID)
        } else {
            activeProductIDs.remove(transaction.productID)
        }
    }
}
```

App tạo listener sớm và giữ task theo app lifetime. Với purchase result, dùng cùng `apply` path để tránh hai implementation fulfillment khác nhau. Đừng finish trước khi durable fulfillment hoàn tất; nhưng fulfillment phải idempotent vì transaction có thể được giao lại.

### Restore purchase

App nên tự reconcile khi launch, login, foreground và sau purchase. Nút Restore vẫn hữu ích để user chủ động sửa trạng thái; `AppStore.sync()` yêu cầu tương tác/account authentication nên chỉ gọi từ user action, sau đó đọc lại entitlement. Consumable đã tiêu thụ không thể “restore” như non-consumable.

### Subscription state

Đừng rút gọn mọi thứ thành expiration date. Cần xem renewal state/status để quyết định policy cho subscribed, grace period, billing retry, expired/revoked và product upgrade. UI quản lý subscription nên dùng system-provided management flow khi phù hợp. Clock của device không phải authority chống gian lận cho dịch vụ giá trị cao.

### Server notification và fraud boundary

Server Notifications V2 gửi signed JWS. Endpoint phải xác minh chain/signature và claims, phân biệt sandbox/production, deduplicate notification/transaction, lưu raw identifier tối thiểu phục vụ audit và trả 2xx chỉ sau durable acceptance. Khi event thiếu hoặc out-of-order, gọi App Store Server API để reconcile history/status thay vì đoán.

Fraud handling là defense-in-depth: dùng `appAccountToken` bind giao dịch với account nội bộ, rate-limit fulfillment, chống replay theo transaction ID, không tin product ID/expiration do client tự gửi, xử lý refund/revocation và giữ audit trail. Không fingerprint user hoặc biến false positive thành mất quyền âm thầm; cần recovery/support path.

## Production Case

### Context

Global Commerce bán auto-renewable Premium dùng được trên nhiều thiết bị.

### Symptom

0,4% purchase thành công nhưng app vẫn hiển thị Free; một số account được Premium hai lần.

### Investigation

Team nối `appAccountToken`, transaction ID, original transaction ID và server notification ID bằng log đã redact. Timeline cho thấy client finish trước khi backend ghi ledger; request timeout khiến client retry với một endpoint không idempotent. Listener cũng chỉ tồn tại trong paywall nên renewal đến lúc màn hình đóng bị bỏ qua.

### Root Cause

Fulfillment không có idempotency key và task listener thuộc screen lifetime thay vì app lifetime.

### Fix

Backend upsert ledger theo transaction ID, app giữ listener tại composition root, chỉ finish sau durable acceptance hoặc local durable queue, rồi reconcile current entitlements.

### Prevention

Dashboard đo purchase initiated/success/verified/fulfilled; alert cho khoảng cách giữa verified và activated; test duplicate, delayed, refund, revoke, account switch và notification out-of-order.

## Interview Questions

### Foundation

**StoreKit 2 verification khác receipt flag thế nào?** Transaction được App Store ký và StoreKit trả qua `VerificationResult`; entitlement vẫn phải áp business rule.

### Middle

**Restore purchase nên làm gì?** Reconcile `currentEntitlements`; chỉ gọi `AppStore.sync()` từ user gesture khi cần đồng bộ lịch sử với App Store, rồi rebuild projection.

### Senior

**Thiết kế subscription cho app có backend?** Trình bày client listener, JWS verification, account binding, idempotent ledger, Notifications V2, Server API reconciliation, refund/grace policy, observability và support recovery.

## Exercises

### Easy

Mô hình hóa purchase UI state: idle, loading products, purchasing, pending, active và failed.

### Medium

Viết `EntitlementStore` có injected transaction stream để test verified/unverified/revoked.

### Hard

Thiết kế database ledger và idempotent notification handler cho subscription nhiều thiết bị.

### Debugging Lab

Dùng StoreKit Configuration tạo Ask to Buy, renewal, expiration và refund; chứng minh UI tự reconcile sau relaunch.

## Cheat Sheet

```text
success ≠ verified ≠ fulfilled
Transaction.updates      → event listener theo app lifetime
currentEntitlements      → rebuild entitlement projection
AppStore.sync()          → user-initiated restore, không gọi tùy tiện
finish()                 → sau durable/idempotent fulfillment
Notifications V2        → verify + dedupe + ledger + reconcile
```

## Chapter Summary

1. Transaction là signed event; entitlement là business projection có thể tái tạo.
2. Verify trước khi cấp quyền và finish sau fulfillment idempotent.
3. Listener thuộc app lifetime; restore dùng reconciliation, không chỉ một nút.
4. Subscription cần grace, retry, refund, revoke và account binding.
5. Backend phải xem notification là at-least-once, có thể delayed/out-of-order.

## Related Chapters

- [Single-flight token refresh](../Phase-05-Networking/10-single-flight-token-refresh.md)
- [Offline-first synchronization](../Phase-07-Persistence/12-offline-first-synchronization.md)
- [Commerce Checkout state machine](../Phase-10-Mobile-System-Design/17-commerce-checkout-state-machine.md)

## References

- [Apple — Transaction and verification](https://developer.apple.com/documentation/storekit/transaction)
- [Apple — Transaction.currentEntitlements](https://developer.apple.com/documentation/storekit/transaction/currententitlements)
- [Apple — In-App Purchase](https://developer.apple.com/in-app-purchase/)
- [Apple — App Store Server Notifications](https://developer.apple.com/documentation/appstoreservernotifications)
- [Apple — App Store Server API](https://developer.apple.com/documentation/appstoreserverapi)
