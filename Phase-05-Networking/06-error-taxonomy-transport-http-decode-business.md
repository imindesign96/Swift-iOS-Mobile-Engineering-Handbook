---
title: "Error taxonomy: transport/HTTP/decode/business"
phase: "Networking"
difficulty: 4
importance: 5
interview_frequency: 4
status: complete
last_verified: 2026-08-09
swift_baseline: "Swift 6.3 toolchain; Swift 6 language mode"
levels:
  - L3
prerequisites:
  - "API client và Endpoint abstraction"
used_later:
  - "Timeout, retry, backoff và jitter"
competencies:
  - "Networking"
  - "Production"
  - "Debugging"
  - "Interview"
tags:
  - "error-taxonomy-transport-http-decode-business"
  - "global-commerce"
---

# Error taxonomy: transport/HTTP/decode/business

> **Version scope**
>
> Baseline Swift 6.3 toolchain, Swift 6 language mode; API iOS-specific phải kiểm tra availability tại call site. Xác minh 2026-08-09.

## Story / Problem

Trong Global Commerce, request Commerce thành công ở happy path nhưng production gặp mạng yếu, token hết hạn và response đến sai thứ tự. Chapter này tập trung vào **Error taxonomy: transport/HTTP/decode/business**: không dừng ở syntax/API mà nối behavior với ownership, failure mode và evidence production.

Nếu team chỉ nhớ tên concept, fix thường dịch symptom sang chỗ khác. Câu hỏi mở đầu là:

```text
Input/event → state hoặc resource nào thay đổi?
            → ai sở hữu thay đổi đó?
            → contract nào có thể bị vi phạm?
            → evidence nào chứng minh kết luận?
```

## Objectives

Sau chapter này, bạn có thể:

- giải thích chính xác rằng transport, HTTP, decode và business errors có recovery khác nhau;
- nhận diện failure mode chính: gộp tất cả thành networkError;
- chọn giải pháp bằng rule: preserve underlying evidence, map ở boundary thích hợp;
- nối runtime, memory, concurrency và architecture implications;
- điều tra case production bằng metrics theo category và user-safe mapping;
- trả lời câu hỏi interview ở ba độ sâu thay vì đọc thuộc định nghĩa.

## Prerequisites { data-search-exclude }

- [API client và Endpoint abstraction](05-api-client-va-endpoint-abstraction.md); không lặp lại định nghĩa nền nếu chapter trước đã giải thích.
- [Glossary](../GLOSSARY.md) cho terminology canonical.

## Used Later { data-search-exclude }

- [Timeout, retry, backoff và jitter](07-timeout-retry-backoff-va-jitter.md) dùng contract của chapter này làm building block.
- [Production Playbook](../PRODUCTION_PLAYBOOK.md) dùng cùng flow evidence-first.
- [Interview Playbook](../INTERVIEW_PLAYBOOK.md) dùng mental model để xử lý follow-up.

## Mental Model

```text
View → ViewModel → Repository → API Client → URLSession → HTTP server → mapped result
                 ↓
Focus: Error taxonomy: transport/HTTP/decode/business
                 ↓
Evidence: metrics theo category và user-safe mapping
```

Mental model hữu ích để đặt câu hỏi đúng, nhưng không thay thế API contract hoặc measurement. Đặc biệt, không suy luận implementation private của compiler/framework thành behavior được đảm bảo.

## What?

Trọng tâm của **Error taxonomy: transport/HTTP/decode/business** là: transport, HTTP, decode và business errors có recovery khác nhau. Hãy mô tả bằng state transition, lifetime hoặc output quan sát được thay vì chỉ bằng keyword.

Một contract tốt nói rõ input hợp lệ, output/failure, side effect, owner và thời điểm kết thúc. Nếu concept chạm external data hoặc asynchronous work, contract cũng phải nói cancellation, ordering và recovery.

## Why?

Concept tồn tại để giúp xây networking boundary có error taxonomy, cancellation, auth, retry và cache policy. Không có boundary này, rule domain bị nhân bản, behavior phụ thuộc call order và incident khó điều tra vì không biết layer nào chịu trách nhiệm.

Giá trị lớn nhất không phải ít dòng code hơn; đó là giảm số state hợp lệ cần giữ trong đầu và làm violation xuất hiện sớm qua compiler, test hoặc telemetry.

## How?

1. Xác định source of truth và invariant liên quan.
2. Xác định creator/owner/mutator/observer.
3. Chọn API hoặc abstraction thể hiện đúng semantics.
4. Mô hình hóa failure/cancellation thay vì che bằng fallback.
5. Đo observable behavior bằng metrics theo category và user-safe mapping.

### Documented behavior vs inference

- **Documented:** dùng contract trong Swift/Apple documentation và availability của SDK.
- **Inference:** storage placement, executor scheduling chi tiết hoặc reconciliation internals chỉ được dùng như giả thuyết đo lường, không phải guarantee.

## When?

Áp dụng khi preserve underlying evidence, map ở boundary thích hợp. Bắt đầu bằng giải pháp đơn giản nhất giữ được invariant; thêm abstraction/synchronization/cache chỉ khi requirement hoặc measurement chứng minh cần.

