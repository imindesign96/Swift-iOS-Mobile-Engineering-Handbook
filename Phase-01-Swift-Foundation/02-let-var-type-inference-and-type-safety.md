---
title: "Khi nào một giá trị được phép thay đổi? — let, var, type inference và type safety"
phase: "Swift Foundation"
difficulty: 2
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
used_later:
  - Optional
  - Struct and Class
  - Value and Reference Semantics
  - State Management
  - Sendable
  - Architecture
competencies:
  - Swift
  - Type System
  - Domain Modeling
  - Concurrency
  - Production
  - Interview
tags:
  - let
  - var
  - type-safety
  - type-inference
  - literals
  - immutability
  - domain-modeling
---

# Khi nào một giá trị được phép thay đổi?

## Story / Problem

Checkout nhận JSON:

```json
{
  "product_id": "keyboard-01",
  "amount": 2490000,
  "currency": "VND"
}
```

Một developer viết:

```swift
var amount = 2_490_000
var currency = "VND"
```

Code compile. Sau vài lần refactor, `amount` được chia cho `100` ở một layer vì người viết tưởng server gửi minor unit; `currency` bị gán thành chuỗi rỗng khi fallback. UI vẫn hiển thị một con số. Compiler không biết hai `Int` ở hai layer mang **đơn vị khác nhau**, và `var` cho phép state bị thay đổi ở nơi không nên có quyền.

Vấn đề không chỉ là chọn keyword ngắn hơn:

```text
What may change?
  ↓
Which type proves the invariant?
  ↓
Where is conversion allowed?
  ↓
Can invalid state still compile?
```

Câu hỏi trung tâm:

> `let`, `var` và type inference giúp compiler bảo vệ điều gì — và điều gì chúng không thể tự hiểu nếu domain model quá yếu?

## Objectives

Sau chapter này, bạn có thể:

- phân biệt immutable binding với immutable object graph;
- giải thích `let` và `var` bằng reassignment/mutation thay vì khẩu hiệu “constant vs variable”;
- giải thích type inference vẫn tạo static type, không biến Swift thành dynamically typed language;
- dự đoán default type của integer/floating-point literal trong context thông thường;
- dùng type annotation khi nó thêm constraint hoặc intent;
- giải thích vì sao Swift không ngầm chuyển `Int` thành `Double`;
- mô hình hóa `Money`/`ProductID` để compiler bắt semantic mismatch tốt hơn;
- nhận diện shared mutable state do `var` nhưng không kết luận mọi `var` đều nguy hiểm;
- điều tra production bug do unit/currency/type boundary.

## Prerequisites

- [Một chương trình Swift chạy như thế nào?](01-how-a-swift-program-runs.md) — type checking nằm ở đâu trong build pipeline.

## Used Later

- **Optional**: type biểu diễn “có hoặc không có value”.
- **Struct/Class**: `let` tác động khác tới value và reference semantics.
- **SwiftUI State**: mutation là input khiến UI state tiến hóa.
- **Concurrency/Sendable**: immutable value thường dễ chuyển qua isolation boundary hơn shared mutable reference.
- **Architecture**: domain type bảo vệ boundary tốt hơn primitive/stringly-typed data.
- **Testing**: invariant mạnh làm giảm số invalid state cần test.

## Mental Model

### Binding, value và type là ba lớp khác nhau

```text
name/binding ── has a static type ──→ allowed operations
     │
     ├── let: binding không được gán lại sau initialization
     └── var: binding có thể nhận value mới cùng type
```

Với value type:

```text
let product: Product
  ↓
không gán product mới
và không mutate stored state qua binding đó
```

Với reference type:

```text
let session: Session ──→ same object identity
                              ↓
                   var property của object vẫn có thể đổi
```

> **Mental-model limit**
>
> `let` là source-level rule về binding và mutability qua binding. Nó không tự biến toàn bộ object graph thành deep immutable, không bảo đảm thread safety, và không nói value nằm trên stack hay heap.

## 1. `let` và `var` thực sự cam kết điều gì?

### What?

`let` khai báo một constant binding: sau khi được khởi tạo, binding không thể được gán value khác. `var` khai báo mutable binding: code có thể gán value khác, nhưng value mới vẫn phải phù hợp với static type của binding.

