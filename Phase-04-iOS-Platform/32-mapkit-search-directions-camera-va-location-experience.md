---
title: "MapKit: search, directions, camera và location experience"
phase: "iOS Platform"
difficulty: 4
importance: 3
interview_frequency: 3
status: complete
last_verified: 2026-08-09
swift_baseline: "Swift 6.3 toolchain; Swift 6 language mode"
levels:
  - L3
  - L4
prerequisites:
  - "CoreLocation: permission, accuracy, background và energy"
  - "Search autocomplete"
used_later:
  - "Mobile System Design interview"
competencies:
  - "iOS Platform"
  - "User Interface"
  - "Networking"
  - "Performance"
tags:
  - "mapkit"
  - "maps"
  - "local-search"
  - "directions"
---

# MapKit: search, directions, camera và location experience

> **Version scope**
>
> Bao phủ MapKit cho SwiftUI/UIKit theo capability, không phụ thuộc một initializer cụ thể. Search/directions/Look Around/coverage thay đổi theo region, OS và network. Xác minh 2026-08-09.

## Story / Problem

Màn chọn địa chỉ tự động zoom lại vị trí user sau mỗi location update, khiến họ không thể kéo map. Search gửi request cho từng ký tự, kết quả cũ ghi đè query mới. Route được vẽ như đường thẳng trong khi ETA đã stale. Đây là xung đột ownership: system, user gesture, search result và business selection cùng mutate camera/state mà không có policy.

```text
Location signal / search / user gesture / selected place
                         ↓
              map state + camera policy
                         ↓
      annotations / overlays / route / accessible alternative
```

## Objectives

Sau chapter này, bạn có thể:

- tách CoreLocation signal khỏi MapKit presentation;
- mô hình hóa camera ownership và user-interaction state;
- xây search/autocomplete có debounce, cancellation, region bias và stale-result protection;
- hiển thị annotation/overlay/directions với stable identity và resource budget;
- xử lý permission denied, no coverage, offline, route stale và accessibility fallback;
- tránh log/lưu location nhạy cảm không cần thiết.

## Prerequisites

- [CoreLocation](22-corelocation-permission-accuracy-background-va-energy.md).
- [Search autocomplete](../Phase-10-Mobile-System-Design/14-search-autocomplete.md).
- [Cancellation từ screen đến URLSession](../Phase-05-Networking/08-cancellation-tu-screen-en-urlsession.md).

## Used Later

- [Mobile System Design interview](../Phase-11-Interview/14-mobile-system-design-interview.md).
- [Battery và energy diagnostics](../Phase-09-Production/13-battery-va-energy-diagnostics.md).

## Mental Model

```text
User location = noisy, permission-scoped signal
Map camera    = UI state có owner/policy
Place         = semantic selection, không chỉ coordinate
Route/ETA     = network-derived snapshot có timestamp
```

Coordinate không đủ cho address/business identity. Một địa điểm cần stable app ID khi có, map item/placemark metadata và validation với backend coverage. Search region chỉ bias, không phải security boundary.

## What?

MapKit hiển thị map, annotation, overlay, search completion, local search, directions và Look Around theo availability. CoreLocation cung cấp location/authorization; MapKit dùng chúng để render hoặc query. App nên có `MapViewState` riêng: camera, selected place, userInteraction mode, loading/result/error và route version.

Camera policy ví dụ: lần đầu center vào user; sau gesture chuyển sang user-controlled; nút Recenter trả control cho app; selection có thể fit bounding region; location update không giành lại camera tự động.

## Why?

Location update tần suất cao không cần render/recenter tương ứng. Nhiều annotation với view nặng làm hitch; unstable identity khiến marker nhấp nháy. Autocomplete response đến out-of-order làm chọn sai địa điểm. Route request có cost/network và ETA nhanh stale. App map-only cũng khó dùng với VoiceOver nếu thiếu danh sách địa điểm tương đương.

## How?

```swift
import MapKit

struct Place: Identifiable, Equatable {
    let id: String
    let name: String
    let coordinate: CLLocationCoordinate2D

    static func == (lhs: Place, rhs: Place) -> Bool {
        lhs.id == rhs.id &&
        lhs.coordinate.latitude == rhs.coordinate.latitude &&
        lhs.coordinate.longitude == rhs.coordinate.longitude
    }
}

enum CameraOwner {
    case initialLocation
    case userGesture
    case selectedPlace
    case recenterAction
}
```

