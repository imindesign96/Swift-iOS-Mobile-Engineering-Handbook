---
title: "App Intents, Shortcuts, Live Activities và ActivityKit"
phase: "iOS Platform"
difficulty: 5
importance: 4
interview_frequency: 4
status: complete
last_verified: 2026-08-09
swift_baseline: "Swift 6.3 toolchain; Swift 6 language mode"
levels:
  - L4
  - L5
prerequisites:
  - "App Extensions: Notification Service Extension và WidgetKit"
  - "APNs và Push Notification end-to-end"
used_later:
  - "App Store release engineering: signing, privacy, review và rollback"
competencies:
  - "iOS Platform"
  - "Architecture"
  - "Concurrency"
  - "Production"
tags:
  - "app-intents"
  - "shortcuts"
  - "live-activities"
  - "activitykit"
---

# App Intents, Shortcuts, Live Activities và ActivityKit

> **Version scope**
>
> App Intents và ActivityKit phát triển nhanh giữa các SDK. Chapter tập trung contract bền: discoverability, entity identity, execution mode, bounded work, push-token rotation và stale/end lifecycle. Gate API mới bằng availability và test trên device. Xác minh 2026-08-09.

## Story / Problem

Team thêm shortcut “Track order”, interactive widget và Live Activity bằng cách gọi trực tiếp singleton của app. Shortcut hoạt động khi app mở nhưng timeout khi chạy nền; widget mutate một cache khác; Live Activity giữ trạng thái “Đang giao” nhiều giờ sau khi order đã hủy. Vấn đề không phải thiếu framework API mà là capability bên ngoài main app chưa dùng chung **domain action và authoritative state contract**.

```text
Siri / Shortcuts / Widget / Live Activity interaction
                         ↓
                 typed App Intent
                         ↓
          use case + repository + policy boundary
                         ↓
               result / route / timeline update
```

## Objectives

Sau chapter này, bạn có thể:

- mô hình hóa `AppIntent`, parameter, `AppEntity` và query có identity ổn định;
- expose App Shortcuts có phrase/localization/discoverability hợp lý;
- chọn foreground/background execution và giới hạn work trong extension/system budget;
- thiết kế Live Activity state nhỏ, Codable, có stale/end policy;
- quản lý push-to-start/update token rotation giữa app, server và APNs;
- dùng shared use case mà không kéo toàn bộ app graph vào extension.

## Prerequisites

- [App Extensions và WidgetKit](21-app-extensions-notification-service-extension-va-widgetkit.md).
- [APNs end-to-end](27-apns-push-notification-end-to-end.md).
- [Typed navigation](16-navigationstack-va-typed-navigation.md).

## Used Later

- [App Store release engineering](../Phase-09-Production/21-app-store-release-engineering-signing-privacy-review-va-rollback.md) kiểm tra entitlement, privacy, metadata và fallback.
- [Mobile System Design interview](../Phase-11-Interview/14-mobile-system-design-interview.md) dùng capability graph làm bài trade-off.

## Mental Model

```text
App Intent    = public, typed command contract cho system experience
App Entity    = stable identity + display representation + query
Live Activity = bounded glanceable projection, không phải database hay timer
```

System có thể chạy intent khi main app không active, trong target khác và với deadline khác. Vì vậy intent phải nhỏ, deterministic, Sendable-friendly và explicit dependency. Live Activity chỉ mang state cần render; dữ liệu nhạy cảm hoặc graph lớn ở repository/server.

## What?

`AppIntent` diễn tả action, title, parameter và `perform()`. `AppEntity` đưa domain object ra system bằng identifier bền và query có scope. `AppShortcutsProvider` cung cấp shortcut/phrase giúp Siri, Spotlight và Shortcuts khám phá action. Interactive widget/Live Activity có thể kích hoạt intent thay vì mở app cho mọi thao tác.

ActivityKit tạo, update và end Live Activity với `ActivityAttributes` và `ContentState`. Local update đến từ app; remote update dùng ActivityKit push token và APNs push type riêng. Token này không phải device token UserNotifications và có lifecycle riêng cho activity/channel.

## Why?

Nếu intent gọi UI controller, nó fail ngoài foreground. Nếu entity ID là localized name, rename làm hỏng shortcut đã lưu. Nếu Live Activity chứa order object đầy đủ, schema/version/privacy và payload size trở nên khó kiểm soát. Nếu server không đặt timestamp/stale/end policy, lock screen hiển thị thông tin sai lâu hơn main app.

## How?

```swift
import AppIntents

struct TrackOrderIntent: AppIntent {
    static let title: LocalizedStringResource = "Track Order"
    static let description = IntentDescription("Open the latest status for an order.")

    @Parameter(title: "Order ID")
    var orderID: String

    static var openAppWhenRun: Bool { true }

    func perform() async throws -> some IntentResult & OpensIntent {
        .result(opensIntent: OpenURLIntent(URL(string: "commerce://order/\(orderID)")!))
    }
}

struct CommerceShortcuts: AppShortcutsProvider {
    static var appShortcuts: [AppShortcut] {
        AppShortcut(
            intent: TrackOrderIntent(),
            phrases: ["Track an order in \(.applicationName)"],
            shortTitle: "Track Order",
            systemImageName: "shippingbox"
        )
    }
}
```