```swift
let productID = "keyboard-01"
var quantity = 1

quantity = 2       // hợp lệ: Int → Int
// quantity = "2"  // compile error: String không phải Int
// productID = "cable-02" // compile error: let không được gán lại
```

### Why?

Keyword làm intent trở thành constraint compiler kiểm tra:

- `let` nói “identity/value của binding này không tiến hóa sau initialization”.
- `var` nói “state này có lifecycle và có thể transition”.

Nếu mọi thứ là mutable, reviewer phải đọc toàn scope để đoán value có đổi không. `let` thu nhỏ state space: sau assignment, một nhóm thay đổi trở thành bất khả thi tại compile time.

### How? — Definite initialization

Một local `let` không nhất thiết phải nhận value ngay tại dòng khai báo. Nó có thể được gán đúng một lần trên mọi control-flow path trước khi đọc:

```swift
let shippingFee: Int

if quantity >= 2 {
    shippingFee = 0
} else {
    shippingFee = 30_000
}

print(shippingFee)
```

Compiler chứng minh `shippingFee` được khởi tạo trước khi dùng và không bị gán lần hai. Đây là **definite initialization**, không phải runtime flag bí mật.

### When?

Ưu tiên `let` khi binding không cần reassignment. Dùng `var` khi change là một phần hợp lệ của algorithm/state:

```swift
var total = 0
for line in cartLines {
    total += line.subtotal
}
```

`var` ở đây local, scope nhỏ và mutation có mục đích rõ. Viết một chuỗi `let`/`reduce` chỉ để tránh từ khóa `var` không mặc định tốt hơn nếu làm code khó đọc.

### What if?

Mutation rộng và không có owner rõ gây:

- khó biết state nào là current;
- invalid intermediate state;
- khó reproduce ordering bug;
- data race nếu state bị share qua concurrency domain;
- test phải cover quá nhiều transition không chủ đích.

Nhưng thay mọi `var` bằng `let` mà không mô hình hóa state transition chỉ đẩy mutation sang object/reference khác hoặc tạo abstraction khó hiểu.

### Review questions — Binding

1. `let` cấm reassignment hay cấm mọi thay đổi reachable từ value?
2. Local `let` có bắt buộc gán value ngay cùng dòng không?
3. Khi nào local `var` là lựa chọn rõ ràng?
4. Vì sao “dùng `let` để thread-safe” là phát biểu thiếu điều kiện?

## 2. `let` với struct và class

### Value type binding

```swift
struct Cart {
    var itemCount: Int
}

let cart = Cart(itemCount: 1)
// cart.itemCount += 1 // compile error
```

`Cart` là value type. Binding `cart` là `let`, nên mutation property sẽ là mutation value qua immutable binding.

### Reference type binding

```swift
final class CheckoutSession {
    var retryCount = 0
}

let session = CheckoutSession()
session.retryCount += 1 // hợp lệ
// session = CheckoutSession() // compile error
```

`let session` không thể trỏ sang instance khác, nhưng instance hiện tại vẫn có mutable property. Nói ngắn gọn:

```text
let + class
→ reference binding ổn định
→ referenced object không tự động immutable
```

Điều này giải thích vì sao một `let` dependency có thể vẫn chứa shared mutable state:

```swift
final class ProductRepositoryClass {
    var cachedProductCount = 0
}

final class CatalogViewModel {
    let repository: ProductRepositoryClass

    init(repository: ProductRepositoryClass) {
        self.repository = repository
    }
}
```

ViewModel không thay repository instance, nhưng repository class có thể có cache/state thay đổi bên trong. Ownership, isolation và API contract vẫn phải được phân tích.

> **Interview trap**
>
> “Property được khai báo `let`, vậy object thread-safe đúng không?”
>
> Không đủ thông tin. Cần biết đó là value hay reference, internal state có mutable không, có bị share không và synchronization/isolation contract là gì.

## 3. Type safety

### What?

Mọi value và nơi lưu value trong Swift có type. Compiler kiểm tra value được cung cấp có phù hợp nơi sử dụng không. Swift không ngầm đổi một value tùy tiện từ type này sang type khác.