Giữ `CameraOwner`/generation trong state machine. Map callbacks biến thành event; reducer quyết định camera transition. Không để location service gọi trực tiếp `setRegion`.

### Search và selection

Debounce input, cancel query cũ và gắn generation. `MKLocalSearchCompleter` trả suggestions; completion được resolve thành search/map item trước khi commit. Bias bằng visible region nhưng validate service area ở domain/backend. Empty, partial address, no network và unsupported region cần state riêng.

### Annotation, overlay và route

Identifier dựa domain ID, không dựa index. Cluster khi density cao; render overlay path có simplification/zoom strategy nếu data lớn. Directions request chỉ chạy khi endpoints stable, cancel khi thay selection, lưu request version/timestamp và đánh dấu stale. Route là suggestion theo service/coverage; không dùng như guarantee an toàn hoặc pháp lý.

### Accessibility và privacy

Cung cấp list/sheet đồng bộ với marker, accessibility label chứa tên/khoảng cách/status và action chọn địa điểm. Không biểu đạt status chỉ bằng màu. Xin location khi feature cần, hỗ trợ nhập/search thủ công khi denied. Giảm precision/retention trong analytics; không log coordinate raw nếu chỉ cần region bucket.

## Production Case

### Context

User chọn cửa hàng nhận hàng, search trong vùng map.

### Symptom

Sau khi gõ nhanh “Shinjuku”, list quay lại kết quả query “Shin”; map nhảy về user location giữa lúc chọn store.

### Investigation

Timeline log query generation, completion time, camera owner và location timestamp cho thấy request cũ không bị cancel/guard; location callback luôn set camera.

### Root Cause

Thiếu generation cho async search và camera ownership policy.

### Fix

Reducer bỏ response không khớp generation; user gesture giữ camera ownership cho đến explicit Recenter/selection.

### Prevention

Async ordering test, UI test typing nhanh/pan map, metric search-to-selection latency và camera override count.

## Interview Questions

### Foundation

**CoreLocation và MapKit khác vai trò?** CoreLocation cung cấp location/permission; MapKit cung cấp map/search/directions presentation/service.

### Middle

**Ngăn map tự nhảy khi user pan thế nào?** Mô hình camera owner; location update chỉ thay signal, không luôn mutate camera.

### Senior

**Thiết kế store locator toàn cầu?** Region-biased cancellable search, backend coverage, clustering, stable selection, permission fallback, accessibility, privacy, cache/staleness và observability.

## Exercises

### Easy

Thiết kế state cho initial center, pan và recenter.

### Medium

Viết generation guard cho autocomplete response out-of-order.

### Hard

Thiết kế map data pipeline cho 50.000 điểm với viewport query, clustering, caching và offline fallback.

### Debugging Lab

Throttle network, type/pan/select liên tục và chứng minh selection/camera không bị response cũ ghi đè.

## Cheat Sheet

```text
CoreLocation      → permission + location signal
MapKit            → map/search/directions
camera            → explicit owner
search            → debounce + cancel + generation
annotation        → stable ID + cluster
route/ETA         → versioned, timestamped, stale-able
accessibility     → list/action alternative
privacy           → minimize precision + retention
```

## Chapter Summary

1. Location signal và map camera là hai state khác nhau.
2. User gesture cần ownership rõ để không bị system update giành lại.
3. Search/directions là async snapshot cần cancellation và staleness.
4. Stable identity, clustering và resource budget bảo vệ performance.
5. Permission fallback, accessibility và privacy là phần của map architecture.

## Related Chapters

- [CoreLocation](22-corelocation-permission-accuracy-background-va-energy.md)
- [Search autocomplete](../Phase-10-Mobile-System-Design/14-search-autocomplete.md)
- [Typed navigation](16-navigationstack-va-typed-navigation.md)

## References

- [Apple — MapKit](https://developer.apple.com/documentation/mapkit)
- [Apple — MKLocalSearch](https://developer.apple.com/documentation/mapkit/mklocalsearch)
- [Apple — MKDirections](https://developer.apple.com/documentation/mapkit/mkdirections)
- [Apple HIG — Maps](https://developer.apple.com/design/human-interface-guidelines/maps)