Production code không force unwrap URL và nên dùng typed route builder. Với action không cần UI, inject use case/repository nhỏ qua supported dependency mechanism, kiểm tra authorization và trả dialog/value có localization. Không lạm dụng `openAppWhenRun`; action nhanh nên hoàn thành tại chỗ nếu policy và execution mode cho phép.

### Entity và query

Identifier phải là stable domain ID, không phải index/display name. Query giới hạn kết quả, hỗ trợ search/candidate resolution và không tải toàn database. Display representation không lộ PII trên lock screen. Khi account đổi, invalidate entity cache/shortcut assumptions và yêu cầu authorization lại tại action boundary.

### Live Activity state

```swift
import ActivityKit

struct DeliveryAttributes: ActivityAttributes {
    struct ContentState: Codable, Hashable {
        let phase: String
        let progress: Double
        let updatedAt: Date
    }

    let orderID: String
}
```

State nên semantic, nhỏ và backward-aware. UI render nhiều presentation family, Dynamic Type và privacy redaction. `staleDate` biểu diễn khi content không còn đáng tin; server end activity khi workflow kết thúc. Không update mỗi giây chỉ để giả animation; dùng system-supported time presentation khi phù hợp.

### Push lifecycle

Khi start activity với push, quan sát async sequence token updates, gửi token mới lên backend với activity/order identity và invalidate association cũ. Push-to-start/update/broadcast có capability và OS constraints khác; backend phải chọn đúng topic/push type, timestamp và event. Remote events có thể trễ/reorder nên state mang version/sequence hoặc server timestamp, và end event phải thắng update cũ.

## Production Case

### Context

Live Activity theo dõi giao hàng trong 45 phút.

### Symptom

Sau khi user đổi account, activity của account cũ vẫn cập nhật; 3% activity không kết thúc.

### Investigation

Team đối chiếu activity ID, account generation, push token version, event sequence và end reason. Backend chỉ key token bằng order ID; logout không revoke binding, và retry queue cho update cũ chạy sau event end.

### Root Cause

Thiếu account-scoped identity và terminal-state ordering.

### Fix

Key binding theo account + activity ID + token generation, end/invalidate khi logout, persist monotonic version và bỏ update thấp hơn terminal version.

### Prevention

Test account switch, token rotation, offline, stale, remote end và push reorder; metric active duration, stale duration và orphan activity rate.

## Interview Questions

### Foundation

**App Intent khác deep link?** Intent là typed action có parameter/result và system execution; deep link chủ yếu định tuyến mở app.

### Middle

**Live Activity có phải widget refresh liên tục?** Không. Nó là system-managed projection với constrained update/budget và explicit lifecycle.

### Senior

**Thiết kế remote Live Activity an toàn?** Trình bày token rotation, account binding, APNs headers, versioned state, stale/end semantics, privacy, idempotency, fallback và observability.

## Exercises

### Easy

Tạo App Intent mở typed order route với localized title.

### Medium

Thiết kế `AppEntity` query không dùng display name làm ID.

### Hard

Thiết kế protocol server cho start/update/end Live Activity chịu được token rotation và reorder.

### Debugging Lab

Tạo activity, background app, rotate token giả lập, gửi update cũ sau end và chứng minh client/server bỏ event.

## Cheat Sheet

```text
Intent       → typed, localized, bounded command
Entity ID    → stable domain identity
Extension    → dependency graph nhỏ, không UI singleton
Live state   → compact semantic projection
staleDate    → content không còn đáng tin
end          → terminal business event
push token   → rotating, activity-scoped, không phải APNs device token thường
```

## Chapter Summary

1. App Intents là public action contract với system experiences.
2. Entity identity phải bền và query phải bounded.
3. Shared domain use case tốt hơn gọi trực tiếp main app graph.
4. Live Activity là projection có stale/end lifecycle, không phải database.
5. Remote update cần token rotation, ordering, account isolation và telemetry.

## Related Chapters

- [App Extensions và WidgetKit](21-app-extensions-notification-service-extension-va-widgetkit.md)
- [APNs end-to-end](27-apns-push-notification-end-to-end.md)
- [Typed navigation](16-navigationstack-va-typed-navigation.md)

## References

- [Apple — App Intents](https://developer.apple.com/documentation/appintents)
- [Apple — Creating your first app intent](https://developer.apple.com/documentation/appintents/creating-your-first-app-intent)
- [Apple — Widgets, Live Activities, and Controls](https://developer.apple.com/documentation/appintents/widgets-live-activities-and-controls)
- [Apple — ActivityKit](https://developer.apple.com/documentation/activitykit)
- [Apple — Starting and updating Live Activities with push notifications](https://developer.apple.com/documentation/activitykit/starting-and-updating-live-activities-with-activitykit-push-notifications)
