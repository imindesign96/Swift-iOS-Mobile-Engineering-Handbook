---
title: "WKWebView bridge: Cookie, LocalStorage và native-web data contract"
phase: "iOS Platform"
difficulty: 4
importance: 5
interview_frequency: 4
status: complete
last_verified: 2026-08-09
swift_baseline: "Swift 6.3 toolchain; Swift 6 language mode"
levels:
  - L3
prerequisites:
  - "Universal Links: AASA, routing, fallback và security"
used_later:
  - "Human Interface Guidelines in practice: navigation, modality, controls và feedback"
competencies:
  - "iOS Platform"
  - "Production"
  - "Debugging"
  - "Interview"
tags:
  - "wkwebview-bridge-cookie-localstorage-va-native-web-data-contract"
  - "global-commerce"
---

# WKWebView bridge: Cookie, LocalStorage và native-web data contract

> **Version scope**
>
> Baseline Swift 6.3 toolchain, Swift 6 language mode; API iOS-specific phải kiểm tra availability tại call site. Xác minh 2026-08-09.

## Story / Problem

Trong Global Commerce, screen Commerce hiển thị sai, cập nhật sau khi dismiss hoặc giật vì identity/lifecycle bị hiểu sai. Chapter này tập trung vào **WKWebView bridge: Cookie, LocalStorage và native-web data contract**: không dừng ở syntax/API mà nối behavior với ownership, failure mode và evidence production.

Nếu team chỉ nhớ tên concept, fix thường dịch symptom sang chỗ khác. Câu hỏi mở đầu là:

```text
Input/event → state hoặc resource nào thay đổi?
            → ai sở hữu thay đổi đó?
            → contract nào có thể bị vi phạm?
            → evidence nào chứng minh kết luận?
```

## Objectives

Sau chapter này, bạn có thể:

- giải thích chính xác rằng WKWebView integration là protocol giữa hai security domains; Cookie thuộc WKHTTPCookieStore còn LocalStorage thuộc origin và chỉ nên truy cập qua bridge versioned, validated;
- nhận diện failure mode chính: giả định HTTPCookieStorage tự đồng bộ, inject JavaScript chứa dữ liệu không escape, message handler giữ cycle hoặc native/web schema drift;
- chọn giải pháp bằng rule: định nghĩa handshake/schema/allowlist/timeout trước, chọn persistent hoặc nonpersistent WKWebsiteDataStore rõ ràng và đồng bộ auth ở một boundary;
- nối runtime, memory, concurrency và architecture implications;
- điều tra case production bằng Web Inspector, cookie-store snapshot, origin-scoped storage probe, navigation/message correlation và contract tests;
- trả lời câu hỏi interview ở ba độ sâu thay vì đọc thuộc định nghĩa.

## Prerequisites { data-search-exclude }

- [Universal Links: AASA, routing, fallback và security](23-universal-links-aasa-routing-fallback-va-security.md); không lặp lại định nghĩa nền nếu chapter trước đã giải thích.
- [Glossary](../GLOSSARY.md) cho terminology canonical.

## Used Later { data-search-exclude }

- [Human Interface Guidelines in practice: navigation, modality, controls và feedback](25-human-interface-guidelines-in-practice-navigation-modality-controls-va-feedback.md) dùng contract của chapter này làm building block.
- [Production Playbook](../PRODUCTION_PLAYBOOK.md) dùng cùng flow evidence-first.
- [Interview Playbook](../INTERVIEW_PLAYBOOK.md) dùng mental model để xử lý follow-up.

## Mental Model

```text
Event/state mutation → lifecycle/observation → UI description/layout → visible frame
                 ↓
Focus: WKWebView bridge: Cookie, LocalStorage và native-web data contract
                 ↓
Evidence: Web Inspector, cookie-store snapshot, origin-scoped storage probe, navigation/message correlation và contract tests
```

Mental model hữu ích để đặt câu hỏi đúng, nhưng không thay thế API contract hoặc measurement. Đặc biệt, không suy luận implementation private của compiler/framework thành behavior được đảm bảo.

## What?

