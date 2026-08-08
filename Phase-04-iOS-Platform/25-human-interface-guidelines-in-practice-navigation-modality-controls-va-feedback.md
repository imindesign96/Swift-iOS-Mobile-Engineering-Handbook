---
title: "Human Interface Guidelines in practice: navigation, modality, controls và feedback"
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
  - "WKWebView bridge: Cookie, LocalStorage và native-web data contract"
used_later:
  - "Phase Review: iOS Platform"
competencies:
  - "iOS Platform"
  - "Production"
  - "Debugging"
  - "Interview"
tags:
  - "human-interface-guidelines-in-practice-navigation-modality-controls-va-feedback"
  - "global-commerce"
---

# Human Interface Guidelines in practice: navigation, modality, controls và feedback

> **Version scope**
>
> Baseline Swift 6.3 toolchain, Swift 6 language mode; API iOS-specific phải kiểm tra availability tại call site. Xác minh 2026-08-09.

## Story / Problem

Trong Global Commerce, screen Commerce hiển thị sai, cập nhật sau khi dismiss hoặc giật vì identity/lifecycle bị hiểu sai. Chapter này tập trung vào **Human Interface Guidelines in practice: navigation, modality, controls và feedback**: không dừng ở syntax/API mà nối behavior với ownership, failure mode và evidence production.

Nếu team chỉ nhớ tên concept, fix thường dịch symptom sang chỗ khác. Câu hỏi mở đầu là:

```text
Input/event → state hoặc resource nào thay đổi?
            → ai sở hữu thay đổi đó?
            → contract nào có thể bị vi phạm?
            → evidence nào chứng minh kết luận?
```

## Objectives

Sau chapter này, bạn có thể:

- giải thích chính xác rằng HIG thực hành biến user intent thành hierarchy, navigation, modality, control và feedback nhất quán với convention của Apple platform;
- nhận diện failure mode chính: navigation/action lẫn lộn, modal lạm dụng, error không recovery, permission sai thời điểm hoặc custom gesture không có alternative;
- chọn giải pháp bằng rule: chọn component/pattern theo user task và platform convention; document mọi deviation cùng evidence, accessibility và fallback;
- nối runtime, memory, concurrency và architecture implications;
- điều tra case production bằng task walkthrough, Accessibility Inspector, interaction-state matrix, usability evidence và production funnel/error telemetry;
- trả lời câu hỏi interview ở ba độ sâu thay vì đọc thuộc định nghĩa.

## Prerequisites { data-search-exclude }

- [WKWebView bridge: Cookie, LocalStorage và native-web data contract](24-wkwebview-bridge-cookie-localstorage-va-native-web-data-contract.md); không lặp lại định nghĩa nền nếu chapter trước đã giải thích.
- [Glossary](../GLOSSARY.md) cho terminology canonical.

## Used Later { data-search-exclude }

- [Phase Review: iOS Platform](99-phase-review.md) dùng contract của chapter này làm building block.
- [Production Playbook](../PRODUCTION_PLAYBOOK.md) dùng cùng flow evidence-first.
- [Interview Playbook](../INTERVIEW_PLAYBOOK.md) dùng mental model để xử lý follow-up.

## Mental Model

```text
Event/state mutation → lifecycle/observation → UI description/layout → visible frame
                 ↓
Focus: Human Interface Guidelines in practice: navigation, modality, controls và feedback
                 ↓
Evidence: task walkthrough, Accessibility Inspector, interaction-state matrix, usability evidence và production funnel/error telemetry
```

Mental model hữu ích để đặt câu hỏi đúng, nhưng không thay thế API contract hoặc measurement. Đặc biệt, không suy luận implementation private của compiler/framework thành behavior được đảm bảo.

## What?

Trọng tâm của **Human Interface Guidelines in practice: navigation, modality, controls và feedback** là: HIG thực hành biến user intent thành hierarchy, navigation, modality, control và feedback nhất quán với convention của Apple platform. Hãy mô tả bằng state transition, lifetime hoặc output quan sát được thay vì chỉ bằng keyword.

