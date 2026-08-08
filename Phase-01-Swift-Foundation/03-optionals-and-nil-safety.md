---
title: "Khi dữ liệu có thể vắng mặt — Optional và nil safety"
phase: "Swift Foundation"
difficulty: 3
importance: 5
interview_frequency: 5
status: complete
last_verified: 2026-08-08
swift_baseline: "Swift 6 language mode; version-independent fundamentals"
levels:
  - L1
  - L2
  - L3
  - L4
prerequisites:
  - "Một chương trình Swift chạy như thế nào?"
  - "let, var, type inference và type safety"
used_later:
  - Error Handling
  - Codable
  - UIKit Lifecycle
  - SwiftUI State
  - Networking
  - Persistence
  - Production Crash Analysis
competencies:
  - Swift
  - Type System
  - Domain Modeling
  - Debugging
  - Production
  - Interview
tags:
  - Optional
  - nil
  - if-let
  - guard-let
  - nil-coalescing
  - optional-chaining
  - force-unwrap
  - IUO
---

# Khi dữ liệu có thể vắng mặt

## Story / Problem

Global Commerce hỗ trợ deep link:

```text
commerce://product?id=keyboard-01
```

Một campaign gửi nhầm link:

```text
commerce://product
```

Parser cũ viết:

```swift
let productID = queryItems.first(where: { $0.name == "id" })!.value!
```

Hàng nghìn link đúng hoạt động bình thường. Link thiếu `id` đi tới production, app crash ngay khi user chạm notification.

Đội phát triển có thể “fix” bằng chuỗi rỗng:

```swift
let productID = queryValue ?? ""
```

App không crash, nhưng giờ request `/products/` chạy, log 404 tăng và user nhìn loading vô tận. Absence đã bị che, không được xử lý.

Câu hỏi đúng không phải chỉ là “unwrap thế nào?”:

```text
Can the value be absent?
  ↓
What does absence mean in this domain?
  ↓
Skip, fallback, propagate, fail, or model another state?
  ↓
Who must handle it?
```

## Objectives

Sau chapter này, bạn có thể:

- giải thích `T?` như `Optional<T>` có hai trạng thái;
- phân biệt `nil` với pointer null hoặc giá trị mặc định;
- chọn `if let`, `guard let`, `switch`, `??` và optional chaining theo control flow;
- giải thích `if let` vs `guard let` bằng scope và invariant;
- biết optional chaining luôn làm kết quả có khả năng vắng mặt;
- dùng `map`/`flatMap` cho transformation có chủ đích;
- nhận diện force unwrap như runtime precondition, không phải error handling;
- giải thích `String?`, `String!` và `String`;
- phân biệt absence, empty value, failure và loading state;
- điều tra crash do malformed deep link bằng symbolicated evidence;
- tránh logical race khi unwrap state trước/sau `await`.

## Prerequisites

- [01 — Một chương trình Swift chạy như thế nào?](01-how-a-swift-program-runs.md)
- [02 — `let`, `var`, type inference và type safety](02-let-var-type-inference-and-type-safety.md)

## Used Later

- **Error Handling**: Optional nói “có/không”; error nói thêm vì sao operation thất bại.
- **Codable**: field missing, `null`, default và schema evolution.
- **UIKit**: outlet/lifecycle và implicitly unwrapped optional.
- **SwiftUI**: optional route/selection/state identity.
- **Networking/Persistence**: cache miss, not found, decode failure không phải một nghĩa.
- **Production**: force unwrap, stale optional state và missing external input.

## Mental Model

`String?` không phải một `String` “có thể lỏng lẻo”. Nó là một type khác có hai case:

```swift
enum Optional<Wrapped> {
    case none
    case some(Wrapped)
}
```

```text
Optional<Product>
  ├── .some(product) → có Product
  └── .none / nil    → không có Product
```

Unwrap là xử lý hai nhánh để nhận `Wrapped` ở nhánh `.some`:

```text
Product?
  ↓ branch on presence
Product in success scope | explicit absence behavior
```

> **Mental-model limit**
>
> `Optional` có semantics enum hai trạng thái, nhưng memory representation cụ thể có thể được compiler/runtime tối ưu tùy `Wrapped`. Đừng suy ra mọi Optional luôn tốn thêm một byte/tag hoặc `nil` luôn là địa chỉ 0.

## 1. Optional giải quyết vấn đề gì?

### What?