```swift
let quantity: Int = 2
let unitPrice: Double = 49.5

// let total = quantity * unitPrice // compile error
let total = Double(quantity) * unitPrice
```

Conversion explicit buộc developer nói rõ ý định. Nhưng explicit không có nghĩa tự động đúng domain: `Double(quantity)` hợp lệ về type, còn dùng `Double` cho tiền có phù hợp precision/rounding hay không là quyết định khác.

### Strong typing không phải magic domain knowledge

Đoạn này type-check:

```swift
let amountInDong: Int = 2_490_000
let amountInCents: Int = 2_490_000

func charge(amountInCents: Int) {
    // Send payment request
}

charge(amountInCents: amountInDong)
```

Argument label giúp reader nhưng cả hai vẫn là `Int`; compiler không biết đơn vị. Type safety chỉ bảo vệ distinction đã được đưa vào type system.

Mô hình mạnh hơn:

```swift
enum Currency: String {
    case vnd = "VND"
    case usd = "USD"
}

struct Money {
    let minorUnits: Int
    let currency: Currency
}

func charge(_ amount: Money) {
    print("Charging \(amount.minorUnits) \(amount.currency.rawValue)")
}
```

`Money` gom amount với currency và tạo một nơi để kiểm tra invariant/rounding/format/conversion policy. Một `typealias Dong = Int` chỉ tạo tên khác cho cùng type, không ngăn truyền `Int` sai semantic như wrapper `struct`.

### What type safety can and cannot do

| Compiler có thể bắt khi model đủ mạnh | Compiler không tự biết |
|---|---|
| String truyền vào Int parameter | `Int` này là VND hay cents |
| Gán lại `let` | business có cho đổi giá hay không nếu model dùng `var` |
| Thiếu case trong exhaustive switch | API payload có gian lận hay không |
| Một số concurrency isolation violation | checkout transition có đúng business ordering không |

## 4. Type inference

### What?

Type inference để compiler suy ra static type từ initializer và surrounding context. Bạn viết ít annotation hơn, nhưng binding vẫn có type cố định.

```swift
let itemCount = 2           // Int
let taxRate = 0.08          // Double
let productName = "Cable"  // String
let isAvailable = true      // Bool
```

Sau inference:

```swift
var itemCount = 2
itemCount = 3
// itemCount = 3.0 // compile error; itemCount đã là Int
```

> **Myth:** Không viết annotation nghĩa là variable không có type cho tới runtime.
>
> **Reality:** Compiler suy ra type tại build time; Swift vẫn statically typed.

### Literal và context

Integer literal không tự mang một concrete type cố định từ lúc parse; context giúp inference. Không có context khác, default thường là `Int`. Floating-point literal mặc định thường là `Double`.

```swift
let defaultCount = 42       // Int
let smallCount: Int8 = 42   // context chọn Int8
let defaultRate = 0.2       // Double
let compactRate: Float = 0.2
```

Context cũng đến từ function parameter hoặc expression:

```swift
func update(quantity: Int16) {}

update(quantity: 12) // literal được context hóa thành Int16 nếu representable
```

### Khi inference thiếu context

Empty collection cần annotation hoặc surrounding context:

```swift
struct Product {
    let id: String
}

let products: [Product] = []
```

Annotation có giá trị khi:

- initializer không đủ context;
- muốn chọn type khác default literal type;
- type là một phần quan trọng của domain/API boundary;
- làm compile diagnostic và reader intent rõ hơn;
- tránh expression phức tạp làm type checker hoặc người đọc khó theo.

Annotation thừa khi nó chỉ lặp lại điều hiển nhiên mà không thêm constraint:

```swift
let title = "Products"          // thường đủ rõ
let timeoutSeconds: Double = 5  // annotation có thể nói rõ contract numeric
```

### Inference không vượt qua ambiguity bằng đoán mò

Overload/generic context có thể khiến expression ambiguous. Cách sửa tốt là thêm type ở boundary nhỏ nhất hữu ích, chia expression hoặc chọn API rõ hơn; đừng annotate mọi intermediate chỉ để “compiler im lặng”.

### Review questions — Type system

