---
title: "Localization: String Catalog, pluralization, RTL và testing"
phase: "iOS Platform"
difficulty: 4
importance: 5
interview_frequency: 4
status: complete
last_verified: 2026-08-09
swift_baseline: "Swift 6.3 toolchain; Swift 6 language mode"
levels:
  - L3
  - L4
prerequisites:
  - "Human Interface Guidelines, accessibility và adaptive UI"
used_later:
  - "App Store release engineering: signing, privacy, review và rollback"
competencies:
  - "iOS Platform"
  - "User Interface"
  - "Testing"
  - "Production"
tags:
  - "localization"
  - "string-catalog"
  - "pluralization"
  - "rtl"
---

# Localization: String Catalog, pluralization, RTL và testing

> **Version scope**
>
> String Catalog (`.xcstrings`) là baseline hiện đại; project cũ có thể còn `.strings`/`.stringsdict`. API format theo `Locale`, `Calendar` và `TimeZone`; không hard-code kết quả phụ thuộc OS locale data. Xác minh 2026-08-09.

## Story / Problem

Ứng dụng Commerce dịch tiếng Nhật đúng chữ nhưng hiển thị `¥1,200.00`, ngày giao hàng lệch một ngày, tiếng Ả Rập đảo icon Back nhưng biểu đồ và mã đơn cũng bị mirror, còn câu “1 items” xuất hiện trong push. Team đã xem localization như file dịch, trong khi bài toán thật là **quốc tế hóa data, layout, assets, copy và workflow kiểm thử**.

```text
Semantic value + locale/calendar/time zone + localized resource
                         ↓
             text/layout/accessibility output
```

Không lưu formatted string như domain data. Lưu `Decimal`, currency code, `Date`/instant và semantic identifier; format ở presentation boundary theo locale phù hợp.

## Objectives

Sau chapter này, bạn có thể:

- tổ chức String Catalog có stable key, comment và trạng thái dịch;
- dùng plural variation thay vì nối chuỗi hoặc giả định chỉ có one/other;
- format tiền, số, ngày và measurement theo locale/time zone rõ ràng;
- thiết kế UI chịu được text expansion, RTL và localized assets;
- tạo test matrix cho language, region, calendar, time zone và pseudo-localization;
- ngăn server/push làm vỡ localization contract.

## Prerequisites

- [HIG, accessibility và adaptive UI](20-human-interface-guidelines-accessibility-va-adaptive-ui.md).
- [HIG in practice](25-human-interface-guidelines-in-practice-navigation-modality-controls-va-feedback.md) cho writing và feedback.

## Used Later

- [App Store release engineering](../Phase-09-Production/21-app-store-release-engineering-signing-privacy-review-va-rollback.md) dùng localization completeness và screenshot matrix làm release gate.
- [E2E automation](../Phase-08-Testing/15-e2e-automation-voi-xcuitest-fixtures-stability-va-ci.md) chạy critical flows ở locale đại diện.

## Mental Model

```text
Language ≠ Region ≠ Locale ≠ TimeZone ≠ Calendar

"ja" + Japan region + Asia/Tokyo
"en" + US region   + America/Los_Angeles
```

Language quyết định copy; region ảnh hưởng định dạng; time zone đổi ngày hiển thị; calendar có thể đổi component; layout direction ảnh hưởng thứ tự không gian. User có thể chọn tổ hợp khác giả định của developer.

## What?

Internationalization làm code/resource có khả năng thích nghi. Localization cung cấp bản dịch và adaptation cho một thị trường. String Catalog tập trung key, source language, comments, plural/device variations và translation state. Stable semantic key như `cart.item_count` chịu được đổi English copy tốt hơn lấy nguyên câu làm identity trong hệ thống lớn.

UI cần Auto Layout/SwiftUI flexible sizing, Dynamic Type, multiline và semantic alignment. RTL không đơn giản là transform toàn screen: navigation direction và directional chevron thường mirror, nhưng logo, media controls, chart timeline, số điện thoại hoặc mã định danh có rule riêng.

## Why?

Nối chuỗi phá trật tự ngữ pháp. Hard-code `%d items` bỏ qua ngôn ngữ có zero/two/few/many. `DateFormatter` mặc định có thể dùng time zone không mong muốn. Giá `Decimal` format với locale device nhưng currency theo market khác có thể gây hiểu nhầm thanh toán. Một translation đúng vẫn fail nếu button truncate hoặc VoiceOver đọc key kỹ thuật.

## How?

```swift
import Foundation

struct CommerceFormatting {
    static func price(
        _ amount: Decimal,
        currency: String,
        locale: Locale
    ) -> String {
        amount.formatted(
            .currency(code: currency)
                .locale(locale)
        )
    }

    static func deliveryDate(
        _ instant: Date,
        locale: Locale,
        timeZone: TimeZone
    ) -> String {
        instant.formatted(
            Date.FormatStyle(date: .long, time: .omitted)
                .locale(locale)
                .timeZone(timeZone)
        )
    }
}
```

Domain quyết định currency code và business time zone; presentation nhận chúng explicit. Không parse lại chuỗi đã format để tính toán.