Một non-optional `Product` cam kết luôn có value hợp lệ tại nơi sử dụng. `Product?` nói rõ value có thể vắng mặt. Swift không cho dùng Optional như Wrapped trước khi code xử lý possibility đó.

```swift
struct Product {
    let id: String
}

let selectedProduct: Product? = nil
// print(selectedProduct.id) // compile error
```

### Why?

Nếu absence không nằm trong type, code thường dùng sentinel:

```swift
let missingProductID = ""
let missingIndex = -1
let unknownPrice = 0
```

Sentinel trộn “không có value” với value domain có thể hợp lệ hoặc đi tiếp quá xa. Optional buộc caller đối diện absence tại compile time.

### `nil` trong Swift

Theo Swift Language Guide, `nil` là absence của value thuộc một Optional type, không phải pointer chỉ dùng cho object. Vì vậy value type cũng có Optional:

```swift
let discountPercent: Int? = nil
let deliveryDate: String? = nil
```

Không thể gán `nil` cho non-optional:

```swift
// let productID: String = nil // compile error
```

### When?

Dùng Optional khi **absence là một state hợp lệ và caller có thể xử lý**:

- user chưa chọn product;
- cache lookup không có entry;
- optional profile field;
- deep link có thể không chứa optional campaign code.

Không mặc định dùng Optional để thay error khi caller cần biết failure reason, retryability hoặc recovery action.

### What if Optional is overused?

Model chứa nhiều Optional không độc lập tạo số tổ hợp state khổng lồ:

```swift
var product: Product?
var errorMessage: String?
var isLoading: Bool
```

Có thể đồng thời `product != nil`, `errorMessage != nil`, `isLoading == true` dù business không cho phép. Một state enum thường tốt hơn:

```swift
enum LoadState<Value> {
    case idle
    case loading
    case loaded(Value)
    case failed(message: String)
}
```

Optional là hai-state model; đừng ép nó đại diện workflow bốn trạng thái.

### Review questions — Meaning

1. `nil` có phải một pointer trong Swift không?
2. Khi nào `Product?` phù hợp hơn `throws -> Product`?
3. Chuỗi rỗng khác `String? == nil` thế nào về domain?
4. Vì sao ba Optional/Boolean có thể tạo invalid combinations?

## 2. Cách tạo và quan sát Optional

```swift
let knownName: String? = "Keyboard"
let missingName: String? = nil
let inferredOptional = Optional.some("Cable")
```

`String?` là syntactic sugar của `Optional<String>`. `nil` cần expected Optional type từ annotation/context.

### Pattern matching đầy đủ bằng `switch`

```swift
func describe(_ productName: String?) -> String {
    switch productName {
    case .some(let name):
        return "Product: \(name)"
    case .none:
        return "Product is missing"
    }
}
```

`switch` làm hai case explicit, hữu ích khi cả presence và absence đều có logic đáng kể.

## 3. Optional binding: `if let` và `guard let`

### `if let` — work chỉ tồn tại khi có value

```swift
if let campaignCode = queryCampaignCode {
    analytics.track(campaignCode: campaignCode)
}
```

`campaignCode` non-optional chỉ trong nhánh `if`. Phù hợp khi nhánh presence là optional work, và function vẫn tiếp tục bình thường nếu thiếu.

Có thể bind cùng tên để giảm naming noise:

```swift
if let queryCampaignCode {
    print(queryCampaignCode)
}
```

### `guard let` — absence không cho flow chính tiếp tục

```swift
func openProduct(id: String?) {
    guard let id else {
        showInvalidLinkMessage()
        return
    }

    // id là String trong phần còn lại của scope.
    loadProduct(id: id)
}
```

`guard` yêu cầu `else` chuyển control ra khỏi scope bằng `return`, `throw`, `break`, `continue` hoặc function không return. Sau guard, compiler biết invariant `id` tồn tại.

### `if let` vs `guard let`

| Câu hỏi | `if let` | `guard let` |
|---|---|---|
| Scope của Wrapped | trong success branch | phần còn lại sau guard |
| Absence | có thể là normal path | phải exit current scope/path |
| Phù hợp | optional behavior | precondition cho happy path |
| Risk khi lạm dụng | nested pyramid | nhiều early exit che flow nếu guard mọi thứ |

Không có keyword “tốt hơn”. Chọn theo control-flow semantics.