1. Type inference khác dynamic typing thế nào?
2. `42` luôn là `Int` không?
3. Vì sao `Int + Double` cần conversion explicit?
4. `typealias ProductID = String` có ngăn truyền email vào ProductID parameter không?
5. Khi nào type annotation làm code tốt hơn?

## 5. Runnable Swift Example — Stronger Commerce model

```swift
enum Currency: String {
    case vnd = "VND"
    case usd = "USD"
}

struct Money {
    let minorUnits: Int
    let currency: Currency

    func adding(_ other: Money) -> Money? {
        guard currency == other.currency else {
            return nil
        }

        return Money(
            minorUnits: minorUnits + other.minorUnits,
            currency: currency
        )
    }
}

struct Product {
    let id: String
    let name: String
    let price: Money
}

@main
struct CommerceTypesDemo {
    static func main() {
        let keyboard = Product(
            id: "keyboard-01",
            name: "Magic Keyboard",
            price: Money(minorUnits: 2_490_000, currency: .vnd)
        )

        var quantity = 1
        quantity += 1

        let firstUnit = keyboard.price
        let secondUnit = keyboard.price

        guard let total = firstUnit.adding(secondUnit) else {
            print("Currency mismatch")
            return
        }

        print("Product: \(keyboard.name)")
        print("Quantity: \(quantity)")
        print("Total: \(total.minorUnits) \(total.currency.rawValue)")
    }
}
```

Chạy:

```bash
swiftc -parse-as-library -swift-version 6 CommerceTypesDemo.swift -o CommerceTypesDemo
./CommerceTypesDemo
```

Expected output:

```text
Product: Magic Keyboard
Quantity: 2
Total: 4980000 VND
```

Điểm cần quan sát:

- `keyboard`, `firstUnit`, `secondUnit`, `total` là `let` vì binding không đổi.
- `quantity` là `var` vì algorithm có state transition chủ đích.
- `.vnd` được inference từ expected `Currency` context.
- `adding` không cộng hai currency khác nhau; invalid operation được biểu diễn bằng Optional. Chapter sau sẽ giải thích Optional sâu hơn.
- `Money` mạnh hơn hai primitive rời, nhưng vẫn chưa giải quyết overflow, exchange rate, locale formatting hoặc server validation. Model tốt làm invalid state khó hơn, không làm mọi bug biến mất.

## 6. Runtime and memory implications

### Type checking chủ yếu diễn ra lúc build, nhưng runtime check vẫn tồn tại

Swift thực hiện nhiều safety check lúc build; một số điều cần check runtime, ví dụ bounds, casts hoặc integer overflow theo operation/build behavior. “Statically typed” không có nghĩa mọi lỗi đều được chứng minh trước launch.

### `let` không quyết định stack/heap

Storage phụ thuộc value/reference semantics, escape và compiler optimization; keyword `let` không phải allocation directive.

### `let` với class vẫn giữ strong reference mặc định

```swift
let session = CheckoutSession()
```

Binding ổn định nhưng vẫn sở hữu class instance theo ARC rules thông thường. Nếu session giữ closure và closure giữ ngược owner, `let` không phá retain cycle.

### Value wrapper có cost không?

Một wrapper `struct Money` thường cho type safety tốt với representation tối giản, nhưng không nên tuyên bố “zero cost” trong mọi generic/ABI/optimization context. Đo khi performance-critical; ưu tiên correctness ở domain boundary trước micro-optimization.

## 7. Concurrency implications

Shared mutable state là nguồn race, nhưng rule chính xác là ownership/isolation chứ không phải đếm `var`.

```swift
var localTotal = 0 // local trong một task/scope: thường dễ reason
```

khác với:

```swift
final class CartStore {
    var itemCount = 0 // nếu nhiều task cùng mutate: cần isolation design
}
```

`let store = CartStore()` chỉ làm reference binding ổn định; `itemCount` vẫn mutable và có thể bị share.

Checklist:

```text
Who owns mutable state?
Can multiple tasks reach it?
Which actor/lock/serialization protects it?
Can value snapshots replace shared reference?
Can mutation be scoped to one operation?
```