Một contract tốt nói rõ input hợp lệ, output/failure, side effect, owner và thời điểm kết thúc. Nếu concept chạm external data hoặc asynchronous work, contract cũng phải nói cancellation, ordering và recovery.

## Why?

Concept tồn tại để giúp đặt UI state và work đúng lifecycle trong UIKit lẫn SwiftUI. Không có boundary này, rule domain bị nhân bản, behavior phụ thuộc call order và incident khó điều tra vì không biết layer nào chịu trách nhiệm.

Giá trị lớn nhất không phải ít dòng code hơn; đó là giảm số state hợp lệ cần giữ trong đầu và làm violation xuất hiện sớm qua compiler, test hoặc telemetry.

## How?

1. Xác định source of truth và invariant liên quan.
2. Xác định creator/owner/mutator/observer.
3. Chọn API hoặc abstraction thể hiện đúng semantics.
4. Mô hình hóa failure/cancellation thay vì che bằng fallback.
5. Đo observable behavior bằng task walkthrough, Accessibility Inspector, interaction-state matrix, usability evidence và production funnel/error telemetry.

## Technical Deep Dive

### 1. Design principles và content hierarchy

HIG không phải một bộ kích thước để copy; nó là hệ decision tools bắt đầu từ mục đích của người dùng. Với mỗi screen, viết một primary task, một primary content hierarchy và một primary action. Content quan trọng phải nổi bật trước decoration; controls hỗ trợ content thay vì cạnh tranh với nó. Dùng system materials, semantic colors, text styles và SF Symbols để giao diện tự thích ứng appearance, contrast, Dynamic Type và platform evolution.

Consistency không có nghĩa mọi screen giống nhau. Cần nhất quán về meaning, placement, terminology và response của cùng một action. Custom branding nên xuất hiện ở color, illustration, motion và voice có chủ đích; đừng thay system navigation/control chỉ để “khác biệt” rồi mất behavior quen thuộc, focus, keyboard và accessibility.

### 2. Information architecture và navigation

Chọn navigation từ mental model của content:

- Tab bar cho một số ít top-level destinations ổn định; tab là nơi đến, không phải action.
- Navigation stack cho hierarchy drill-down có đường quay lại rõ.
- Sidebar/split view cho collection lớn hoặc master-detail trên regular width; compact width cần adaptation có continuity.
- Search là capability tìm content; giữ query/scope/result state khi user chuyển context hợp lý.
- Toolbar chứa actions liên quan view hiện tại; không trộn top-level navigation vào toolbar.

Mỗi destination cần title có nghĩa, selection state và restoration policy. Deep link phải đưa người dùng tới đúng hierarchy mà vẫn cho họ hiểu đang ở đâu. Không giấu tab bar tùy tiện giữa các section, không tạo nhiều nút Back giả, và không reset navigation state khi chuyển tab nếu người dùng kỳ vọng quay lại vị trí cũ.

### 3. Modality, sheets, alerts và confirmation

Modal làm gián đoạn parent context nên chỉ dùng cho task hẹp, critical decision hoặc focus thật sự cần thiết. Sheet phù hợp nhập/chọn dữ liệu liên quan context; full screen cho task nhiều bước hoặc immersive; popover cho lựa chọn contextual trên không gian lớn. Chỉ hiển thị một sheet chính tại một thời điểm và để user dismiss trước khi present modal tiếp theo.

Alert dành cho thông tin critical cần hành động ngay, không phải banner “thành công” hay lỗi mạng thông thường. Action sheet/confirmation dialog phù hợp các lựa chọn sau hành động có chủ đích. Destructive action phải có role, copy mô tả consequence và đường cancel rõ. Nếu action thường xuyên và undo được, ưu tiên undo/snackbar contextual thay vì confirmation ở mọi lần.

### 4. Controls, input và action hierarchy

Một view nên có primary action dễ nhận ra, secondary action ít nổi hơn và destructive action không cạnh tranh về emphasis. Button label dùng động từ cụ thể như “Thanh toán” hoặc “Lưu địa chỉ”, không dùng “OK” khi outcome chưa rõ. Hit region tối thiểu 44×44 pt trên iOS/iPadOS; custom button cần pressed, disabled, loading và focus/hover states phù hợp.

