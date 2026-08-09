---
title: "APNs và Push Notification end-to-end"
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
  - "App Extensions: Notification Service Extension và WidgetKit"
  - "Notification routing"
used_later:
  - "App Intents, Shortcuts, Live Activities và ActivityKit"
  - "BackgroundTasks và background URLSession"
competencies:
  - "iOS Platform"
  - "Networking"
  - "Security"
  - "Production"
tags:
  - "apns"
  - "push-notification"
  - "silent-notification"
  - "notification-routing"
---

# APNs và Push Notification end-to-end

> **Version scope**
>
> Áp dụng APNs HTTP/2 provider API, UserNotifications và scene-based navigation. Header/payload contract phải kiểm tra lại theo loại push và OS target. Xác minh 2026-08-09.

## Story / Problem

Backend báo APNs trả `200`, nhưng khách không thấy thông báo. Một push mở đúng order khi app foreground nhưng sai khi cold launch. Token hoạt động ở development, fail ở TestFlight. Team đang trộn bốn khái niệm: provider chấp nhận request, hệ thống giao push, người dùng cho phép UI notification, và app route event thành navigation.

```text
Business event → provider → APNs → device/system → app/extension → typed route
                   200         best effort          lifecycle-dependent
```

Mỗi mũi tên có identity, environment, policy và evidence khác nhau. `200` từ APNs chỉ là acceptance, không phải bằng chứng người dùng đã thấy nội dung.

## Objectives

Sau chapter này, bạn có thể:

- giải thích lifecycle và scope của APNs device token;
- tạo payload/header đúng cho alert, background và service extension;
- phân biệt development/production environment, topic, push type, priority, expiration và collapse ID;
- thiết kế permission prompt theo value moment thay vì hỏi ở first launch;
- route notification idempotently qua foreground, background và cold start;
- điều tra lỗi production từ provider response đến delivery và business outcome.

## Prerequisites

- [App Extensions](21-app-extensions-notification-service-extension-va-widgetkit.md) cho `mutable-content` và expiration fallback.
- [Notification routing](../Phase-10-Mobile-System-Design/09-notification-routing.md) cho typed route và deduplication.
- [Universal Links](23-universal-links-aasa-routing-fallback-va-security.md) cho link validation.

## Used Later

- [App Intents và ActivityKit](29-app-intents-shortcuts-live-activities-va-activitykit.md) dùng push token riêng của Live Activity.
- [BackgroundTasks](../Phase-09-Production/22-bgtaskscheduler-background-urlsession-energy-va-debugging.md) chọn đúng background mechanism.

## Mental Model

```text
Token = địa chỉ opaque của app-device-environment hiện tại
Permission = quyền trình bày alert/sound/badge, không phải quyền đăng ký token
Payload = hint/event nhỏ; API fetch mới là source of truth
Delivery = best effort; business workflow phải chịu được mất, trễ, lặp, reorder
```

Token không phải user ID và một user có thể có nhiều token. Không cache giả định token bất biến; đăng ký với APNs mỗi launch và gửi token mới nhất lên provider. Khi logout, backend phải gỡ association account-token nhưng không cần tự “hủy” token của hệ thống.

## What?

Client bật Push Notifications capability để có `aps-environment`, gọi `registerForRemoteNotifications()`, nhận token qua app delegate và upload qua TLS. Provider dùng APNs authentication key hoặc certificate, gửi request đến đúng endpoint với token, `apns-topic` khớp bundle ID/target và `apns-push-type` khớp payload.

Alert notification có `alert`, `sound` hoặc `badge`; silent/background update dùng `content-available: 1` và không giả làm guaranteed scheduler. `mutable-content: 1` cho Notification Service Extension sửa nội dung trước delivery. Custom payload chỉ mang identifier/version tối thiểu, không mang secret, token hay dữ liệu thanh toán.

## Why?

APNs tối ưu hệ thống, pin và mạng; nó có thể throttle, coalesce, store tạm hoặc không giao. Silent push phụ thuộc system conditions và usage pattern. Nếu product coi push là message queue đáng tin cậy, mất một notification sẽ làm mất business state. Rule đúng là: push nói “có thể có thay đổi”, app fetch authoritative state bằng cursor/version và idempotent API.

## How?

```swift
import UIKit
import UserNotifications

final class AppDelegate: NSObject, UIApplicationDelegate, UNUserNotificationCenterDelegate {
    func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions options: [UIApplication.LaunchOptionsKey: Any]? = nil
    ) -> Bool {
        UNUserNotificationCenter.current().delegate = self
        application.registerForRemoteNotifications()
        return true
    }

    func application(
        _ application: UIApplication,
        didRegisterForRemoteNotificationsWithDeviceToken token: Data
    ) {
        let value = token.map { String(format: "%02x", $0) }.joined()
        Task { try? await PushRegistration.shared.upsert(token: value) }
    }

    func application(
        _ application: UIApplication,
        didFailToRegisterForRemoteNotificationsWithError error: Error
    ) {
        // Log error class + build/environment, không log credential.
    }
}
```