Immutable value không tự động `Sendable` trong mọi trường hợp: stored members và conformance rules vẫn quyết định. Nhưng value semantics + immutable stored state thường làm reasoning qua concurrency boundary dễ hơn.

## 8. Architecture notes

### Parse primitives at boundary, use domain types inside

```text
Network DTO (String/Int)
  ↓ validate + map
Domain Money / ProductID / Quantity
  ↓
UseCase / Repository / ViewModel
```

DTO phản ánh transport schema; domain model phản ánh business invariant. Không nhất thiết dùng một type cho cả JSON, database và UI.

### Mutation belongs to an owner

Đừng phát tán `var` model qua nhiều layer. Chọn owner/state machine:

```text
CartStore owns cart state
  ↓ exposes values/events
UI requests transition
  ↓ store validates and mutates
new snapshot
```

### Typealias vs wrapper

```swift
typealias ProductID = String
```

tăng readability nhưng không tạo type distinction. Dùng wrapper `struct ProductID` khi nhầm lẫn có consequence cao hoặc cần validation/behavior. Không wrapper mọi primitive nếu làm mapping/serialization quá nặng mà không tăng safety đáng kể.

## 9. Production Case — Giá bị thu nhỏ 100 lần

### Context

Backend cũ trả `amount` theo major unit cho VND. Payment SDK mới nhận `minorUnits`. Cả hai API dùng `Int`.

### Symptom

Một cohort checkout hiển thị đúng giá ở Catalog nhưng payment request gửi số tiền bằng 1/100 expected value. Không crash, không type error.

### Hypotheses

1. Backend trả sai amount.
2. Currency conversion chạy hai lần.
3. Formatter chỉ hiển thị sai, charge value đúng.
4. DTO mapper nhầm major/minor unit.
5. Experiment flag chọn sai payment adapter.

### Investigation

- Dùng correlation ID nối Catalog response → domain mapping → payment request, log category/value đã redact an toàn.
- So sánh raw response với request amount trên một test account.
- Kiểm tra code path theo feature flag.
- Unit test mapper với VND/USD boundary.
- Không log token, card data hoặc full payment payload.

Timeline chỉ ra Catalog giữ `Int` tên `amount`, adapter chia `100` vì assumption từ USD cents. Type checker không thể bắt vì input/output đều `Int`.

### Root Cause

Transport và payment domain chia sẻ primitive `Int` không mang unit; conversion policy nằm rải rác. `var amount` bị transform ở nhiều function, không có một owner/boundary duy nhất.

### Fix

- Tạo `Money(minorUnits:currency:)` làm representation canonical trong domain/payment boundary.
- Mapper theo contract của từng backend version; conversion nằm một nơi có tên rõ.
- Không mutate amount in-place qua nhiều layer; tạo new validated value.
- Payment adapter chỉ nhận `Money`, reject unsupported currency/range.
- Server vẫn phải validate amount/order; client type safety không phải security boundary.

### Prevention

- contract tests cho currency/unit;
- golden cases qua Catalog → Checkout → Payment request;
- structured telemetry ghi safe currency + normalized amount category, không sensitive payload;
- API schema field name có unit (`minor_units`) khi kiểm soát được backend;
- code review checklist: naked numeric type ở money/time/size boundary.

> **Production lesson**
>
> Strong typing chỉ bảo vệ distinction đã được encode. Hai semantic khác nhau cùng là `Int` vẫn có thể đi nhầm đường và compile hoàn hảo.

## 10. Debugging approach

| Symptom | Evidence | Câu hỏi type/mutation |
|---|---|---|
| Value đổi “bí ẩn” | watchpoint/log state transition | Binding nào là `var`? Ai có quyền mutate? |
| Compile type mismatch | full diagnostic + inferred types | Context nào chọn type? Conversion có thật sự đúng domain? |
| Ambiguous expression | chia expression, annotation boundary | Overload/generic context thiếu gì? |
| Release-only numeric issue | input/range/build config | overflow/unsafe assumption hay optimization correlation? |
| Unit/currency mismatch | end-to-end correlated values | Semantic unit có nằm trong type/name/schema không? |

### LLDB và inferred type