Form dùng label persistent, keyboard/content type đúng, autofill khi phù hợp và validation gần field. Placeholder không thay label. Không disable submit mà không giải thích field nào sai; error copy nói cách sửa, giữ input user đã nhập và đưa accessibility focus tới vùng lỗi có chủ đích. Toggle biểu diễn state on/off tức thời; action một lần phải là button, không phải switch.

### 5. Gesture và alternative input

Tap, swipe, drag, pinch và long press mang expectation hệ thống. Custom gesture chỉ nên bổ sung shortcut cho task lặp lại, không phải con đường duy nhất tới chức năng. Luôn có visible control hoặc discoverable alternative cho action quan trọng; hỗ trợ keyboard, pointer, Voice Control và Switch Control khi platform có thể dùng chúng.

Gesture conflict phải được test với scroll, system back gesture, text selection và accessibility. Animation/gesture response cần direct, interruptible và phản ánh state thật; haptic chỉ củng cố outcome có ý nghĩa, không dùng liên tục như decoration.

### 6. Feedback, loading, empty và error states

Mọi action cần feedback tương xứng: visual pressed state ngay, progress cho work đủ lâu, success/failure ở đúng scope. Hiển thị content hoặc skeleton sớm thay vì blank screen. Dùng determinate progress khi biết tiến độ; indeterminate khi không biết, nhưng nếu process stall phải cho user hiểu vấn đề và action tiếp theo. Work dài có thể cancel thì cung cấp Cancel; cancel mất tiến độ cần giải thích consequence.

Empty state phải phân biệt first use, zero search result, filtered-empty, offline và permission-denied vì action recovery khác nhau. Error message đặt gần nơi xảy ra, không đổ lỗi, không chỉ ghi mã lỗi và luôn có recovery hợp lệ: retry, edit input, open Settings hoặc contact support kèm correlation code an toàn.

### 7. Permission và privacy UX

Xin permission đúng lúc người dùng bắt đầu feature cần capability; trước system prompt, giải thích user value bằng UI trung thực nhưng không mô phỏng alert hệ thống hoặc ép/incentivize consent. Purpose string viết cụ thể dữ liệu dùng làm gì. Denied không được biến app thành dead end: giữ phần không cần permission hoạt động và cung cấp đường vào Settings khi user chủ động muốn bật lại.

Data minimization cũng là UX: chỉ hỏi field cần thiết, cho biết dữ liệu nào optional, không hiển thị sensitive content trên lock screen/widget mặc định và có privacy redaction. Destructive privacy actions như xoá account cần consequence, authentication phù hợp, progress và final confirmation/result rõ.

### 8. Writing, localization và tone

UI copy ngắn, trực tiếp, nhất quán với terminology domain. Title mô tả context; button mô tả action; error mô tả vấn đề và cách sửa. Không nối câu bằng string fragments vì word order thay đổi theo locale. Test pseudo-localization, text expansion, right-to-left, plural và formatting theo locale. Icon không thay text khi meaning không phổ biến; accessibility label mô tả intent chứ không đọc tên asset.

### 9. HIG review rubric trước release

Review theo user journey, không theo từng screenshot rời:

1. **Purpose:** primary task/action có rõ trong vài giây không?
2. **Navigation:** user biết đang ở đâu, quay lại và deep link thế nào?
3. **Modality:** mỗi interruption có thật sự cần và dismiss an toàn không?
4. **Input:** label, keyboard, validation, autofill và recovery có đúng không?
5. **Feedback:** pressed/loading/success/error/empty/offline states đầy đủ chưa?
6. **Adaptation:** iPhone nhỏ/lớn, iPad split, portrait/landscape, keyboard?
7. **Accessibility:** Dynamic Type, VoiceOver order, contrast, Reduce Motion, target size?
8. **Privacy:** permission timing/copy, denied state và sensitive presentation?
9. **Localization:** locale dài, RTL, plural, currency/date/time?
10. **Evidence:** usability walkthrough, Accessibility Inspector, snapshots và analytics có cùng chỉ ra outcome tốt hơn không?

