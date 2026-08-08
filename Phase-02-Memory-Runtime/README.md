# Phase 02 — Memory & Runtime

Phase này trả lời bốn câu hỏi cho mọi object graph: ai tạo, ai sở hữu, ai giải phóng và khi nào `deinit` phải chạy.

```text
Value/Reference Semantics
        ↓
Stack/Heap mental model → Copy-on-Write
        ↓
ARC → strong/weak/unowned → closure capture
        ↓
Ownership graph → retain cycle → Memory Graph / Instruments
```

Kết thúc phase, người học phải phân biệt được leak với memory pressure, phân tích retain cycle bằng graph thay vì áp dụng `[weak self]` máy móc, và điều tra được screen không giải phóng sau khi dismiss/pop.

> **Production**
>
> Domain xuyên suốt là vòng đời `ProductDetail`, delegate, observer, timer và async task trong Global Commerce.

Roadmap chi tiết nằm trong [SUMMARY](../SUMMARY.md).