Trong debugging, xem dynamic value là hữu ích nhưng đừng dùng runtime observation để thay thế static contract. Khi inference khó đọc, IDE Quick Help/jump-to-definition hoặc compiler diagnostic ở expression nhỏ thường cho signal tốt hơn việc đoán type từ output.

### Review bằng mutation map

Với bug state:

```text
Declare binding
  ↓ list every write
  ↓ identify owner and allowed transitions
  ↓ remove/encapsulate unauthorized writes
  ↓ add invariant test
```

## 11. Common Mistakes

- **“Luôn dùng `let`, không bao giờ dùng `var`.”** Mutation có chủ đích là cần thiết; vấn đề là scope/owner/invariant.
- **“`let` class là immutable.”** Chỉ reference binding không đổi; object có thể mutate.
- **“Inference là dynamic typing.”** Type vẫn được compiler xác định và kiểm tra.
- **Annotate mọi dòng.** Làm code nhiễu mà không tăng constraint.
- **Không annotate boundary quan trọng.** Literal/default type có thể che intent về width/precision/unit.
- **Dùng `typealias` để mong có type safety mới.** Alias không tạo distinct type.
- **Dùng `Double` cho money theo thói quen.** Cần representation/rounding contract rõ; `Int` minor units hoặc `Decimal` có trade-off khác nhau.
- **Ép kiểu để hết compiler error.** Explicit conversion có thể vẫn sai domain hoặc truncate/overflow.
- **Biến mọi model thành class `let`.** Stable reference không giải quyết shared mutable state.

## 12. Best Practices

- Bắt đầu với `let`, chuyển sang `var` khi có transition hợp lệ và owner rõ.
- Giữ mutable scope nhỏ; expose mutation qua operation có tên thay vì public writable property khi invariant quan trọng.
- Tin type inference cho local obvious values; annotate API/domain boundary và nơi default type không nói đủ intent.
- Dùng wrapper type cho unit/identity có consequence cao: Money, ProductID, Quantity, ByteCount, Duration theo context.
- Validate external primitives khi map vào domain; compile-time type safety không tin được input từ network/disk.
- Chọn numeric representation theo range, precision, serialization và business rule — không theo thói quen.
- Với shared state, thiết kế isolation; `let` là một mảnh của reasoning, không phải synchronization primitive.

## 13. Interview Questions

### Foundation — `let` vs `var`

**30-second answer**

`let` tạo binding chỉ gán một lần; `var` cho phép reassignment với value cùng static type. Nên ưu tiên `let` khi không cần mutation để compiler giữ invariant, dùng `var` khi state/algorithm cần đổi có chủ đích. Với class, `let` giữ reference không đổi nhưng mutable properties của instance vẫn có thể thay đổi.

**2–3 minute answer**

Mở rộng bằng definite initialization, khác biệt value/reference type, scope mutation và concurrency. Nêu rằng `let` không deep immutable/thread-safe; owner/isolation vẫn cần thiết.

**Deep Dive**

Nối sang stored property initialization, `mutating` method, ARC ownership, Sendable/actor isolation, SwiftUI state ownership và API/domain modeling.

### Foundation — Type inference là gì?

Compiler suy ra static type từ initializer/context. Integer literal mặc định thường thành `Int`, floating literal thường `Double` khi không có context khác. Sau inference, binding vẫn không nhận value type khác.

### Junior — Tại sao Swift không tự đổi `Int` sang `Double`?

Explicit conversion làm loss/precision/intent visible và tránh silent conversion. Nhưng candidate mạnh nói thêm: `Double(quantity)` chỉ đúng về type; domain vẫn phải quyết định numeric representation.

### Middle — `let` có làm class thread-safe?

Không. `let` chỉ giữ reference binding. Nếu object có mutable state và được nhiều task truy cập, cần actor/lock/serialization hoặc value snapshot; còn phải xét lifetime và logical invariant.

### Senior — Khi nào tạo wrapper type?

Khi hai values cùng primitive nhưng semantic không được phép trộn, hoặc boundary cần validation/behavior. Cân nhắc consequence của nhầm lẫn, API clarity, serialization, ergonomics, performance và migration. Không wrapper mọi string/int nếu không thêm safety thực.

### Production — Type-safe code vẫn charge sai tiền vì sao?

