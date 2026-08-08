# Phase 01 — Swift Foundation

Phase này xây nền ngôn ngữ trước khi chạm vào framework. Đích đến không phải nhớ cú pháp, mà là giải thích được type safety, Optional, value/reference semantics, protocol, generics và error handling tác động ra sao đến code iOS.

## Dependency map

```text
Program execution
  ↓
Types → Optional → Control flow → Functions → Closures
  ↓                                      ↓
Enum → Struct/Class → Value/Reference → Protocol
                                      ↓
                         Generics → associatedtype → some/any
                                      ↓
                    Error handling → Collections → Codable
```

## Learning outcomes

Sau phase này, người học có thể:

- đọc và viết pure Swift trong domain Global Commerce;
- chọn Optional thay vì sentinel value và xử lý nil có chủ đích;
- phân biệt equality với identity;
- chọn struct hoặc class theo semantics của domain;
- dùng protocol/generic mà không che giấu trade-off;
- mô hình hóa lỗi thay vì dùng chuỗi hoặc `try!` tùy tiện.

## Status

Chương 01–03 đã hoàn chỉnh. Các chapter còn lại được quản lý trong [SUMMARY](../SUMMARY.md) và chỉ có file khi nội dung vượt quality gate.