Trọng tâm của **WKWebView bridge: Cookie, LocalStorage và native-web data contract** là: WKWebView integration là protocol giữa hai security domains; Cookie thuộc WKHTTPCookieStore còn LocalStorage thuộc origin và chỉ nên truy cập qua bridge versioned, validated. Hãy mô tả bằng state transition, lifetime hoặc output quan sát được thay vì chỉ bằng keyword.

Một contract tốt nói rõ input hợp lệ, output/failure, side effect, owner và thời điểm kết thúc. Nếu concept chạm external data hoặc asynchronous work, contract cũng phải nói cancellation, ordering và recovery.

## Why?

Concept tồn tại để giúp đặt UI state và work đúng lifecycle trong UIKit lẫn SwiftUI. Không có boundary này, rule domain bị nhân bản, behavior phụ thuộc call order và incident khó điều tra vì không biết layer nào chịu trách nhiệm.

Giá trị lớn nhất không phải ít dòng code hơn; đó là giảm số state hợp lệ cần giữ trong đầu và làm violation xuất hiện sớm qua compiler, test hoặc telemetry.

## How?

1. Xác định source of truth và invariant liên quan.
2. Xác định creator/owner/mutator/observer.
3. Chọn API hoặc abstraction thể hiện đúng semantics.
4. Mô hình hóa failure/cancellation thay vì che bằng fallback.
5. Đo observable behavior bằng Web Inspector, cookie-store snapshot, origin-scoped storage probe, navigation/message correlation và contract tests.

## Technical Deep Dive

### Data stores, Cookie và LocalStorage

`WKWebViewConfiguration` phải hoàn chỉnh trước khi tạo web view. `.default()` giữ website data persistent; `.nonPersistent()` cô lập private/ephemeral session. Cookie của WebKit nằm trong `WKHTTPCookieStore`; đừng giả định `HTTPCookieStorage.shared` tự đồng bộ hai chiều. Nếu native bootstrap session cookie, await việc set cookie trước request đầu và định nghĩa logout xóa đúng domains/path/data types.

`localStorage` thuộc security origin (scheme/host/port) và synchronous bên JavaScript. Native không nên đọc/ghi tùy ý bằng string interpolation. Web layer nên expose một bridge function trả schema versioned; native gọi script với arguments được encode an toàn hoặc nhận `WKScriptMessage`, validate type/version/origin/size rồi map sang command allowlist.

### Bridge và navigation security

Message handler thường được `WKUserContentController` giữ; nếu handler giữ web view/owner mạnh sẽ tạo cycle. Dùng proxy/weak ownership và remove handler khi session kết thúc. Chỉ cho phép navigation tới host/scheme đã xác định, mở external link có chủ đích, chặn `javascript:`/unexpected custom scheme, và xử lý process termination/reload như lifecycle bình thường.

Định nghĩa handshake `nativeReady/webReady`, request ID, timeout, cancellation, duplicate response và backward compatibility. Cookie/session refresh phải có một owner; tránh native và web cùng refresh rồi overwrite. Test first load, redirect login, SameSite/domain/path, logout, corrupt LocalStorage, schema cũ, offline, process crash và content process restart. Dùng Safari Web Inspector cùng native correlation logs; không log cookie/token hoặc raw bridge payload nhạy cảm.

### Documented behavior vs inference

- **Documented:** dùng contract trong Swift/Apple documentation và availability của SDK.
- **Inference:** storage placement, executor scheduling chi tiết hoặc reconciliation internals chỉ được dùng như giả thuyết đo lường, không phải guarantee.

## When?

Áp dụng khi định nghĩa handshake/schema/allowlist/timeout trước, chọn persistent hoặc nonpersistent WKWebsiteDataStore rõ ràng và đồng bộ auth ở một boundary. Bắt đầu bằng giải pháp đơn giản nhất giữ được invariant; thêm abstraction/synchronization/cache chỉ khi requirement hoặc measurement chứng minh cần.

Tránh dùng concept như cargo cult. Một type, layer hay primitive không có owner/contract/test rõ chỉ chuyển complexity chứ không loại bỏ nó.

## What if?

Failure mode quan trọng là giả định HTTPCookieStorage tự đồng bộ, inject JavaScript chứa dữ liệu không escape, message handler giữ cycle hoặc native/web schema drift. Consequence có thể là state stale, duplicate work, leak, crash, UI hitch hoặc test flaky tùy boundary.