> **Interview trap**
>
> “`guard let` nhanh hơn `if let` nên luôn dùng guard?”
>
> Không có rule API-level như vậy. Khác biệt chính là scope/control flow/readability. Performance nếu quan trọng phải đo compiled context cụ thể.

### Multiple bindings và condition

```swift
guard
    let rawID,
    !rawID.isEmpty,
    let quantity,
    quantity > 0
else {
    return
}
```

Đừng gom quá nhiều validation không liên quan vào một guard nếu error/recovery khác nhau; caller sẽ mất lý do thất bại.

### Review questions — Binding

1. Khi nào `if let` rõ hơn `guard let`?
2. Tại sao value từ `guard let` sống sau statement?
3. Một guard xử lý năm field có thể làm mất thông tin lỗi thế nào?
4. Optional binding copy value hay giữ reference? Cần xét semantics của Wrapped nào?

## 4. Fallback với `??`

Nil-coalescing:

```swift
let displayName = profile.nickname ?? profile.fullName
```

Nếu vế trái có value, unwrap value đó; nếu `nil`, dùng fallback tương thích Wrapped type.

Fallback tốt khi business có default hợp lệ:

```swift
let pageSize = remoteConfig.pageSize ?? 20
```

Fallback nguy hiểm khi che invalid/missing input:

```swift
let productID = deepLink.productID ?? "" // request sai được đẩy xuống network
```

Hỏi:

```text
Default này có ý nghĩa domain thật?
Hay chỉ làm compiler im lặng?
Có cần telemetry cho missing value không?
```

Vế fallback của `??` được đánh giá theo cơ chế autoclosure, nên expression fallback không cần chạy nếu value có sẵn. Đừng lợi dụng điều này để nhét side effect khó thấy vào fallback.

## 5. Optional chaining

Optional chaining truy cập member/call/subscript nếu value có mặt; nếu một link `nil`, chain trả `nil`:

```swift
let city: String? = user.profile?.shippingAddress?.city
```

Nếu `city` property gốc là `String`, truy cập qua Optional chain vẫn cho `String?` vì operation có thể không thực hiện được.

```text
User?
  ?.profile
  ?.shippingAddress
  ?.city
  ↓
String?
```

Optional chaining phù hợp cho read/operation mà absence có thể propagate. Nó có thể che mất **link nào** vắng nếu production cần chẩn đoán; lúc đó tách guard/validation và error category.

```swift
analytics?.trackCheckoutOpened()
```

Call bị bỏ qua nếu `analytics == nil`. Điều này chỉ đúng nếu analytics thật sự optional/noncritical. Nếu compliance event bắt buộc, silent skip là sai architecture.

## 6. Transform Optional bằng `map` và `flatMap`

### `map`

Transform Wrapped nếu có, giữ `nil` nếu thiếu:

```swift
let rawCode: String? = " summer10 "
let normalizedCode = rawCode.map { $0.trimmingCharacters(in: .whitespaces) }
// String?
```

(`trimmingCharacters` cần Foundation.)

### `flatMap`

Nếu transform cũng trả Optional, `flatMap` tránh nested Optional:

```swift
let rawQuantity: String? = "2"
let quantity: Int? = rawQuantity.flatMap(Int.init)
```

Conceptual:

```text
map:     T? + (T → U)  → U?
flatMap: T? + (T → U?) → U?
```

Chọn `if/guard` khi cần nhiều statements, logging hoặc distinct errors. Chọn `map/flatMap` khi transformation ngắn, pure và absence propagation rõ.

## 7. Force unwrap `!`

```swift
let productID = deepLink.productID!
```

Force unwrap nói:

> Tại điểm này, programmer khẳng định Optional chắc chắn có value. Nếu assertion sai, program phải fail ở runtime.

Nó không “bỏ Optional”; nó đưa một runtime precondition vào code.

### Khi nào có thể chấp nhận?

Ở nơi invariant được chứng minh rất gần và failure thực sự là programmer error, ví dụ test fixture hoặc literal conversion chắc chắn theo source:

```swift
let fixtureURL = URL(string: "https://example.com/products")!
```

Ngay cả ở đây, project có thể chọn guard/precondition helper để error message rõ hơn. Với input network/user/deep link, `!` gần như luôn sai vì external input không phải invariant do compiler kiểm soát.

### Force unwrap không phải error handling

```text
Expected absence/failure → model and handle
Broken internal invariant → assertion/precondition/fail fast with evidence
```