### String Catalog và plural

Mỗi key cần comment nói context, parameter semantics và nơi hiển thị. Dùng localized interpolation/variation để Xcode tạo plural forms, điền mọi category mà ngôn ngữ yêu cầu và luôn có `other`. Không reuse một từ ngắn cho title, verb và accessibility label nếu grammar/context khác.

Server nên gửi event data (`orderID`, quantity, status) hoặc localization key đã version với arguments primitive; client render theo catalog. Nếu server gửi toàn bộ copy, server chịu trách nhiệm locale selection, fallback, audit và consistency giữa push/in-app—not một contract nửa vời.

### RTL và layout

Dùng leading/trailing thay left/right. Kiểm tra `layoutDirection`, `semanticContentAttribute` chỉ khi component có semantic đặc biệt. Giữ số/mã trong isolation phù hợp để bidirectional algorithm không làm khó đọc. Asset chứa text phải localize hoặc loại bỏ text khỏi image. Screenshot test không thay được review bởi người bản địa, nhưng bắt được clipping, overlap và sai mirror.

### Testing matrix

Không nhân mọi test với mọi locale. Chọn lớp:

- unit: formatters với fixed locale/time zone/calendar;
- catalog lint: missing/stale/untranslated key và placeholder mismatch;
- snapshot: English dài, German/French expansion, Arabic/Hebrew RTL, Japanese/CJK;
- UI/E2E: checkout, permission, error và restore flow ở locale rủi ro;
- manual/native review: meaning, tone, legal/payment copy và accessibility speech.

Pseudo-localization hoặc launch arguments giúp kéo dài string và thêm dấu để lộ hard-code. Test ngày gần DST, cuối năm, calendar khác và currency không có/khác minor units.

## Production Case

### Context

Order cutoff là 23:00 JST, app dùng ở nhiều múi giờ.

### Symptom

User tại California thấy ngày giao hàng sớm hơn một ngày; analytics chỉ log localized label nên không group được lỗi.

### Investigation

Team log semantic delivery instant, business time zone ID, locale ID và formatted-screen version. Formatter dùng `.current` time zone trong view, trong khi backend contract định nghĩa ngày theo warehouse JST.

### Root Cause

Time zone là hidden dependency và formatted copy được dùng như analytics dimension.

### Fix

Domain trả instant + warehouse time zone; formatter nhận dependency explicit; analytics log status code/instant thay vì chuỗi dịch.

### Prevention

Unit test quanh midnight/DST, localization screenshot matrix và review checklist cấm domain/analytics phụ thuộc localized string.

## Interview Questions

### Foundation

**Localization khác internationalization?** Internationalization tạo khả năng thích nghi; localization cung cấp translation/adaptation cho locale cụ thể.

### Middle

**Vì sao không nối `count + " items"`?** Grammar và plural categories khác theo ngôn ngữ; parameter order cũng thay đổi.

### Senior

**Thiết kế localization cho app 20 thị trường?** Nói về semantic keys, catalog ownership, translator context, server/client contract, locale-aware data, RTL/accessibility, automation, native QA và staged rollout.

## Exercises

### Easy

Chuyển ba chuỗi nối thành String Catalog có interpolation và plural.

### Medium

Viết formatter test cho JPY, USD, VND, Arabic locale và hai time zone.

### Hard

Thiết kế CI gate phát hiện missing translation, placeholder mismatch, clipping và stale key.

### Debugging Lab

Chạy checkout với pseudo-language, Arabic RTL, Japanese và Dynamic Type accessibility size; ghi screenshot và lỗi semantic.

## Cheat Sheet

```text
Domain data          → semantic value, không formatted string
String Catalog       → stable key + comment + variants
Plural               → grammar rule của locale, không if count == 1
Layout               → leading/trailing + flexible size
RTL                  → semantic mirror, có ngoại lệ
Testing              → unit format + lint + snapshot + E2E + native review
```

## Chapter Summary

1. Localization là data/layout/workflow problem, không chỉ dịch câu.
2. Locale, region, calendar và time zone phải được mô hình hóa rõ.
3. String Catalog và plural variation bảo vệ grammar contract.
4. RTL cần semantic direction, không mirror mù quáng.
5. Release gate phải đo completeness, layout và critical business copy.

## Related Chapters

- [String, Unicode và indexing](../Phase-01-Swift-Foundation/17-string-unicode-va-indexing.md)
- [HIG in practice](25-human-interface-guidelines-in-practice-navigation-modality-controls-va-feedback.md)
- [E2E automation](../Phase-08-Testing/15-e2e-automation-voi-xcuitest-fixtures-stability-va-ci.md)

## References

- [Apple — Localization](https://developer.apple.com/documentation/xcode/localization)
- [Apple — Localizing and varying text with a string catalog](https://developer.apple.com/documentation/xcode/localizing-and-varying-text-with-a-string-catalog)
- [Apple — Localizing strings that contain plurals](https://developer.apple.com/documentation/xcode/localizing-strings-that-contain-plurals)
- [Apple HIG — Right to left](https://developer.apple.com/design/human-interface-guidelines/right-to-left)