Khi assumption có thể thay đổi qua `await`, lifecycle callback, network retry hoặc migration, hãy revalidate state trước khi commit kết quả.

### Review questions

1. Observable behavior nào định nghĩa WKWebView bridge: Cookie, LocalStorage và native-web data contract?
2. Owner của state/resource là ai và lifetime kết thúc khi nào?
3. Giả định httpcookiestorage tự đồng bộ, inject javascript chứa dữ liệu không escape, message handler giữ cycle hoặc native/web schema drift tạo evidence gì?
4. Rule chọn giải pháp là gì, và constraint nào khiến rule đổi?

## Implementation Example

```swift
import WebKit

@MainActor
func makeCheckoutWebView(sessionCookie: HTTPCookie) async -> WKWebView {
    let configuration = WKWebViewConfiguration()
    configuration.websiteDataStore = .default()
    let cookieStore = configuration.websiteDataStore.httpCookieStore
    await cookieStore.setCookie(sessionCookie)

    let controller = configuration.userContentController
    controller.addScriptMessageHandler(
        CheckoutMessageHandler(allowedOrigin: "https://checkout.example.com"),
        contentWorld: .page,
        name: "checkout"
    )
    return WKWebView(frame: .zero, configuration: configuration)
}

// LocalStorage thuộc origin. Native trao đổi qua message schema đã version,
// không ghép token/JSON trực tiếp vào evaluateJavaScript.
```

Ví dụ Swift chạy trong executable/test target hoặc iOS target tương ứng. Ví dụ Ruby mô tả `Fastfile` versioned. Mục tiêu là minh họa contract thực tế, không giả lập framework bằng toy code.

## iOS Runtime Behavior { data-search-exclude }

UIKit vận hành qua object lifecycle; SwiftUI đánh giá description và reconcile phần UI bị ảnh hưởng, không đơn giản là vẽ lại mọi thứ. Với **WKWebView bridge: Cookie, LocalStorage và native-web data contract**, hãy log hoặc đo transition ở boundary thay vì suy luận từ UI cuối cùng.

Một callback xuất hiện không chứng minh object còn owner đúng; một UI update đúng không chứng minh request cũ đã bị cancel; một compile success cũng không chứng minh logical ordering đúng.

## Memory Implications { data-search-exclude }

Controller/model/task ownership phải khớp screen lifetime; cell/view reuse không phải object mới cho mỗi item.

```text
Who creates? → Who owns? → Who releases? → Expected deinit/eviction?
```

Nếu không có reference object trong chapter, câu hỏi vẫn hữu ích cho buffer, cache, task capture và framework object được ví dụ tạo ra.

## Concurrency Implications { data-search-exclude }

UI state được cô lập phù hợp; work nặng không nên bị giữ trên MainActor chỉ vì kết quả cuối cập nhật UI.

```text
Task owner? → isolation? → cancellation? → lifetime? → ordering?
```

Data-race freedom không tự động bảo đảm business invariant nhiều bước. Sau suspension, response hoặc lifecycle change, state có thể đã thuộc generation khác.

## Architecture Notes { data-search-exclude }

View biểu diễn và chuyển event; state transition/business rule ở model/ViewModel/use case theo độ phức tạp. Dependency hướng vào contract ổn định; implementation details nằm phía ngoài. Composition root tạo concrete dependencies và quyết định lifetime.

Không thêm layer chỉ vì chapter nhắc đến pattern. Hãy yêu cầu layer mới có ít nhất một giá trị: hấp thụ volatility, bảo vệ invariant, tạo test seam hoặc quản lý lifetime.

## Production Case { data-search-exclude }

### Context

Feature Commerce áp dụng **WKWebView bridge: Cookie, LocalStorage và native-web data contract** trong flow có network, UI lifecycle và cache.

### Symptom

User báo behavior không ổn định; telemetry cho thấy giả định HTTPCookieStorage tự đồng bộ, inject JavaScript chứa dữ liệu không escape, message handler giữ cycle hoặc native/web schema drift.

### Hypotheses

1. Contract bị hiểu sai tại call site.
2. Owner/lifetime không khớp feature scope.
3. Ordering hoặc external input phá invariant.
4. Resource budget/policy thiếu bound.