Đừng force unwrap vì “đã check ở dòng trước” nếu state có thể đổi qua alias/concurrency/suspension.

## 8. Implicitly Unwrapped Optional — `String!`

Ba type interview thường hỏi:

| Type | Meaning |
|---|---|
| `String` | luôn có String, không nhận `nil` |
| `String?` | Optional String, caller phải xử lý absence |
| `String!` | Optional String có khả năng implicit unwrap tại use site; nil khi unwrap gây runtime failure |

IUO hữu ích khi lifecycle đảm bảo value được thiết lập sau initialization nhưng trước mọi use, hoặc ở một số Objective-C interoperability/nullability boundary. UIKit outlet lịch sử là ví dụ quen thuộc:

```swift
@IBOutlet private weak var titleLabel: UILabel!
```

Sau view loading, outlet được kỳ vọng nối. Access trước lifecycle hoặc connection sai có thể crash.

Không dùng IUO như cách né initializer:

```swift
var repository: ProductRepository! // “sẽ set sau” nhưng không có proof rõ
```

Tốt hơn là constructor injection/non-optional property nếu dependency bắt buộc.

Apple khuyến nghị nullability annotations ở Objective-C API để Swift import thành optional/non-optional chính xác thay vì IUO vì “không biết”.

## 9. Nested Optional và ba trạng thái

`T??` có ba trạng thái quan sát được:

```text
.none
.some(.none)
.some(.some(value))
```

Điều này có thể xuất hiện khi dictionary chứa Optional value hoặc khi cần phân biệt “field không được cung cấp” với “field được cung cấp là null”. Nhưng nested Optional thường khó đọc; domain enum có tên case rõ hơn:

```swift
enum FieldUpdate<Value> {
    case unchanged
    case clear
    case set(Value)
}
```

Đây là ví dụ Optional không đủ vocabulary cho mọi protocol/state.

## 10. Runnable Swift Example — Deep-link parser an toàn

```swift
import Foundation

struct Product {
    let id: String
    let name: String
}

enum ProductRoute {
    case product(id: String, campaign: String?)
}

func makeProductRoute(
    productID: String?,
    campaign: String?
) -> ProductRoute? {
    guard let productID, !productID.isEmpty else {
        return nil
    }

    let normalizedCampaign = campaign.flatMap { value in
        let trimmed = value.trimmingCharacters(in: .whitespacesAndNewlines)
        return trimmed.isEmpty ? nil : trimmed
    }

    return .product(id: productID, campaign: normalizedCampaign)
}

func describe(_ route: ProductRoute?) -> String {
    guard let route else {
        return "Invalid product link"
    }

    switch route {
    case .product(let id, let campaign):
        let source = campaign ?? "organic"
        return "Open product \(id), source: \(source)"
    }
}

@main
struct OptionalDemo {
    static func main() {
        let valid = makeProductRoute(
            productID: "keyboard-01",
            campaign: " summer "
        )
        let invalid = makeProductRoute(
            productID: nil,
            campaign: "push"
        )

        print(describe(valid))
        print(describe(invalid))
    }
}
```

Build và chạy:

```bash
swiftc -parse-as-library -swift-version 6 OptionalDemo.swift -o OptionalDemo
./OptionalDemo
```

Expected output:

```text
Open product keyboard-01, source: summer
Invalid product link
```

Thiết kế này:

- dùng `guard` vì `productID` là prerequisite của route;
- dùng `flatMap` vì normalize có thể biến chuỗi whitespace thành absence;
- giữ `campaign` Optional vì absence hợp lệ và có fallback `organic` ở presentation/analytics policy;
- trả `nil` cho invalid route vì caller hiện chỉ cần valid/invalid. Nếu UI cần lý do chi tiết, đổi sang `throws` hoặc result enum.

## 11. Runtime and memory implications

### Optional là value type semantics

Optional wrap `Wrapped`; copy/mutation behavior chịu semantics của Wrapped. `Optional<ProductStruct>` chứa value semantics; `Optional<ProductClass>` có thể chứa reference và ARC ownership.

```swift
final class Session {}
var session: Session? = Session()
session = nil
```

Gán Optional strong reference thành `nil` bỏ owning edge đó; object chỉ `deinit` nếu không còn strong owner khác. `nil` không “xóa object” toàn cục.

### `weak` thường là Optional