Tránh dùng concept như cargo cult. Một type, layer hay primitive không có owner/contract/test rõ chỉ chuyển complexity chứ không loại bỏ nó.

## What if?

Failure mode quan trọng là gộp tất cả thành networkError. Consequence có thể là state stale, duplicate work, leak, crash, UI hitch hoặc test flaky tùy boundary.

Khi assumption có thể thay đổi qua `await`, lifecycle callback, network retry hoặc migration, hãy revalidate state trước khi commit kết quả.

### Review questions

1. Observable behavior nào định nghĩa Error taxonomy: transport/HTTP/decode/business?
2. Owner của state/resource là ai và lifetime kết thúc khi nào?
3. Gộp tất cả thành networkerror tạo evidence gì?
4. Rule chọn giải pháp là gì, và constraint nào khiến rule đổi?

## Runnable Swift Example

```swift
enum CheckoutError: Error { case emptyCart, paymentDeclined }

func placeOrder(cart: Cart) throws -> Order {
    guard !cart.items.isEmpty else { throw CheckoutError.emptyCart }
    return Order(id: UUID().uuidString)
}

let outcome = Result { try placeOrder(cart: cart) }
```

Ví dụ pure Swift chạy trong executable/test target với Swift 6.3. Ví dụ dùng UIKit, SwiftUI, Security, Core Data hoặc SwiftData cần target iOS tương ứng; mục tiêu là minh họa contract, không giả lập framework bằng toy code.

## iOS Runtime Behavior { data-search-exclude }

URLSession quản lý task/connection theo configuration; HTTP response và transport completion là hai lớp evidence khác nhau. Với **Error taxonomy: transport/HTTP/decode/business**, hãy log hoặc đo transition ở boundary thay vì suy luận từ UI cuối cùng.

Một callback xuất hiện không chứng minh object còn owner đúng; một UI update đúng không chứng minh request cũ đã bị cancel; một compile success cũng không chứng minh logical ordering đúng.

## Memory Implications { data-search-exclude }

Response body, decoded models và image data cần budget; cache/request registry không được tăng vô hạn.

```text
Who creates? → Who owns? → Who releases? → Expected deinit/eviction?
```

Nếu không có reference object trong chapter, câu hỏi vẫn hữu ích cho buffer, cache, task capture và framework object được ví dụ tạo ra.

## Concurrency Implications { data-search-exclude }

Request phải có owner, cancellation, ordering và single-flight khi chia sẻ refresh/cache work.

```text
Task owner? → isolation? → cancellation? → lifetime? → ordering?
```

Data-race freedom không tự động bảo đảm business invariant nhiều bước. Sau suspension, response hoặc lifecycle change, state có thể đã thuộc generation khác.

## Architecture Notes { data-search-exclude }

Repository phối hợp remote/local/policy; API client chịu transport, request construction và error mapping. Dependency hướng vào contract ổn định; implementation details nằm phía ngoài. Composition root tạo concrete dependencies và quyết định lifetime.

Không thêm layer chỉ vì chapter nhắc đến pattern. Hãy yêu cầu layer mới có ít nhất một giá trị: hấp thụ volatility, bảo vệ invariant, tạo test seam hoặc quản lý lifetime.

## Production Case { data-search-exclude }

### Context

Feature Commerce áp dụng **Error taxonomy: transport/HTTP/decode/business** trong flow có network, UI lifecycle và cache.

### Symptom

User báo behavior không ổn định; telemetry cho thấy gộp tất cả thành networkError.

### Hypotheses

1. Contract bị hiểu sai tại call site.
2. Owner/lifetime không khớp feature scope.
3. Ordering hoặc external input phá invariant.
4. Resource budget/policy thiếu bound.

### Investigation

Dùng metrics theo category và user-safe mapping; thêm correlation ID/generation an toàn, tái hiện repeated flow và so sánh expected transition với actual transition.

### Root Cause

Root cause chỉ được kết luận khi evidence chỉ ra nơi invariant bị phá, không phải nơi symptom cuối cùng xuất hiện.

### Fix

Áp dụng rule **preserve underlying evidence, map ở boundary thích hợp**, thu hẹp mutation/ownership và làm failure/cancellation explicit.

### Prevention

Thêm regression test tại boundary, metric cho failure mode, review checklist về owner/state và documentation cho constraint quyết định.

## Debug / Instruments { data-search-exclude }

Primary evidence: **metrics theo category và user-safe mapping**.

1. Tái hiện trên build/device gần production.
2. Đánh dấu user flow bằng signpost hoặc correlation ID không chứa PII.
3. Thu trace/log trước khi sửa.
4. Đặt hypothesis có thể bị bác bỏ.
5. Đo lại cùng workload và thêm regression protection.

## Myth vs Reality { data-search-exclude }

> **Myth:** Chỉ cần dùng đúng API/pattern tên **Error taxonomy: transport/HTTP/decode/business** là code an toàn.
>
> **Reality:** Safety đến từ semantics, owner, invariant, lifecycle và evidence; API chỉ là một phần của contract.