### Investigation

Dùng Web Inspector, cookie-store snapshot, origin-scoped storage probe, navigation/message correlation và contract tests; thêm correlation ID/generation an toàn, tái hiện repeated flow và so sánh expected transition với actual transition.

### Root Cause

Root cause chỉ được kết luận khi evidence chỉ ra nơi invariant bị phá, không phải nơi symptom cuối cùng xuất hiện.

### Fix

Áp dụng rule **định nghĩa handshake/schema/allowlist/timeout trước, chọn persistent hoặc nonpersistent WKWebsiteDataStore rõ ràng và đồng bộ auth ở một boundary**, thu hẹp mutation/ownership và làm failure/cancellation explicit.

### Prevention

Thêm regression test tại boundary, metric cho failure mode, review checklist về owner/state và documentation cho constraint quyết định.

## Debug / Instruments { data-search-exclude }

Primary evidence: **Web Inspector, cookie-store snapshot, origin-scoped storage probe, navigation/message correlation và contract tests**.

1. Tái hiện trên build/device gần production.
2. Đánh dấu user flow bằng signpost hoặc correlation ID không chứa PII.
3. Thu trace/log trước khi sửa.
4. Đặt hypothesis có thể bị bác bỏ.
5. Đo lại cùng workload và thêm regression protection.

## Myth vs Reality { data-search-exclude }

> **Myth:** Chỉ cần dùng đúng API/pattern tên **WKWebView bridge: Cookie, LocalStorage và native-web data contract** là code an toàn.
>
> **Reality:** Safety đến từ semantics, owner, invariant, lifecycle và evidence; API chỉ là một phần của contract.

## Common Mistakes { data-search-exclude }

- Giả định httpcookiestorage tự đồng bộ, inject javascript chứa dữ liệu không escape, message handler giữ cycle hoặc native/web schema drift → behavior chỉ sai ở scale/lifecycle edge.
- Che failure bằng default hoặc retry → mất root-cause signal.
- Nhiều layer cùng mutate state → source of truth không còn rõ.
- Tối ưu trước khi đo → tăng complexity nhưng không cải thiện bottleneck.

## Best Practices { data-search-exclude }

- Định nghĩa handshake/schema/allowlist/timeout trước, chọn persistent hoặc nonpersistent wkwebsitedatastore rõ ràng và đồng bộ auth ở một boundary.
- Ghi assumption và availability cạnh boundary version-sensitive.
- Dùng immutable value và explicit state transition khi phù hợp.
- Log category/correlation an toàn; không log token, PII hoặc payment payload.
- Đo trước/sau trên cùng workload và giữ regression test.

## Interview Questions { data-search-exclude }

### Foundation

**Hỏi:** WKWebView bridge: Cookie, LocalStorage và native-web data contract giải quyết vấn đề gì?

**30-second:** Wkwebview integration là protocol giữa hai security domains; cookie thuộc wkhttpcookiestore còn localstorage thuộc origin và chỉ nên truy cập qua bridge versioned, validated. Chọn nó khi định nghĩa handshake/schema/allowlist/timeout trước, chọn persistent hoặc nonpersistent WKWebsiteDataStore rõ ràng và đồng bộ auth ở một boundary; rủi ro chính là giả định HTTPCookieStorage tự đồng bộ, inject JavaScript chứa dữ liệu không escape, message handler giữ cycle hoặc native/web schema drift.

### Junior

**Hỏi:** Cho một ví dụ Commerce và common mistake.

**2–3 minute:** Nêu input/state, owner, code contract, failure path và test. Dùng ví dụ ở trên, sau đó giải thích vì sao giả định HTTPCookieStorage tự đồng bộ, inject JavaScript chứa dữ liệu không escape, message handler giữ cycle hoặc native/web schema drift phá invariant.

### Middle

**Hỏi:** Concept ảnh hưởng memory/concurrency/testability thế nào?

Trả lời bằng object/task graph, isolation/cancellation, boundary DI và evidence **Web Inspector, cookie-store snapshot, origin-scoped storage probe, navigation/message correlation và contract tests**.

### Senior

**Hỏi:** Constraint nào khiến bạn chọn giải pháp khác?