Weak reference không giữ object sống và tự về `nil` khi object deallocate, nên type thường Optional. Việc unwrap weak reference tạo một local strong reference trong scope phù hợp có thể giữ object sống trong lúc sử dụng; ownership chi tiết sẽ ở Phase 02.

### Representation là implementation detail

Compiler có thể dùng spare bits/niche optimization cho một số Optional representation. Không viết unsafe/layout-sensitive code dựa trên phỏng đoán size mà không dùng documented ABI/API và measurement phù hợp.

## 12. Concurrency implications — value có thể đổi qua `await`

Optional binding tạo value cho scope hiện tại, nhưng invariant của shared state có thể thay đổi trong lúc task suspended.

```swift
actor SessionStore {
    private var token: String?

    func authenticatedRequest() async throws {
        guard let token else {
            throw SessionError.missingToken
        }

        try await sendRequest(token: token)
    }
}
```

Local `token` là snapshot String dùng cho request. Trong lúc `await`, actor có thể reenter và `self.token` bị logout/refresh. Không có data race, nhưng request có thể dùng token stale nếu business invariant yêu cầu token current.

Hỏi:

```text
Optional belongs to which state owner?
Is the unwrapped value a snapshot or must it remain current?
Can state change across await?
Should operation be cancelled/versioned/revalidated?
```

Force unwrap sau một check tách rời đặc biệt nguy hiểm nếu property có thể đổi:

```swift
if store.selectedProduct != nil {
    await doOtherWork()
    // store.selectedProduct! may no longer satisfy the earlier check.
}
```

Thiết kế snapshot rõ hoặc revalidate sau suspension; actor isolation không tự bảo vệ logical invariant qua `await`.

## 13. Architecture notes — Absence, empty, failure và state

Chọn return type theo semantic:

| Tình huống | Model thường hợp lý |
|---|---|
| Cache lookup không có entry | `Product?` |
| Server fetch có network/decode/business failure | `async throws -> Product` hoặc domain result |
| Search thành công nhưng không có kết quả | `[Product]` rỗng, không nhất thiết `[Product]?` |
| Screen idle/loading/content/error | state enum |
| Partial update: unchanged/clear/set | enum ba case, không chỉ `T?` |

### Repository example

```swift
protocol ProductCache {
    func product(id: String) async -> Product?
}

protocol ProductRemoteDataSource {
    func fetchProduct(id: String) async throws -> Product
}
```

Cache miss là normal absence; remote failure cần reason/recovery. Gộp cả hai thành `Product?` làm mất network error và khả năng retry.

### API design rule

Optional output chuyển responsibility xử lý absence cho caller. Trước khi thêm `?`, viết một câu:

> `nil` ở API này nghĩa là ______, và caller nên ______.

Nếu không điền rõ, type có thể chưa đủ chính xác.

## 14. Production Case — Malformed deep link crash

### Context

Push campaign tạo link từ CMS. App parser force unwrap query item `id` vì template “luôn có field”. CMS cho phép editor xóa field.

### Symptom

- Crash chỉ xảy ra khi mở một campaign cụ thể.
- App launch bình thường khi mở icon.
- Stack trace symbolicate vào `ProductDeepLinkParser.parse(_:)` tại force unwrap.

### Hypotheses

1. URL thiếu query item.
2. Percent encoding làm parser trả `nil`.
3. Notification payload bị truncate.
4. Race trong routing state.
5. Outlet/view chưa load.

### Investigation

1. Xác nhận crash report đúng dSYM/build và faulting thread.
2. Dựa trên app frame, inspect source line `value!`.
3. Dùng safe telemetry/campaign ID để lấy template, không log private notification content.
4. Reproduce với missing `id`, empty `id`, invalid percent encoding và duplicated query.
5. Kiểm tra router behavior khi parse thất bại.

Evidence cho thấy query item không tồn tại; `!` biến external absence thành fatal invariant.

### Root Cause

App coi contract do CMS/user-controlled data cung cấp là internal invariant. Parser trả non-optional route và dùng force unwrap, nên không có failure path. Test chỉ dùng golden valid link.

### Fix

- Parser validate và trả `ProductRoute?` hoặc `throws DeepLinkError` tùy UX/telemetry need.
- Router hiển thị safe fallback screen/message, không gửi request với ID rỗng.
- Campaign validation ở CMS/server từ chối template thiếu required field.
- Normalize/validate URL một lần tại boundary; feature nhận typed route.

### Prevention