Type system chỉ phân biệt type đã encode. Nếu major units và minor units đều là `Int`, conversion sai vẫn compile. Cần domain `Money`, canonical unit/currency, boundary validation, server-side verification và contract/integration tests.

## 14. Exercises

### Easy

Đổi các binding trong đoạn code sau thành `let` hoặc giữ `var`, giải thích từng lựa chọn:

```swift
var productID = "keyboard-01"
var quantity = 1
var total = 0

for price in [100, 200, 300] {
    total += price
}

print(productID, quantity, total)
```

### Medium

Thiết kế `ProductID`, `Quantity` và `Money` sao cho:

- ID rỗng bị reject;
- quantity phải lớn hơn 0;
- chỉ cộng Money cùng currency;
- external DTO vẫn decode primitive;
- mapping failure được biểu diễn rõ.

### Hard

Thiết kế numeric policy cho Commerce hỗ trợ VND, USD và JPY. Nêu:

- canonical representation;
- fraction digits;
- rounding;
- overflow/range;
- JSON contract;
- formatting boundary;
- server validation;
- migration từ field `amount: Int` cũ.

### Debugging Lab

Bug report: chỉ USD checkout bị lệch 100 lần, VND đúng. Có response/request logs đã redact, feature flag và mapper code. Lập hypothesis, trace unit qua boundary, tìm root cause, thêm test và telemetry ngăn tái diễn.

### Engineering / Design Exercise

Một `CartStore` class có 12 public `var` và được View, ViewModel, Repository cùng sửa. Lập mutation map, chọn owner, thiết kế state transition API và giải thích phần nào dùng value snapshot, phần nào cần actor/MainActor.

## 15. Cheat Sheet

```text
let
- binding gán một lần
- hỗ trợ definite initialization
- value type: không mutate value qua binding
- class: reference không đổi, object có thể vẫn mutable
- không phải deep immutability/thread safety

var
- binding có thể nhận value mới cùng static type
- dùng khi transition là hợp lệ
- giữ scope/owner nhỏ và rõ

type inference
- build-time static type inference
- integer literal default thường Int
- floating literal default thường Double
- context có thể chọn type khác
- không phải dynamic typing

type safety
- bắt mismatch đã encode trong type system
- không hiểu unit/business semantics nếu cùng primitive
- wrapper struct tạo distinction; typealias thì không
```

## 16. Chapter Summary

1. **Problem:** Mutable primitive không mang semantic cho phép state/unit đi sai đường mà vẫn compile.
2. **Mental model:** Binding có static type; `let`/`var` điều khiển reassignment, còn value/reference semantics quyết định mutation sâu hơn.
3. **Usage rule:** Bắt đầu với `let`, dùng `var` khi transition hợp lệ; encode distinction quan trọng thành domain type.
4. **Mistake nguy hiểm:** Coi `let` class là immutable/thread-safe hoặc nghĩ type inference là dynamic typing.
5. **Production lesson:** Strong typing chỉ mạnh bằng model; money/time/size/identity cần unit và boundary validation rõ.

## Related Chapters

- [01 — Một chương trình Swift chạy như thế nào?](01-how-a-swift-program-runs.md)
- Planned: 03 — Optional và nil safety
- Planned: 08 — Struct, class, equality và identity
- Planned: 09 — Value semantics vs reference semantics
- Planned: Phase 03 — Sendable và strict concurrency
- [Glossary — Value/Reference semantics, Sendable](../GLOSSARY.md)
- [Production Playbook](../PRODUCTION_PLAYBOOK.md)

## References

Primary sources, truy cập/xác minh ngày 2026-08-08:

1. The Swift Programming Language, [The Basics — Constants and Variables; Type Safety and Type Inference](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/thebasics/).
2. The Swift Programming Language, [Declarations — Constant and Variable Declarations](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/declarations/).
3. The Swift Programming Language, [Lexical Structure — Literals](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/lexicalstructure/).
4. The Swift Programming Language, [Properties — Constant Stored Properties](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/properties/).
5. The Swift Programming Language, [Initialization — Assigning Constant Properties](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/initialization/).
6. The Swift Programming Language, [Advanced Operators — Overflow Operators](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/advancedoperators/).