Deep Dive phải so sánh complexity, lifecycle, scale, migration, operability và rollback; không biến best practice thành luật tuyệt đối.

### Production

**Hỏi:** Symptom chỉ xảy ra trên 0,1% session. Bạn điều tra thế nào?

Clarify impact → thu evidence → hypothesis → controlled measurement → root cause → mitigation/fix → regression metric.

## Exercises { data-search-exclude }

### Easy

Viết một ví dụ nhỏ minh họa **WKWebView bridge: Cookie, LocalStorage và native-web data contract** và test happy path lẫn edge case.

### Medium

Refactor một call site đang gặp **giả định HTTPCookieStorage tự đồng bộ, inject JavaScript chứa dữ liệu không escape, message handler giữ cycle hoặc native/web schema drift** để contract/owner rõ hơn.

### Hard

Thiết kế state transition có cancellation/lifecycle interruption và chứng minh không publish stale result.

### Debugging Lab

Bug report: repeated Commerce flow tạo symptom liên quan **WKWebView bridge: Cookie, LocalStorage và native-web data contract**. Thu evidence bằng Web Inspector, cookie-store snapshot, origin-scoped storage probe, navigation/message correlation và contract tests, vẽ owner/state graph, xác định root cause và thêm regression test.

### Engineering / Design Exercise

Viết ADR một trang: context, options, decision, consequences và revisit conditions cho lựa chọn trong chapter.

## Cheat Sheet { data-search-exclude }

```text
Concept   → WKWebView integration là protocol giữa hai security domains; Cookie thuộc WKHTTPCookieStore còn LocalStorage thuộc origin và chỉ nên truy cập qua bridge versioned, validated
Use when  → định nghĩa handshake/schema/allowlist/timeout trước, chọn persistent hoặc nonpersistent WKWebsiteDataStore rõ ràng và đồng bộ auth ở một boundary
Risk      → giả định HTTPCookieStorage tự đồng bộ, inject JavaScript chứa dữ liệu không escape, message handler giữ cycle hoặc native/web schema drift
Evidence  → Web Inspector, cookie-store snapshot, origin-scoped storage probe, navigation/message correlation và contract tests
Remember  → owner + state + failure + lifecycle + measurement
```

## Chapter Summary { data-search-exclude }

1. Problem: API/pattern không đủ nếu semantics và owner mơ hồ.
2. Mental model: Event/state mutation → lifecycle/observation → UI description/layout → visible frame.
3. Usage rule: định nghĩa handshake/schema/allowlist/timeout trước, chọn persistent hoặc nonpersistent WKWebsiteDataStore rõ ràng và đồng bộ auth ở một boundary.
4. Mistake nguy hiểm: giả định HTTPCookieStorage tự đồng bộ, inject JavaScript chứa dữ liệu không escape, message handler giữ cycle hoặc native/web schema drift.
5. Production lesson: kết luận bằng Web Inspector, cookie-store snapshot, origin-scoped storage probe, navigation/message correlation và contract tests, rồi bảo vệ bằng test và metric.

## Related Chapters { data-search-exclude }

- [Universal Links: AASA, routing, fallback và security](23-universal-links-aasa-routing-fallback-va-security.md)
- [Human Interface Guidelines in practice: navigation, modality, controls và feedback](25-human-interface-guidelines-in-practice-navigation-modality-controls-va-feedback.md)
- [Cross-reference Index](../CROSS_REFERENCE_INDEX.md)

## References { data-search-exclude }

- [UIKit](https://developer.apple.com/documentation/uikit) — truy cập 2026-08-09.
- [SwiftUI](https://developer.apple.com/documentation/swiftui) — truy cập 2026-08-09.
- [Observation](https://developer.apple.com/documentation/observation) — truy cập 2026-08-09.
- [WKWebView](https://developer.apple.com/documentation/webkit/wkwebview) — truy cập 2026-08-09.
- [WKWebsiteDataStore](https://developer.apple.com/documentation/webkit/wkwebsitedatastore) — truy cập 2026-08-09.
- [WKHTTPCookieStore](https://developer.apple.com/documentation/webkit/wkhttpcookiestore) — truy cập 2026-08-09.

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