- property-based/table tests cho missing/empty/duplicate/encoded query;
- crash-free deep-link metric theo route/campaign ID an toàn;
- schema validation trước publish;
- code review rule: không force unwrap external input;
- regression test từ payload gây incident.

> **Production lesson**
>
> Optional không chỉ ngăn crash. Nó buộc kiến trúc quyết định failure path. Dùng fallback vô nghĩa có thể đổi crash thành silent corruption hoặc broken flow.

## 15. Debug / Instruments

### Force-unwrap crash

```text
Crash report
→ symbolicate đúng build
→ faulting thread + first app frame
→ source line containing unwrap/IUO access
→ reconstruct Optional origin
→ classify: external absence or broken internal invariant
→ fix model/control flow
→ regression test
```

### Debug questions

- Optional được tạo ở network, persistence, UI lifecycle hay mapping?
- `nil` là expected state hay evidence của bug trước đó?
- Có fallback đang che signal không?
- Optional bị unwrap bao nhiêu layer sau origin?
- Có `await`/callback/lifecycle transition giữa check và use không?
- Nếu IUO nil, initialization/lifecycle contract nào không xảy ra?

### Logging

Log category và safe identifier, không log token/PII:

```text
route=product parse_result=missing_required_id campaign_id=<safe-id>
```

Đừng log full URL nếu query có sensitive data.

## 16. Common Mistakes

- Force unwrap external input.
- Dùng `?? ""` hoặc `?? 0` để che invalid absence.
- Optional hóa mọi field thay vì thiết kế state enum.
- Trả `nil` cho mọi lỗi và mất failure reason.
- Dùng IUO để trì hoãn dependency injection.
- Check `optional != nil` rồi force unwrap ở chỗ khác.
- Optional chaining cho operation bắt buộc, khiến side effect bị skip im lặng.
- Dùng `Bool?` mà không định nghĩa rõ `nil` khác `false` thế nào.
- Nested `if let` sâu thay vì guard/state/model rõ.
- Giả định actor ngăn optional state đổi qua `await`.

## 17. Best Practices

- Viết semantic của `nil` trước khi chọn Optional.
- Dùng `guard let` cho prerequisite của happy path; `if let` cho optional branch.
- Chỉ dùng `??` khi fallback là domain-valid và observability requirement đã rõ.
- Giữ unwrap gần origin hoặc map boundary thành domain type sớm.
- Dùng error/result khi caller cần reason/retry/recovery.
- Dùng state enum khi workflow có hơn presence/absence.
- Xem force unwrap là executable precondition; yêu cầu proof gần và controlled input.
- Hạn chế IUO ở lifecycle/interop contract thực sự, ưu tiên non-optional constructor injection.
- Qua `await`, coi unwrapped value là snapshot và revalidate business invariant khi cần.

## 18. Interview Questions

### Foundation — Optional là gì?

**30-second answer**

`T?` là `Optional<T>`, một type có hai trạng thái: có Wrapped value hoặc `nil`. Swift buộc code xử lý absence trước khi dùng như `T`, giúp không trộn missing value với non-optional value.

**2–3 minute answer**

Nêu `if let`, `guard let`, `switch`, `??`, chaining; phân biệt empty/sentinel/error. Force unwrap là runtime precondition. `nil` không chỉ dành cho object pointer.

**Deep Dive**

Nối nested Optional, IUO/ObjC nullability, memory representation không guarantee, weak references, state modeling và logical race qua await.

### Foundation — `if let` vs `guard let`

Khác biệt chính là control flow/scope. `if let` cho success branch cục bộ; `guard let` yêu cầu failure exit và giữ Wrapped trong remaining scope. Chọn theo semantics, không theo claim performance tuyệt đối.

### Junior — `String?` vs `String!` vs `String`

- `String`: luôn có value.
- `String?`: có/không, explicit handling.
- `String!`: vẫn Optional nhưng có implicit unwrap behavior; nil lúc use có thể runtime failure. Chỉ dùng khi lifecycle/interop bảo đảm sau initialization.

### Middle — Optional vs Result/throws

Optional phù hợp khi caller chỉ cần presence/absence và absence là normal. Result/throws phù hợp khi failure reason, recovery, retry hoặc observability quan trọng. Empty collection thường biểu diễn successful zero results, không phải nil.

### Senior — Optional và API design

Một câu trả lời mạnh hỏi semantic của nil, ownership của validation, state-space, transport/domain boundary, interoperability, concurrency snapshot và migration compatibility. Optional là vocabulary hai trạng thái, không phải universal error/state model.