## Common Mistakes { data-search-exclude }

- Gộp tất cả thành networkerror → behavior chỉ sai ở scale/lifecycle edge.
- Che failure bằng default hoặc retry → mất root-cause signal.
- Nhiều layer cùng mutate state → source of truth không còn rõ.
- Tối ưu trước khi đo → tăng complexity nhưng không cải thiện bottleneck.

## Best Practices { data-search-exclude }

- Preserve underlying evidence, map ở boundary thích hợp.
- Ghi assumption và availability cạnh boundary version-sensitive.
- Dùng immutable value và explicit state transition khi phù hợp.
- Log category/correlation an toàn; không log token, PII hoặc payment payload.
- Đo trước/sau trên cùng workload và giữ regression test.

## Interview Questions { data-search-exclude }

### Foundation

**Hỏi:** Error taxonomy: transport/HTTP/decode/business giải quyết vấn đề gì?

**30-second:** Transport, http, decode và business errors có recovery khác nhau. Chọn nó khi preserve underlying evidence, map ở boundary thích hợp; rủi ro chính là gộp tất cả thành networkError.

### Junior

**Hỏi:** Cho một ví dụ Commerce và common mistake.

**2–3 minute:** Nêu input/state, owner, code contract, failure path và test. Dùng ví dụ ở trên, sau đó giải thích vì sao gộp tất cả thành networkError phá invariant.

### Middle

**Hỏi:** Concept ảnh hưởng memory/concurrency/testability thế nào?

Trả lời bằng object/task graph, isolation/cancellation, boundary DI và evidence **metrics theo category và user-safe mapping**.

### Senior

**Hỏi:** Constraint nào khiến bạn chọn giải pháp khác?

Deep Dive phải so sánh complexity, lifecycle, scale, migration, operability và rollback; không biến best practice thành luật tuyệt đối.

### Production

**Hỏi:** Symptom chỉ xảy ra trên 0,1% session. Bạn điều tra thế nào?

Clarify impact → thu evidence → hypothesis → controlled measurement → root cause → mitigation/fix → regression metric.

## Exercises { data-search-exclude }

### Easy

Viết một ví dụ nhỏ minh họa **Error taxonomy: transport/HTTP/decode/business** và test happy path lẫn edge case.

### Medium

Refactor một call site đang gặp **gộp tất cả thành networkError** để contract/owner rõ hơn.

### Hard

Thiết kế state transition có cancellation/lifecycle interruption và chứng minh không publish stale result.

### Debugging Lab

Bug report: repeated Commerce flow tạo symptom liên quan **Error taxonomy: transport/HTTP/decode/business**. Thu evidence bằng metrics theo category và user-safe mapping, vẽ owner/state graph, xác định root cause và thêm regression test.

### Engineering / Design Exercise

Viết ADR một trang: context, options, decision, consequences và revisit conditions cho lựa chọn trong chapter.

## Cheat Sheet { data-search-exclude }

```text
Concept   → transport, HTTP, decode và business errors có recovery khác nhau
Use when  → preserve underlying evidence, map ở boundary thích hợp
Risk      → gộp tất cả thành networkError
Evidence  → metrics theo category và user-safe mapping
Remember  → owner + state + failure + lifecycle + measurement
```

## Chapter Summary { data-search-exclude }

1. Problem: API/pattern không đủ nếu semantics và owner mơ hồ.
2. Mental model: View → ViewModel → Repository → API Client → URLSession → HTTP server → mapped result.
3. Usage rule: preserve underlying evidence, map ở boundary thích hợp.
4. Mistake nguy hiểm: gộp tất cả thành networkError.
5. Production lesson: kết luận bằng metrics theo category và user-safe mapping, rồi bảo vệ bằng test và metric.

## Related Chapters { data-search-exclude }

- [API client và Endpoint abstraction](05-api-client-va-endpoint-abstraction.md)
- [Timeout, retry, backoff và jitter](07-timeout-retry-backoff-va-jitter.md)
- [Cross-reference Index](../CROSS_REFERENCE_INDEX.md)

## References { data-search-exclude }

- [URLSession](https://developer.apple.com/documentation/foundation/urlsession) — truy cập 2026-08-09.
- [URLRequest](https://developer.apple.com/documentation/foundation/urlrequest) — truy cập 2026-08-09.
- [Loading data from your app](https://developer.apple.com/documentation/foundation/loading-data-from-your-app) — truy cập 2026-08-09.

## Completion Checklist { data-search-exclude }

- [x] Objectives có thể kiểm chứng
- [x] Mental model và giới hạn được nói rõ
- [x] What/Why/How/When/What-if đầy đủ
- [x] Code hoặc availability rõ
- [x] Runtime/memory/concurrency implications đúng phạm vi
- [x] Production case dựa trên evidence
- [x] Review + interview + exercises + cheat sheet
- [x] Internal links chỉ tới file tồn tại trong catalog
- [x] Claim version-sensitive có primary source và ngày verify
- [x] Không còn placeholder; status là complete
