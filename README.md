# Swift / iOS Mobile Engineering Handbook

Handbook Swift/iOS bằng tiếng Việt, đi từ Foundation đến Senior/Global Interview theo hướng **hiểu bản chất, production-first và evidence-driven debugging**.

**Website:** [imindesign96.github.io/Swift-iOS-Mobile-Engineering-Handbook](https://imindesign96.github.io/Swift-iOS-Mobile-Engineering-Handbook/)

Đây không phải cheat sheet. Repository được thiết kế để dùng đồng thời như:

1. một cuốn sách đọc tuần tự;
2. một reference tra cứu theo vấn đề;
3. lộ trình luyện phỏng vấn iOS toàn cầu;
4. production debugging playbook;
5. curriculum thực hành với coding exercise, debugging lab và system design.

## Trạng thái hiện tại

| Hạng mục | Trạng thái |
|---|---|
| Repository skeleton 11 Phase | ✅ Hoàn thành |
| 183 chapter và 11 Phase Review | ✅ Hoàn thành |
| Website/search/navigation | ✅ GitHub Pages tự động deploy |

Repository hiện có đủ **183 chapter** theo [SUMMARY](SUMMARY.md). Mỗi chapter gồm mental model, runtime/memory/concurrency implications, production case, debugging evidence, interview prompts, exercises, cheat sheet và primary references.

## Bắt đầu đọc

- Đọc tuần tự: [Một chương trình Swift chạy như thế nào?](Phase-01-Swift-Foundation/01-how-a-swift-program-runs.md)
- Xem toàn bộ knowledge map và trạng thái: [SUMMARY](SUMMARY.md)
- Tra cứu thuật ngữ: [GLOSSARY](GLOSSARY.md)
- Đi từ symptom production đến chapter liên quan: [CROSS REFERENCE INDEX](CROSS_REFERENCE_INDEX.md)
- Kiểm tra coverage toàn bộ catalog: [HANDBOOK COVERAGE](HANDBOOK_COVERAGE.md)
- Xử lý incident: [PRODUCTION PLAYBOOK](PRODUCTION_PLAYBOOK.md)
- Chuẩn bị phỏng vấn: [INTERVIEW PLAYBOOK](INTERVIEW_PLAYBOOK.md)

## Learning paths

### Foundation / Fresher

```text
Phase 01 Swift Foundation
  ↓
Phase 04 iOS Platform (core UI)
  ↓
Phase 05 Networking (fundamentals)
  ↓
Phase 08 Testing (unit basics)
  ↓
Phase 11 Junior interview review
```

### Junior → Middle

```text
Phase 02 Memory & Runtime
  ↓
Phase 03 Concurrency
  ↓
Phase 05 Networking (resilience/auth)
  ↓
Phase 06 Architecture → Phase 07 Persistence
  ↓
Phase 09 Production
```

### Senior / Staff-oriented

```text
Revisit Memory + Concurrency failure modes
  ↓
Architecture trade-offs + modularization
  ↓
Production/observability
  ↓
Mobile System Design
  ↓
Senior interview synthesis
```

## Một domain xuyên suốt

Ví dụ dùng **Global Commerce iOS App**:

```text
Authentication · Profile · Product Catalog · Search · Favorites
Cart · Checkout · Payment · Orders · Notifications · Offline Cache
```

Cùng một domain giúp người đọc nhìn thấy một khái niệm tiến hóa: `Product` bắt đầu là model thuần Swift, đi qua repository/network/cache, vào UI, chịu concurrency, rồi xuất hiện trong production incident và system design.

## Baseline kỹ thuật

- Ưu tiên Swift 6 language mode và convention hiện đại.
- Tại lần xác minh ngày **2026-08-08**, Swift stable hiện hành là **6.3.3**; material beta/snapshot (ví dụ 6.4) không được dùng làm baseline mặc định.
- Luôn phân biệt **compiler/toolchain version** với **language mode**.
- Claim phụ thuộc phiên bản phải ghi rõ availability và ưu tiên nguồn Apple/Swift chính thức.
- Behavior được document và inference từ implementation phải được dán nhãn khác nhau.

Nguồn baseline: [Swift 6.3 release](https://www.swift.org/blog/swift-6.3-released/), [Swift install](https://www.swift.org/install/), [Migrating to Swift 6](https://www.swift.org/migration/), [The Swift Programming Language](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/).

## Tiêu chuẩn một chapter

Chapter quan trọng phải đi theo luồng:

```text
Story/Problem → Objectives → Prerequisites/Used Later → Mental Model
→ What/Why/How/When/What-if → Runnable Swift
→ Runtime/Memory/Concurrency/Architecture
→ Production Case/Debugging → Mistakes/Practices
→ Interview → Exercises → Cheat Sheet → Summary → References
```

Checklist chi tiết nằm trong [SPECIFICATION](SPECIFICATION.md) và [chapter template](templates/chapter-template.md).

## Nguyên tắc viết và review

- Không dùng `TODO` để giả lập một chapter hoàn chỉnh.
- Không lặp định nghĩa; liên kết chapter prerequisite hoặc glossary.
- Không viết “always/never” khi quyết định phụ thuộc context.
- Code async luôn xét owner, isolation, cancellation, lifetime và ordering.
- Object graph luôn xét creator, owner, release và expected `deinit`.
- Production case luôn đi từ symptom đến evidence trước khi kết luận root cause.
- Example code phải có thể chạy hoặc nêu rõ framework/OS requirement.

## Nguồn gốc cấu trúc

Repository tham khảo trải nghiệm đọc và cách tổ chức knowledge graph từ [Java Backend Engineering Handbook](https://github.com/makumawari/java-backend-interview-handbook), nhưng cấu trúc 11 Phase, scope và quality gate của repository này tuân theo [Swift/iOS specification](SPECIFICATION.md).