### Production — Force unwrap crash hiếm

Symbolicate, xác định app frame/origin, cluster theo input/lifecycle, reproduce malformed/edge cases, phân biệt external absence với broken invariant, sửa boundary model, thêm regression input và safe telemetry. Không chỉ thay `!` bằng `?` nếu operation bắt buộc.

## 19. Exercises

### Easy

Viết ba phiên bản xử lý `campaignCode: String?` bằng `if let`, `guard let`, `??`. Với mỗi phiên bản, nói semantic phù hợp và trường hợp dùng sai.

### Medium

Thiết kế API cho:

1. cache lookup;
2. remote product fetch;
3. search zero results;
4. checkout loading/success/failure;
5. profile nickname optional.

Chọn `T?`, `[T]`, `throws`, Result hoặc state enum và giải thích.

### Hard

Thiết kế partial profile PATCH phân biệt:

- không thay field;
- xóa field về null;
- set value mới.

Không dùng `String??` ở public domain API; tạo enum có tên case, rồi map JSON.

### Debugging Lab

Cho crash report trỏ vào một IUO outlet trong async callback sau khi screen dismiss. Lập object/lifecycle timeline, xác định vì sao outlet trở thành nil hoặc view lifecycle không hợp lệ, sửa task cancellation/state ownership thay vì chỉ optional chain để bỏ qua update.

### Engineering / Design Exercise

Refactor ViewModel có `product: Product?`, `error: Error?`, `isLoading: Bool`, `isEmpty: Bool`. Liệt kê invalid combinations, tạo state enum, định nghĩa transitions và test table.

## 20. Cheat Sheet

```text
T? = Optional<T>
- .some(T)
- .none / nil

if let
- unwrap trong success branch
- absence có thể tiếp tục flow ngoài branch

guard let
- absence phải exit current path
- Wrapped sống trong remaining scope

??
- fallback khi nil
- chỉ dùng default có semantic thật

?.
- propagate absence qua member/call/subscript
- result vẫn Optional

!
- runtime precondition
- nil → runtime failure
- không phải error handling

T!
- Optional với implicit unwrap behavior
- dành cho proven lifecycle/interop contract
```

Decision guide:

```text
Normal absence, no reason needed → T?
Successful zero items → [T] empty
Failure reason/recovery needed → throws / Result / domain error
Multi-state workflow → enum state
Programmer invariant → precondition/assertion; force unwrap only with proof
```

## 21. Chapter Summary

1. **Problem:** External/missing data bị force unwrap gây crash; fallback rỗng có thể che bug.
2. **Mental model:** Optional là enum hai case; unwrap là xử lý presence/absence.
3. **Usage rule:** Chọn handling theo meaning của nil, không theo cú pháp ngắn nhất.
4. **Mistake nguy hiểm:** Coi external input là invariant hoặc dùng Optional thay mọi error/state.
5. **Production lesson:** Trace Optional về origin, phân biệt absence hợp lệ với broken contract, rồi sửa boundary và regression protection.

## Related Chapters

- [01 — Một chương trình Swift chạy như thế nào?](01-how-a-swift-program-runs.md)
- [02 — `let`, `var`, type inference và type safety](02-let-var-type-inference-and-type-safety.md)
- Planned: Error handling, `throws` và `Result`
- Planned: Codable fundamentals
- Planned: UIViewController lifecycle
- Planned: Actor reentrancy và logical race
- [Glossary — Optional, Source of Truth, Suspension Point](../GLOSSARY.md)
- [Production Playbook](../PRODUCTION_PLAYBOOK.md)

## References

Primary sources, truy cập/xác minh ngày 2026-08-08:

1. The Swift Programming Language, [The Basics — Optionals](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/thebasics/).
2. The Swift Programming Language, [Types — Optional and Implicitly Unwrapped Optional Types](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/types/).
3. The Swift Programming Language, [Optional Chaining](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/optionalchaining/).
4. The Swift Programming Language, [Basic Operators — Nil-Coalescing Operator](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/basicoperators/).
5. The Swift Programming Language, [Expressions — Optional-Chaining and Forced-Value Expressions](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/expressions/).
6. Apple Developer Documentation, [Designating Nullability in Objective-C APIs](https://developer.apple.com/documentation/swift/designating-nullability-in-objective-c-apis).
