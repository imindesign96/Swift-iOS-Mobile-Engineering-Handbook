# Phase 04 — iOS Platform

Phase này giải thích runtime/lifecycle của UIKit và mô hình cập nhật declarative của SwiftUI mà không nhân đôi toàn bộ ứng dụng.

```text
App/Scene lifecycle
  ├── UIKit: UIView → UIViewController → Navigation → Reuse/Layout
  └── SwiftUI: State → Observation → body evaluation → reconciliation
```

Kết thúc phase, người học phải đặt đúng công việc vào lifecycle, làm chủ identity/state ownership, tránh work nặng trên UI isolation và nối được UIKit với SwiftUI trong migration thực tế.

Roadmap chi tiết nằm trong [SUMMARY](../SUMMARY.md).