Registration token không cần đợi user cho phép alert. Permission nên hỏi sau khi giải thích lợi ích cụ thể, dùng provisional authorization nếu product strategy phù hợp, và luôn có in-app inbox/settings fallback.

### Provider contract

Ví dụ alert payload versioned:

```json
{
  "aps": {
    "alert": { "title-loc-key": "ORDER_UPDATED_TITLE" },
    "sound": "default",
    "mutable-content": 1
  },
  "schema": 2,
  "event_id": "evt_01",
  "route": { "kind": "order", "id": "ord_42" }
}
```

Provider đặt `apns-topic`, `apns-push-type: alert`, expiration hợp lý và collapse ID chỉ khi các event có thể thay thế nhau. Với background update, dùng push type `background`, priority tương ứng và `content-available`. Không dùng cùng collapse ID cho hai order độc lập.

### Token lifecycle và environment

Token gắn app-device và có thể thay đổi sau restore/reinstall/OS changes; luôn nhận token mới từ callback. Sandbox/development và production dùng endpoint/credential/environment khác; build từ TestFlight/App Store dùng production. Backend lưu nhiều installation cho một account, trạng thái last-seen/build/environment và vô hiệu hóa token khi APNs trả reason cho token không còn active.

### Routing

Mọi entry point—user tap, foreground presentation, scene continuation và cold launch—đều parse payload thành `NotificationRoute` typed, validate authorization bằng API, dedupe `event_id`, rồi giao cho coordinator. Payload không được bypass login hoặc mở resource user không còn quyền xem.

## Production Case

### Context

Global Commerce gửi order update cho Nhật và Việt Nam.

### Symptom

TestFlight không nhận push, development nhận bình thường; một nhóm user mở nhầm order cũ.

### Investigation

Provider log `apns-id`, endpoint, topic, push type, status/reason và correlation event ID. Team phát hiện TestFlight token bị lưu nhãn sandbox. Đồng thời collapse ID dùng chung `order-update` cho mọi order, nên event khác nhau coalesce.

### Root Cause

Environment được client tự truyền và provider tin giá trị đó; collapse scope không chứa order identity.

### Fix

Backend suy ra environment từ build channel/credential registration, tách installation record, dùng collapse ID theo `order/{id}`, và app fetch order state sau route.

### Prevention

Canary device cho development/TestFlight/production; dashboard APNs response theo topic/status/reason; contract test header-payload; metric từ send → accepted → route opened → authoritative fetch.

## Interview Questions

### Foundation

**Permission notification và APNs registration có giống nhau không?** Không. Permission kiểm soát presentation; APNs registration cấp device token cho remote delivery.

### Middle

**Vì sao silent push không dùng làm cron?** Nó best effort và có thể bị throttle; background work phải idempotent, checkpointed và có mechanism phù hợp khác.

### Senior

**APNs trả 200 nhưng user không thấy, điều tra thế nào?** Kiểm tra environment/topic/push type/payload/expiration, permission/focus/device state, extension expiration, routing telemetry; phân biệt acceptance với delivery và presentation.

## Exercises

### Easy

Viết decoder từ payload versioned sang enum route, từ chối unknown schema an toàn.

### Medium

Thiết kế installation API hỗ trợ login/logout, nhiều device và token rotation.

### Hard

Thiết kế notification platform có localization key, collapse policy, retry, invalid-token cleanup và observability.

### Debugging Lab

Gửi alert/background push vào development và TestFlight; lưu `apns-id`, đo từng boundary và giải thích mọi trường hợp không present.

## Cheat Sheet

```text
APNs 200              → accepted, chưa chắc delivered/presented
device token          → opaque, rotating, app-device-environment scoped
topic                 → đúng bundle/target
push type             → khớp alert/background/liveactivity...
silent push           → best effort invalidation signal
payload               → identifier/version, không chứa secret
tap/cold launch       → typed route + authorization + dedupe
```

## Chapter Summary

1. Token là installation address, không phải user identity.
2. Permission presentation tách khỏi APNs registration.
3. Header, payload, topic và environment phải nhất quán.
4. Push chỉ kích hoạt reconciliation; API/store mới là authority.
5. Debug theo từng hop và đo business outcome, không dừng ở APNs status.

## Related Chapters

- [Notification Service Extension và WidgetKit](21-app-extensions-notification-service-extension-va-widgetkit.md)
- [Universal Links](23-universal-links-aasa-routing-fallback-va-security.md)
- [Notification routing](../Phase-10-Mobile-System-Design/09-notification-routing.md)

## References

- [Apple — Registering your app with APNs](https://developer.apple.com/documentation/usernotifications/registering-your-app-with-apns)
- [Apple — Sending notification requests to APNs](https://developer.apple.com/documentation/usernotifications/sending-notification-requests-to-apns)
- [Apple — Generating a remote notification](https://developer.apple.com/documentation/usernotifications/generating-a-remote-notification)
- [Apple — Pushing background updates to your app](https://developer.apple.com/documentation/usernotifications/pushing-background-updates-to-your-app)