HIG review tạo issue theo user impact, severity, owner và verification matrix. Một screenshot “đẹp” không thay thế task completion, error recovery hoặc accessibility walkthrough trên device.

### Documented behavior vs inference

- **Documented:** dùng contract trong Swift/Apple documentation và availability của SDK.
- **Inference:** storage placement, executor scheduling chi tiết hoặc reconciliation internals chỉ được dùng như giả thuyết đo lường, không phải guarantee.

## When?

Áp dụng khi chọn component/pattern theo user task và platform convention; document mọi deviation cùng evidence, accessibility và fallback. Bắt đầu bằng giải pháp đơn giản nhất giữ được invariant; thêm abstraction/synchronization/cache chỉ khi requirement hoặc measurement chứng minh cần.

Tránh dùng concept như cargo cult. Một type, layer hay primitive không có owner/contract/test rõ chỉ chuyển complexity chứ không loại bỏ nó.

## What if?

Failure mode quan trọng là navigation/action lẫn lộn, modal lạm dụng, error không recovery, permission sai thời điểm hoặc custom gesture không có alternative. Consequence có thể là state stale, duplicate work, leak, crash, UI hitch hoặc test flaky tùy boundary.

Khi assumption có thể thay đổi qua `await`, lifecycle callback, network retry hoặc migration, hãy revalidate state trước khi commit kết quả.

### Review questions

1. Observable behavior nào định nghĩa Human Interface Guidelines in practice: navigation, modality, controls và feedback?
2. Owner của state/resource là ai và lifetime kết thúc khi nào?
3. Navigation/action lẫn lộn, modal lạm dụng, error không recovery, permission sai thời điểm hoặc custom gesture không có alternative tạo evidence gì?
4. Rule chọn giải pháp là gì, và constraint nào khiến rule đổi?

## Implementation Example

```swift
import SwiftUI

struct CommerceRootView: View {
    @State private var tab: AppTab = .shop
    @State private var checkout: CheckoutDraft?
    @State private var destructiveDraft: CheckoutDraft?

    var body: some View {
        TabView(selection: $tab) {
            Tab("Cửa hàng", systemImage: "bag", value: .shop) {
                NavigationStack { ProductListView(checkout: $checkout) }
            }
            Tab("Đơn hàng", systemImage: "shippingbox", value: .orders) {
                NavigationStack { OrderListView() }
            }
        }
        .sheet(item: $checkout) { CheckoutForm(draft: $0) }
        .confirmationDialog(
            "Xoá bản nháp thanh toán?",
            isPresented: Binding(
                get: { destructiveDraft != nil },
                set: { if !$0 { destructiveDraft = nil } }
            )
        ) {
            Button("Xoá bản nháp", role: .destructive) { deleteDraft() }
            Button("Tiếp tục chỉnh sửa", role: .cancel) {}
        }
    }
}
```

Ví dụ Swift chạy trong executable/test target hoặc iOS target tương ứng. Ví dụ Ruby mô tả `Fastfile` versioned. Mục tiêu là minh họa contract thực tế, không giả lập framework bằng toy code.

## iOS Runtime Behavior { data-search-exclude }

UIKit vận hành qua object lifecycle; SwiftUI đánh giá description và reconcile phần UI bị ảnh hưởng, không đơn giản là vẽ lại mọi thứ. Với **Human Interface Guidelines in practice: navigation, modality, controls và feedback**, hãy log hoặc đo transition ở boundary thay vì suy luận từ UI cuối cùng.

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

Feature Commerce áp dụng **Human Interface Guidelines in practice: navigation, modality, controls và feedback** trong flow có network, UI lifecycle và cache.

### Symptom

User báo behavior không ổn định; telemetry cho thấy navigation/action lẫn lộn, modal lạm dụng, error không recovery, permission sai thời điểm hoặc custom gesture không có alternative.

### Hypotheses

1. Contract bị hiểu sai tại call site.
2. Owner/lifetime không khớp feature scope.
3. Ordering hoặc external input phá invariant.
4. Resource budget/policy thiếu bound.

### Investigation

Dùng task walkthrough, Accessibility Inspector, interaction-state matrix, usability evidence và production funnel/error telemetry; thêm correlation ID/generation an toàn, tái hiện repeated flow và so sánh expected transition với actual transition.

### Root Cause

Root cause chỉ được kết luận khi evidence chỉ ra nơi invariant bị phá, không phải nơi symptom cuối cùng xuất hiện.

### Fix

Áp dụng rule **chọn component/pattern theo user task và platform convention; document mọi deviation cùng evidence, accessibility và fallback**, thu hẹp mutation/ownership và làm failure/cancellation explicit.

### Prevention

Thêm regression test tại boundary, metric cho failure mode, review checklist về owner/state và documentation cho constraint quyết định.

## Debug / Instruments { data-search-exclude }

Primary evidence: **task walkthrough, Accessibility Inspector, interaction-state matrix, usability evidence và production funnel/error telemetry**.

1. Tái hiện trên build/device gần production.
2. Đánh dấu user flow bằng signpost hoặc correlation ID không chứa PII.
3. Thu trace/log trước khi sửa.
4. Đặt hypothesis có thể bị bác bỏ.
5. Đo lại cùng workload và thêm regression protection.

## Myth vs Reality { data-search-exclude }

> **Myth:** Chỉ cần dùng đúng API/pattern tên **Human Interface Guidelines in practice: navigation, modality, controls và feedback** là code an toàn.
>
> **Reality:** Safety đến từ semantics, owner, invariant, lifecycle và evidence; API chỉ là một phần của contract.

## Common Mistakes { data-search-exclude }

- Navigation/action lẫn lộn, modal lạm dụng, error không recovery, permission sai thời điểm hoặc custom gesture không có alternative → behavior chỉ sai ở scale/lifecycle edge.
- Che failure bằng default hoặc retry → mất root-cause signal.
- Nhiều layer cùng mutate state → source of truth không còn rõ.
- Tối ưu trước khi đo → tăng complexity nhưng không cải thiện bottleneck.

## Best Practices { data-search-exclude }

- Chọn component/pattern theo user task và platform convention; document mọi deviation cùng evidence, accessibility và fallback.
- Ghi assumption và availability cạnh boundary version-sensitive.
- Dùng immutable value và explicit state transition khi phù hợp.
- Log category/correlation an toàn; không log token, PII hoặc payment payload.
- Đo trước/sau trên cùng workload và giữ regression test.

## Interview Questions { data-search-exclude }

### Foundation

**Hỏi:** Human Interface Guidelines in practice: navigation, modality, controls và feedback giải quyết vấn đề gì?

**30-second:** Hig thực hành biến user intent thành hierarchy, navigation, modality, control và feedback nhất quán với convention của apple platform. Chọn nó khi chọn component/pattern theo user task và platform convention; document mọi deviation cùng evidence, accessibility và fallback; rủi ro chính là navigation/action lẫn lộn, modal lạm dụng, error không recovery, permission sai thời điểm hoặc custom gesture không có alternative.

### Junior

**Hỏi:** Cho một ví dụ Commerce và common mistake.

**2–3 minute:** Nêu input/state, owner, code contract, failure path và test. Dùng ví dụ ở trên, sau đó giải thích vì sao navigation/action lẫn lộn, modal lạm dụng, error không recovery, permission sai thời điểm hoặc custom gesture không có alternative phá invariant.

### Middle

**Hỏi:** Concept ảnh hưởng memory/concurrency/testability thế nào?

Trả lời bằng object/task graph, isolation/cancellation, boundary DI và evidence **task walkthrough, Accessibility Inspector, interaction-state matrix, usability evidence và production funnel/error telemetry**.

### Senior

**Hỏi:** Constraint nào khiến bạn chọn giải pháp khác?

Deep Dive phải so sánh complexity, lifecycle, scale, migration, operability và rollback; không biến best practice thành luật tuyệt đối.

### Production

**Hỏi:** Symptom chỉ xảy ra trên 0,1% session. Bạn điều tra thế nào?

Clarify impact → thu evidence → hypothesis → controlled measurement → root cause → mitigation/fix → regression metric.

## Exercises { data-search-exclude }

### Easy

Viết một ví dụ nhỏ minh họa **Human Interface Guidelines in practice: navigation, modality, controls và feedback** và test happy path lẫn edge case.

### Medium

Refactor một call site đang gặp **navigation/action lẫn lộn, modal lạm dụng, error không recovery, permission sai thời điểm hoặc custom gesture không có alternative** để contract/owner rõ hơn.

### Hard

Thiết kế state transition có cancellation/lifecycle interruption và chứng minh không publish stale result.

### Debugging Lab

Bug report: repeated Commerce flow tạo symptom liên quan **Human Interface Guidelines in practice: navigation, modality, controls và feedback**. Thu evidence bằng task walkthrough, Accessibility Inspector, interaction-state matrix, usability evidence và production funnel/error telemetry, vẽ owner/state graph, xác định root cause và thêm regression test.

### Engineering / Design Exercise

Viết ADR một trang: context, options, decision, consequences và revisit conditions cho lựa chọn trong chapter.

## Cheat Sheet { data-search-exclude }

```text
Concept   → HIG thực hành biến user intent thành hierarchy, navigation, modality, control và feedback nhất quán với convention của Apple platform
Use when  → chọn component/pattern theo user task và platform convention; document mọi deviation cùng evidence, accessibility và fallback
Risk      → navigation/action lẫn lộn, modal lạm dụng, error không recovery, permission sai thời điểm hoặc custom gesture không có alternative
Evidence  → task walkthrough, Accessibility Inspector, interaction-state matrix, usability evidence và production funnel/error telemetry
Remember  → owner + state + failure + lifecycle + measurement
```

## Chapter Summary { data-search-exclude }

1. Problem: API/pattern không đủ nếu semantics và owner mơ hồ.
2. Mental model: Event/state mutation → lifecycle/observation → UI description/layout → visible frame.
3. Usage rule: chọn component/pattern theo user task và platform convention; document mọi deviation cùng evidence, accessibility và fallback.
4. Mistake nguy hiểm: navigation/action lẫn lộn, modal lạm dụng, error không recovery, permission sai thời điểm hoặc custom gesture không có alternative.
5. Production lesson: kết luận bằng task walkthrough, Accessibility Inspector, interaction-state matrix, usability evidence và production funnel/error telemetry, rồi bảo vệ bằng test và metric.

## Related Chapters { data-search-exclude }

- [WKWebView bridge: Cookie, LocalStorage và native-web data contract](24-wkwebview-bridge-cookie-localstorage-va-native-web-data-contract.md)
- [Phase Review: iOS Platform](99-phase-review.md)
- [Cross-reference Index](../CROSS_REFERENCE_INDEX.md)

## References { data-search-exclude }

- [UIKit](https://developer.apple.com/documentation/uikit) — truy cập 2026-08-09.
- [SwiftUI](https://developer.apple.com/documentation/swiftui) — truy cập 2026-08-09.
- [Observation](https://developer.apple.com/documentation/observation) — truy cập 2026-08-09.
- [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines) — truy cập 2026-08-09.
- [HIG — Design principles](https://developer.apple.com/design/human-interface-guidelines/design-principles) — truy cập 2026-08-09.
- [HIG — Tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars) — truy cập 2026-08-09.
- [HIG — Modality](https://developer.apple.com/design/human-interface-guidelines/modality) — truy cập 2026-08-09.
- [HIG — Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts) — truy cập 2026-08-09.
- [HIG — Gestures](https://developer.apple.com/design/human-interface-guidelines/gestures) — truy cập 2026-08-09.
- [HIG — Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback) — truy cập 2026-08-09.
- [HIG — Loading](https://developer.apple.com/design/human-interface-guidelines/loading) — truy cập 2026-08-09.
- [HIG — Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy) — truy cập 2026-08-09.
- [HIG — Writing](https://developer.apple.com/design/human-interface-guidelines/writing) — truy cập 2026-08-09.

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
