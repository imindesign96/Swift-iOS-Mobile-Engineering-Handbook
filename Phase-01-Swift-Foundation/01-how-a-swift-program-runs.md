---
title: "Một chương trình Swift chạy như thế nào?"
phase: "Swift Foundation"
difficulty: 2
importance: 5
interview_frequency: 4
status: complete
last_verified: 2026-08-08
swift_baseline: "Swift 6 language mode; verified with stable Swift 6.3.3"
levels:
  - L1
  - L2
  - L3
  - L4
prerequisites: []
used_later:
  - Type System
  - Memory & Runtime
  - Concurrency
  - App Lifecycle
  - Performance
  - Production Debugging
competencies:
  - Swift
  - Runtime
  - iOS Platform
  - Debugging
  - Production
  - Interview
tags:
  - compiler
  - swiftc
  - SIL
  - LLVM
  - machine-code
  - main
  - dyld
  - app-launch
---

# Một chương trình Swift chạy như thế nào?

> **Version scope**
>
> Chapter dùng Swift 6 language mode. Tại lần xác minh ngày 2026-08-08, Swift stable hiện hành là 6.3.3. Swift 6.4 đang có tài liệu/snapshot beta nên không được xem là baseline stable ở đây. Compiler version, Swift language mode và iOS deployment target là ba cấu hình khác nhau.

## Story / Problem

Người dùng chạm vào icon **Global Commerce**. Launch screen xuất hiện, rồi Product Catalog mở ra.

Nhìn từ ngoài, chỉ có một lần chạm:

```text
Tap icon → app xuất hiện
```

Nhưng giữa hai sự kiện đó là hai hành trình rất khác nhau:

```text
BUILD-TIME (trên máy developer/CI)
Swift source
  ↓ compiler + linker + signing
iOS app bundle chứa native executable

LAUNCH-TIME (trên thiết bị)
Tap icon
  ↓ OS kiểm tra và tạo process
dyld load executable/frameworks
  ↓
entry point (@main)
  ↓
UIKit/SwiftUI dựng app và event loop
  ↓
first frame
```

Nếu trộn hai hành trình này, nhiều câu trả lời nghe có vẻ đúng nhưng dẫn tới debugging sai:

- “Swift chạy từng dòng source trên iPhone.”
- “`@main` chắc chắn là instruction đầu tiên của process.”
- “Build dùng Swift compiler 6.x nghĩa là target đã ở Swift 6 language mode.”
- “App launch chậm thì chỉ cần tối ưu code trong `AppDelegate`.”

Câu hỏi trung tâm của chapter:

> Từ một file `.swift` đến lúc UI đầu tiên xuất hiện trên iPhone, compiler, linker, operating system, dynamic loader và framework đã làm gì — và phần nào thuộc trách nhiệm của app?

## Objectives

Sau chapter này, bạn có thể:

- tách rõ build-time khỏi launch/runtime;
- mô tả pipeline Swift source → type checking → SIL → LLVM IR → machine code ở mức mental model đúng;
- giải thích vì sao production iOS app không chạy source Swift như một interpreter;
- phân biệt compiler/toolchain version, language mode và deployment target;
- giải thích vai trò của linker, app bundle, code signing, `dyld` và `@main`;
- viết và chạy một Swift executable tối giản;
- điều tra slow launch bằng Xcode Organizer/Instruments thay vì đoán;
- trả lời câu hỏi phỏng vấn “một chương trình Swift chạy thế nào?” ở nhiều độ sâu.

## Prerequisites

Không yêu cầu chapter trước. Bạn chỉ cần nhận biết một vài từ khóa Swift như `struct`, `let`, `func` và `print`; các chapter sau sẽ giải thích chính xác từng khái niệm.

## Used Later

Mental model này là bản đồ cho toàn handbook:

- **Type System**: type checking diễn ra trước khi executable được tạo.
- **Value/Reference Semantics và ARC**: source-level semantics được compiler hiện thực bằng code và runtime support.
- **Concurrency**: `await` là suspension point của task, không phải chỉ thị “đổi thread”.
- **UIKit/SwiftUI Lifecycle**: `@main` mới là cửa vào; framework lifecycle tiếp tục sau đó.
- **Modularization**: static/dynamic frameworks tác động build graph và launch cost khác nhau.
- **Production**: slow launch, missing framework và code-signing failure xảy ra trước hoặc quanh app entry point.

## Mental Model

Hãy giữ hai pipeline riêng trong đầu.

### Pipeline A — Biến source thành artifact có thể chạy

```text
.swift source
   ↓ parse + name/type checking
Swift program đã được hiểu về mặt ngôn ngữ
   ↓ lower to SIL
Swift Intermediate Language
   ↓ optimization + IR generation
LLVM IR
   ↓ target-specific code generation
Object files / native machine code
   ↓ link
Executable + linked dependencies
   ↓ bundle + resources + entitlements + code signing
.app artifact
```

### Pipeline B — Launch artifact trên iOS

```text
Launch request
   ↓
OS validates/creates process
   ↓
dyld maps executable and required libraries, resolves symbols
   ↓
pre-main work where applicable
   ↓
program entry point (@main / top-level entry)
   ↓
UIKit or SwiftUI launch machinery
   ↓
scene + first useful UI
   ↓
event-driven runtime
```

> **Mental-model limit**
>
> Pipeline A không phải public compatibility contract cho mọi chi tiết compiler. SIL và các optimization pass là kiến trúc implementation của Swift compiler và có thể tiến hóa. Điều ổn định hơn đối với application developer là source/language semantics, supported build settings, emitted executable behavior và API/platform contracts.

## 1. Swift là gì trong pipeline này?

### What?

Swift là một ngôn ngữ compiled: Swift compiler nhận source, kiểm tra chương trình và tạo machine code cho target. Với iOS app thông thường, code ứng dụng được build trước khi phân phối; thiết bị chạy executable đã build chứ không đọc lại file `.swift` của bạn để thực thi từng dòng.

Điều đó không có nghĩa Swift “không có runtime”. Một Swift program vẫn cần runtime support cho những capability như metadata, dynamic casting, protocol conformance, error handling, ARC và concurrency. **Compiled** mô tả cách source trở thành executable, không có nghĩa mọi abstraction đều biến mất hoặc mọi call đều static.

### Why?

Pipeline compiled cho Swift đồng thời phục vụ nhiều mục tiêu:

- phát hiện lỗi syntax/type trước khi ship;
- tối ưu xuyên qua representation trung gian;
- sinh machine code phù hợp architecture/OS target;
- liên kết với Swift runtime, Foundation và Apple frameworks;
- tạo artifact có thể ký, cài và được hệ điều hành kiểm soát.

Nếu Product Catalog truyền `String` vào một function yêu cầu `Int`, compiler có thể từ chối build. Nếu app tham chiếu một framework nhưng không embed đúng, source có thể type-check thành công nhưng artifact vẫn lỗi ở link hoặc launch. Mỗi stage bắt một lớp vấn đề khác nhau.

### How?

Theo tài liệu kiến trúc chính thức của Swift compiler, flow cấp cao gồm:

1. **Parsing**: source text được chuyển thành cấu trúc cú pháp.
2. **Semantic analysis / type checking**: compiler resolve name, overload, generic constraint và kiểm tra type rules.
3. **SIL generation**: chương trình được lower thành Swift Intermediate Language, representation giữ các khái niệm cần cho Swift-specific analysis và optimization.
4. **SIL optimization**: tùy build mode/flags, compiler có thể inline, specialize generic, devirtualize hoặc loại dead code khi chứng minh an toàn.
5. **LLVM IR generation**: SIL được lower thành LLVM IR.
6. **LLVM optimization và target code generation**: tạo machine code/object file cho target architecture.
7. **Linking**: linker kết hợp object files và dependencies thành executable/framework.

Rút gọn:

```text
Swift syntax
  ↓ “Chương trình có hợp lệ và có nghĩa gì?”
Typed Swift program
  ↓ “Biểu diễn/optimize Swift semantics thế nào?”
SIL
  ↓ “Sinh code cho target thế nào?”
LLVM IR → machine code
```

> **Documented architecture vs contract**
>
> Swift.org công khai kiến trúc compiler và vai trò SIL/LLVM IR. Đây là nguồn tốt để hiểu implementation. Tuy nhiên, app không nên phụ thuộc vào tên pass hoặc hình dạng SIL cụ thể như một API guarantee.

### When does this matter?

Mental model compiler quan trọng khi:

- đọc diagnostics và hiểu lỗi nằm ở parse, type check, link hay launch;
- so sánh Debug/Release;
- điều tra compile time hoặc binary size;
- thiết kế generic/protocol/public API có ảnh hưởng specialization/dynamic dispatch;
- phân biệt language guarantee với observed optimizer behavior.

### What if you ignore the stages?

Bạn dễ sửa sai lớp:

- **Compiler error** nhưng đi tìm crash log.
- **Linker error** nhưng thay business logic.
- **dyld launch failure** nhưng đặt breakpoint trong `AppDelegate` rồi thắc mắc vì sao không hit.
- **Release-only bug** nhưng kết luận “compiler sai” trước khi kiểm tra race, undefined assumption hoặc configuration difference.

### Review questions — Compiler pipeline

1. SIL khác source và machine code ở điểm nào?
2. Type error thường bị phát hiện ở stage nào?
3. Linker giải quyết vấn đề gì mà type checker không giải quyết?
4. Vì sao không nên coi hình dạng SIL hiện tại là public app contract?
5. “Compiled language” có đồng nghĩa “không cần runtime” không?

## 2. Compiler version không phải language mode

Có ít nhất ba “version” dễ bị trộn:

| Dimension | Trả lời câu hỏi | Ví dụ |
|---|---|---|
| Compiler/toolchain version | Binary compiler và standard tooling nào đang build? | Swift 6.3.3 |
| Swift language mode | Source-compatibility/rule set nào được target chọn? | Swift 6 |
| Deployment target / SDK | App được build với SDK nào và chạy từ OS version nào? | iOS deployment target của target |

Một Swift 6.x compiler có thể hỗ trợ build target ở language mode cũ. Swift 6 migration guide nhấn mạnh việc chuyển target sang Swift 6 language mode là có chủ đích; chỉ thấy “Apple Swift version 6.x” trong build log chưa chứng minh strict Swift 6 rules đã bật cho mọi target.

Điều này đặc biệt quan trọng trong codebase nhiều module:

```text
App target — Swift 6 mode
  ├── FeatureCatalog — Swift 6 mode
  ├── LegacyCheckout — Swift 5 mode
  └── Third-party binary framework — prebuilt
```

Migration có thể theo từng target. Boundary giữa target mới/cũ cần review concurrency annotations và imported API assumptions, thay vì tuyên bố “repo đã lên Swift 6” chỉ vì đổi Xcode.

> **Myth:** Dùng Swift compiler 6.x tự động biến toàn bộ project thành Swift 6 language mode.
>
> **Reality:** Compiler/toolchain và language mode là hai cấu hình khác nhau; language mode được chọn theo target/build settings và migration có thể incremental.

## 3. Runnable Swift example

Ví dụ dưới đây là executable command-line thuần Swift để cô lập pipeline ngôn ngữ khỏi UIKit/SwiftUI.

```swift
struct Product {
    let name: String
    let unitPrice: Int
}

struct CartLine {
    let product: Product
    let quantity: Int

    var subtotal: Int {
        product.unitPrice * quantity
    }
}

@main
struct CommerceCLI {
    static func main() {
        let keyboard = Product(name: "Magic Keyboard", unitPrice: 2_490_000)
        let cable = Product(name: "USB-C Cable", unitPrice: 490_000)

        let cart = [
            CartLine(product: keyboard, quantity: 1),
            CartLine(product: cable, quantity: 2)
        ]

        let total = cart.reduce(0) { partialTotal, line in
            partialTotal + line.subtotal
        }

        print("Items: \(cart.count)")
        print("Total: \(total) VND")
    }
}
```

Lưu thành `CommerceCLI.swift`, rồi build ở Swift 6 language mode:

```bash
swiftc -parse-as-library -swift-version 6 CommerceCLI.swift -o CommerceCLI
./CommerceCLI
```

Expected output:

```text
Items: 2
Total: 3470000 VND
```

`@main` nói rằng type `CommerceCLI` cung cấp top-level entry point. Theo Swift Language Reference, type gắn `@main` phải cung cấp `static main()` phù hợp; một executable chỉ có tối đa một top-level entry point.

### Quan sát representation trung gian

Swift compiler có thể emit các representation để học/điều tra:

```bash
swiftc -parse-as-library -swift-version 6 -emit-silgen CommerceCLI.swift > CommerceCLI.silgen
swiftc -parse-as-library -swift-version 6 -O -emit-sil CommerceCLI.swift > CommerceCLI.sil
swiftc -parse-as-library -swift-version 6 -O -emit-ir CommerceCLI.swift > CommerceCLI.ll
```

Đừng cố đọc hết output. Hãy tìm:

- symbol liên quan `CommerceCLI.main`;
- call tới `CartLine.subtotal` ở unoptimized output;
- khác biệt giữa output không `-O` và có `-O`;
- nơi generic `reduce` xuất hiện hoặc được optimizer biến đổi.

Kết quả có thể khác theo compiler version/target. Mục tiêu là thấy source đã được lower/transform, không ghi nhớ textual SIL.

### Tại sao dùng `let`?

Trong example, `keyboard`, `cable`, `cart` và `total` không được reassign sau initialization, nên `let` thể hiện invariant đó cho compiler và reader. `private` chưa cần vì example nằm trong một file nhỏ; access control trở nên có ý nghĩa khi tạo module/boundary, sẽ được giải thích ở chapter Properties & Access Control.

### Review questions — Runnable example

1. `@main` giải quyết vấn đề gì?
2. Vì sao file example không cần UIKit hoặc SwiftUI?
3. `swiftc -O` có thể làm output SIL khó đối chiếu với source hơn vì sao?
4. `let cart` có làm mọi object nằm trong cart “immutable tuyệt đối” trong mọi trường hợp không? Bạn cần biết thêm semantics nào để trả lời chính xác?

## 4. Từ executable đến iOS app bundle

Command-line example tạo một executable. iOS target còn phải tạo **app bundle**: directory có cấu trúc chứa executable, resources, metadata, embedded frameworks khi cần, provisioning information và code signature.

Pipeline đơn giản hóa:

```text
Swift/ObjC/C source + assets + configuration
                 ↓ Build system schedules compile/resource tasks
Object files + compiled resources + linked frameworks
                 ↓ Link + bundle
MyCommerce.app
                 ↓ Entitlements/provisioning/code signing
Installable/distributable artifact
```

### Linking

Compiler có thể compile từng source/module, nhưng executable cuối cần symbol từ nhiều object file và library. Linker giải quyết references và tạo binary image.

Sai lầm thường gặp:

- **Compile succeeds, link fails**: declaration đã nhìn thấy lúc compile nhưng implementation/symbol không có trong link inputs hoặc architecture không phù hợp.
- **Build and link succeed, launch fails**: app phụ thuộc dynamic framework nhưng framework không được embed/tìm thấy đúng. Apple mô tả trường hợp này là `dyld` launch crash.

### Code signing

iOS kiểm tra code signature như một phần security model. Apple nêu rõ iOS từ chối launch app có signature thiếu hoặc không hợp lệ. Vì vậy “code compile đúng” chưa đủ để app chạy trên device.

Signature liên kết executable/resources/entitlements với identity và phân phối. Không sửa nội dung trong `.app` sau signing rồi kỳ vọng signature vẫn hợp lệ.

### Static vs dynamic dependency

Ở mức mental model:

- **Static link** đưa code được dùng vào binary ở link time.
- **Dynamic framework/library** tồn tại như image riêng mà `dyld` phải tìm/load/resolve khi launch hoặc khi cần theo platform mechanism.

Trade-off không chỉ là “cái nào nhanh hơn”:

- build/iteration time;
- binary duplication/size;
- launch work;
- distribution/embedding constraints;
- module/team boundary;
- symbol/ABI compatibility.

Chỉ thay linkage sau khi đo build và launch, đồng thời kiểm tra distribution correctness.

## 5. iOS launch-time: điều gì xảy ra trước và sau `@main`?

### 5.1 OS nhận launch request

Khi user chạm icon hoặc hệ thống cần launch app cho một event được hỗ trợ, iOS chuẩn bị launch process. App phải thỏa security/code-signing/entitlement conditions. Một activation cũng có thể là resume nếu process còn sống; resume không giống cold launch.

### 5.2 `dyld` load executable và dependencies

Apple mô tả dynamic loader (`dyld`) đọc load commands, tìm executable/frameworks/dynamic libraries cần thiết, map chúng vào memory và resolve dynamic symbols. Việc này xảy ra trước khi app có thể chạy normal entry-point flow.

```text
Mach-O executable
  ├── load commands
  ├── code/data segments
  ├── linked-library references
  └── code-signature information
            ↓ dyld
      mapped images + resolved symbols
```

Nếu framework bắt buộc không tồn tại ở expected path, process có thể kết thúc trước khi breakpoint trong `main`/`AppDelegate` được chạy.

### 5.3 Pre-main work

Một số work có thể xảy ra trước `main`, ví dụ loader work và một số static initializer từ C/C++/Objective-C/runtime ecosystem. Apple khuyến nghị dùng dyld Activity instrument để đo static initializer/loader work thay vì quy toàn bộ slow launch cho `didFinishLaunching`.

> **Myth:** `@main` là instruction đầu tiên chạy trong process.
>
> **Reality:** `@main` xác định program entry point ở source model, nhưng OS/loader và pre-main work cần chuẩn bị process trước khi control tới entry point.

### 5.4 Entry point

Swift Language Reference cho phép một executable có một top-level entry point, thường qua `@main` hoặc top-level executable code theo rules của build.

Với SwiftUI:

```swift
import SwiftUI

@main
struct CommerceApp: App {
    var body: some Scene {
        WindowGroup {
            Text("Global Commerce")
        }
    }
}
```

`App` protocol cung cấp default implementation của `main()` để quản lý launch theo platform. `@main` chỉ vào conforming type là app entry.

Với UIKit app delegate lifecycle:

```swift
import UIKit

@main
final class AppDelegate: UIResponder, UIApplicationDelegate {
    func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
    ) -> Bool {
        true
    }
}
```

Theo Apple, UIKit launch sequence tạo `UIApplication` và app delegate, khởi động main event loop, thực hiện app-delegate launch callbacks, rồi kết nối scene. Chi tiết scene configuration phụ thuộc project/lifecycle setup và OS APIs; không nên nhét mọi startup responsibility vào một callback.

### 5.5 Event-driven runtime

Sau launch, iOS app không chạy “từ dòng đầu đến dòng cuối rồi thoát” như CLI. Nó sống theo event:

```text
Main event loop
  ↓ receives event
Touch / lifecycle / timer / network callback / task continuation
  ↓
App/framework handles event and updates state/UI
  ↓
Return control; wait for next event
```

UIKit và SwiftUI cung cấp abstraction khác nhau trên event/state/rendering, nhưng đều chạy bên trong process/lifecycle do platform quản lý.

### Review questions — App launch

1. Vì sao breakpoint trong `didFinishLaunching` không hit khi dynamic framework bị thiếu?
2. Code signing thuộc compiler, linker hay artifact/platform security stage?
3. Cold launch khác resume ở điểm quan trọng nào?
4. `@main` và `UIApplicationDelegate` có phải cùng một khái niệm không?
5. Tại sao đo pre-main và post-main riêng giúp điều tra slow launch?

## 6. Debug vs Release

Debug và Release thường khác ở optimization, debug information, assertions/configuration, instrumentation và đôi khi dependency/linkage choices. Vì thế:

```text
Same source
  ├── Debug settings → easier stepping, lower optimization, diagnostic support
  └── Release settings → optimized artifact, production configuration
```

Compiler phải giữ semantics của chương trình hợp lệ, nhưng optimizer có thể:

- inline function;
- specialize generic;
- devirtualize calls khi chứng minh được;
- loại dead code;
- thay đổi layout/instruction ordering mà debugger quan sát.

Một bug chỉ xuất hiện ở Release thường là tín hiệu cần kiểm tra:

- data race/timing assumption;
- code dựa vào side effect không được contract bảo đảm;
- `assert` hoặc debug-only guard biến mất/thay đổi behavior;
- environment/configuration/API endpoint khác;
- linker stripping/resource packaging;
- unsafe memory/lifetime assumption;
- compiler issue — chỉ kết luận sau khi có minimal reproducible evidence.

> **Warning**
>
> Đừng “fix” Release-only bug bằng cách tắt optimization toàn app trước khi biết root cause. Có thể dùng thay đổi optimization cục bộ như một experiment để khoanh vùng, không phải mặc định là production fix.

## 7. Memory implications

Chapter này chưa dạy Stack/Heap hay ARC chi tiết, nhưng cần tránh hai shortcut sai.

### Source syntax không quyết định đơn giản storage location

Nói “struct luôn ở stack, class luôn ở heap” là mental model quá cứng. Compiler/optimizer có thể quyết định representation, promote/box/elide allocation tùy context. Điều source-level quan trọng hơn:

- `Product`/`CartLine` là value types với value semantics;
- class instance có identity/reference semantics và chịu ARC ownership;
- storage/optimization cụ thể là implementation detail trừ khi API/unsafe code yêu cầu reasoning thấp hơn.

### Launch cũng tạo memory footprint

Loader map executable/framework images; runtime và framework khởi tạo metadata/state; app dựng dependency graph và cache. Nếu app eager-create mọi service/cache/database ở entry point, launch time và peak memory cùng tăng.

Với object được tạo ở launch, hỏi:

```text
Who creates it?
  ↓
Who owns it and for how long?
  ↓
Does it need process lifetime or feature lifetime?
  ↓
When should deinit/cleanup occur?
```

## 8. Concurrency implications

`@main` không phải lý do để chạy toàn bộ initialization nặng trên UI isolation.

UIKit documentation cho biết app-delegate launch callbacks quan trọng diễn ra synchronously trên main thread; work nặng ở đó làm launch chậm. Với SwiftUI, app/view state phù hợp thường liên quan MainActor, nhưng network/disk/decode cần thiết kế asynchronous và có ownership rõ.

Checklist khi defer launch work:

```text
Which task owns the work?
Which isolation domain owns resulting state?
Can the task be cancelled on logout/background?
Can it outlive the initial screen?
Can response ordering overwrite newer state?
What UI is usable before it finishes?
```

> **Myth:** Đưa initialization vào `Task { ... }` tự động làm launch nhanh và an toàn.
>
> **Reality:** Task chỉ thay đổi cách schedule/lifetime. Work vẫn có thể chạy trên MainActor, giữ dependency sống quá lâu, tạo duplicate request hoặc update stale state nếu ownership/cancellation không được thiết kế.

## 9. Architecture notes — Entry point là composition root, không phải god object

App entry là nơi hợp lý để **bắt đầu** composition, nhưng không phải nơi chứa toàn bộ business logic.

```text
@main App
  ↓ creates minimal AppContainer / root dependencies
Root flow
  ↓ creates feature dependencies when needed
Catalog / Cart / Checkout
```

Một composition root tốt:

- biết concrete implementation nào thỏa dependency abstraction;
- tạo dependency có lifetime đúng;
- chỉ initialize thứ cần cho first useful UI;
- không fetch tất cả data trước khi show screen;
- cho phép test feature với fake dependency mà không launch cả app;
- cô lập environment/configuration selection.

Ví dụ conceptual:

```swift
protocol ProductRepository {
    func fetchProducts() async throws -> [Product]
}

struct AppContainer {
    let productRepository: any ProductRepository
}
```

Tại Foundation, chỉ cần thấy dependency direction. Protocol, `any`, repository và DI sẽ được giải thích ở Phase 01/05/06; không cần áp dụng layer chỉ vì example có tên đẹp.

## 10. Production Case — Launch chậm sau một release

### Context

Global Commerce 8.4 thêm analytics SDK, feature-flag SDK và migration cho persistent Product cache. QA thấy simulator ổn. Sau rollout, p90 cold launch trên device cũ tăng rõ rệt.

### Symptom

```text
User taps icon
  ↓
Launch screen giữ lâu hơn
  ↓
Catalog first frame chậm 500–900 ms ở cohort thiết bị cũ
```

Warm resume gần như không đổi. Crash-free rate không giảm.

### Hypotheses

1. `dyld`/framework loading tăng vì thêm dynamic dependencies.
2. Cache migration đọc/ghi disk synchronously trong app launch callback.
3. Initial Catalog network request chậm.
4. SwiftUI first-body computation hoặc image decode nặng.
5. Device cohort đang bị unrelated OS regression.

### Investigation

Không chọn root cause bằng cảm giác. Team thu evidence:

1. Xcode Organizer/field launch metrics xác nhận regression chủ yếu ở cold launch, bắt đầu từ build 8.4.
2. Instruments App Launch tách loader/pre-main và post-main.
3. dyld Activity cho thấy loader work tăng, nhưng chỉ giải thích một phần nhỏ tổng regression.
4. Time profile/signpost quanh composition root và cache store cho thấy schema migration chạy synchronously trước first useful UI.
5. Network timeline bắt đầu sau migration, nên không phải nguồn của delay trước first frame.
6. A/B local build bỏ migration làm post-main time về gần baseline; giữ migration nhưng bỏ SDK không đủ giải quyết.

### Root Cause

Technical root cause là cache migration không thiết yếu cho first frame nhưng được chạy synchronously trong launch-critical path. Dynamic frameworks làm tăng thêm pre-main work, là contributing factor chứ không phải nguồn lớn nhất.

Process gap: test launch chỉ đo simulator/warm runs; không có cold-launch budget theo device class và không có field-metric gate sau staged rollout.

### Fix

- Mở first screen từ cache format đọc được hoặc empty state an toàn.
- Chạy migration có version/checkpoint sau first useful UI trên execution context phù hợp.
- Nếu migration bắt buộc trước khi đọc, chỉ migrate phần metadata tối thiểu rồi xử lý dữ liệu còn lại theo batch.
- Không start duplicate catalog refresh trong lúc migration hoàn tất.
- Review linkage/configuration của SDK dựa trên measurement và vendor/platform constraints; không đổi mù sang static.

### Prevention

- cold/warm launch performance test trên representative device;
- signpost cho composition, store open/migration và first useful UI;
- p50/p90 launch dashboard theo build/device/OS;
- launch budget cho dependency initialization;
- ADR yêu cầu đo pre-main/post-main trước khi thêm startup SDK;
- rollout theo stage và compare build cohorts.

> **Production lesson**
>
> “App launch” không phải một function. Nó là timeline qua OS/loader/pre-main/entry/framework/first frame. Chỉ tối ưu đúng segment sau khi measurement chứng minh segment đó chiếm cost.

## 11. Debug / Instruments

### Build-time failure map

| Symptom | Stage nghi ngờ trước | Evidence đầu tiên |
|---|---|---|
| Syntax/type diagnostic | parse/type check | compiler diagnostic + source location |
| Undefined symbol / duplicate symbol | link | linker command/error và target membership |
| Resource không có trong bundle | copy/bundle phase | built `.app`, build phase log |
| App không install/launch do signature | signing/platform validation | install log, codesign/provisioning diagnostics |
| `dyld` missing framework | launch loader | crash termination description, embed/link settings |
| Breakpoint sai dòng ở Release | optimization/debug info | build configuration và disassembly/call stack |

### Slow-launch tool map

1. **Xcode Organizer / field metrics** — regression có thật ngoài production, build/device/OS nào bị ảnh hưởng, p50 hay tail latency.
2. **Instruments App Launch / dyld Activity** — cost nằm ở loader/static initialization hay sau entry.
3. **Time Profiler** — hot call tree trong app/framework code.
4. **Points of Interest / signposts** — mốc composition, store open, migration, first useful content.
5. **Build settings and linked binary inspection** — dependency/linkage thay đổi giữa releases.

### Experimental discipline

Một experiment tốt thay đổi một dimension:

```text
Baseline build
  vs
Same build without synchronous migration
```

Không so simulator Debug với device Release rồi kết luận compiler optimization là nguyên nhân; quá nhiều biến thay đổi đồng thời.

## 12. Historical note

Swift dùng LLVM toolchain và native code generation từ đầu, nhưng language/runtime/distribution model đã tiến hóa. Swift 5 đưa ABI stability trên Apple platforms, giúp OS cung cấp Swift runtime compatibility theo platform model; điều này không có nghĩa mọi library ABI/API tự động ổn định hoặc app không còn bundle Swift-related dependencies trong mọi deployment scenario.

Lịch sử chỉ hữu ích ở đây để tránh suy luận: “Swift mới nên chắc chạy qua một VM/interpreter.” Production iOS app vẫn theo native executable + platform runtime/loading model.

## 13. Myth vs Reality

### Myth 1 — `swift MyFile.swift` chứng minh Swift là interpreted

**Reality:** Command-line tool có thể cung cấp trải nghiệm chạy trực tiếp source, nhưng production iOS app artifact vẫn được build thành executable trước khi chạy. Giao diện tool không phải bằng chứng về distribution/runtime model của iOS app.

### Myth 2 — Swift app chỉ là machine code, không có runtime cost

**Reality:** Native code vẫn tương tác Swift/Objective-C runtimes, metadata, dynamic dispatch, ARC, concurrency runtime và frameworks. Cost phải đo theo call path cụ thể.

### Myth 3 — Release luôn nhanh hơn ở mọi metric

**Reality:** Optimization thường cải thiện CPU/code, nhưng launch và runtime còn phụ thuộc binary/dependency size, loader work, configuration, I/O, network, cache và lifecycle. “Release” không thay thế measurement.

### Myth 4 — Thêm `Task` vào launch callback là đưa work xuống background

**Reality:** Task không đồng nghĩa background thread. Isolation/executor và work bên trong mới quyết định execution; lifetime/cancellation/order vẫn cần thiết kế.

## 14. Common Mistakes

### Học thuộc pipeline nhưng không phân lớp lỗi

Nói được “SIL → LLVM” nhưng không phân biệt compile/link/dyld/signing khiến kiến thức không giúp debugging.

### Khẳng định storage từ syntax

“Struct ở stack, class ở heap” bỏ qua escape analysis/optimization/boxing và đánh đồng semantics với storage implementation.

### Eager initialize toàn dependency graph

Tạo database, analytics, remote config, image cache và fetch data ngay ở app entry làm tăng launch CPU/I/O/memory, đồng thời ghép lifetime của mọi feature với process.

### Benchmark sai điều kiện

So cold device launch với warm simulator run, hoặc Debug build với Release build mà không kiểm soát variables.

### Nhìn thấy correlation rồi kết luận causation

Release thêm ba SDK và launch chậm không có nghĩa cả ba là root cause. Timeline/profile phải định lượng contribution.

### Dùng beta behavior như baseline stable

Tài liệu preview có thể mô tả version sắp tới. Handbook phải ghi rõ stable/beta và availability thay vì silently trộn.

## 15. Best Practices

- Dùng pipeline cấp cao để phân loại failure trước khi đi sâu tool/compiler internals.
- Ghi rõ compiler, language mode, SDK và deployment target khi report version-sensitive issue.
- Giữ entry/composition root nhỏ; initialize theo feature lifetime khi phù hợp.
- Đo cold, warm và resume như các activation scenarios khác nhau.
- Dùng field metrics để ưu tiên cohort thật, rồi Instruments để tìm call path.
- Tối ưu theo budget CPU/memory/I/O/first frame, không theo số dòng trong `AppDelegate`.
- Khi đọc SIL/IR, xem đó là evidence cho compiler implementation hiện tại, không là language guarantee.
- Với Release-only issue, tạo minimal reproduction và kiểm tra concurrency/unsafe/config trước khi quy lỗi cho optimizer.

## 16. Interview Questions

### Foundation — Swift source chạy thế nào?

> Swift source trở thành chương trình chạy được như thế nào?

**30-second answer**

Swift compiler parse và type-check source, lower qua SIL rồi LLVM IR để sinh native machine code; linker tạo executable với dependencies. Với iOS, executable nằm trong app bundle được ký. Khi launch, OS và `dyld` chuẩn bị process/dependencies trước khi control tới `@main`, rồi UIKit/SwiftUI chạy lifecycle và event loop.

**2–3 minute answer**

Tách build-time và launch-time. Build-time gồm compile, optimization, target code generation, link, bundle resources/entitlements và sign. Launch-time gồm platform validation, process creation, dyld mapping/resolution, pre-main work, program entry, framework initialization, scene/first frame. Nhấn mạnh compiler version khác language mode, và SIL là compiler IR chứ không phải bytecode VM được iPhone interpret.

**Deep Dive**

Đi vào error boundary (type/link/dyld/sign), Debug vs Release, static/dynamic linkage, field launch metrics, pre-main/post-main, ARC/runtime support và why native code không nghĩa zero runtime.

### Junior — `@main` là gì?

Một type gắn `@main` cung cấp top-level program entry qua `static main()` trực tiếp hoặc default implementation từ protocol/framework như SwiftUI `App`. Executable có tối đa một top-level entry point. Nó không đồng nghĩa “instruction đầu tiên của process”, vì OS/loader work xảy ra trước.

Follow-up:

1. Top-level executable code và `@main` có thể cùng tồn tại tùy ý không?
2. `AppDelegate` có luôn là `@main` trong mọi SwiftUI app không?
3. Tại sao missing dynamic framework có thể crash trước `@main`?

### Middle — Compiler version vs language mode

Một toolchain version có thể hỗ trợ nhiều language modes. Language mode chọn source rules/checking cho target; deployment target/SDK lại quyết định platform availability/runtime environment. Codebase nhiều target có thể migrate incremental, nên phải kiểm tra per-target setting và module boundary.

### Senior — Thiết kế launch architecture

Một câu trả lời mạnh nên:

- định nghĩa first useful UI và launch budget;
- tách critical initialization khỏi deferrable work;
- thiết kế composition/lifetime theo feature;
- xét background/termination/cancellation và duplicate startup work;
- dùng staged rollout, p50/p90 field metric, signpost và Instruments;
- cân nhắc dependency linkage/build/launch trade-off bằng measurement;
- có fallback khi config/network/store chưa sẵn sàng.

### Production — App chỉ chậm ở Release

Đừng trả lời “tắt optimization”. Hỏi build/OS/device/cold-warm/cohort, so configuration và dependency graph, lấy Organizer/MetricKit evidence, profile đúng Release build, kiểm tra race/timing/unsafe/config/resource/linker stripping, tạo minimal reproduction, rồi dùng thay đổi optimization cục bộ như experiment nếu cần.

### Interview trap

> Swift compiled thành native code, vậy gọi protocol method chắc chắn không có dynamic dispatch cost?

Không. Native code không loại mọi abstraction runtime. Dispatch strategy phụ thuộc type information, existential/generic/class/Objective-C boundary và optimization compiler chứng minh được. Cần profile trước khi biến code design thành “manual optimization”.

## 17. Exercises

### Easy — Vẽ hai pipeline

Không nhìn chapter, vẽ riêng build-time và launch-time. Đặt các từ sau đúng nơi: `type checking`, `SIL`, `LLVM IR`, `linker`, `code signing`, `dyld`, `@main`, `first frame`.

Acceptance criteria: không đặt `dyld` ở build-time và không đặt type checking trên iPhone launch path.

### Easy — Chạy CommerceCLI

1. Build example với Swift 6 language mode.
2. Đổi `unitPrice` từ `Int` thành `String` nhưng giữ phép nhân.
3. Ghi diagnostic và xác định stage đã chặn bug.
4. Sửa model theo hai cách, giải thích cách nào giữ domain invariant tốt hơn.

### Medium — So sánh representation

Emit SIL trước optimization và SIL/LLVM IR với `-O`. Chọn một function nhỏ, ghi lại ba transformation quan sát được. Dán nhãn rõ đâu là observation của compiler version hiện tại, không phải language guarantee.

### Medium — Classify failures

Với từng symptom, chọn stage đầu tiên cần điều tra và evidence:

1. `Cannot convert value of type 'String' to expected argument type 'Int'`.
2. `Undefined symbols for architecture arm64`.
3. App cài được nhưng crash với `Library not loaded`.
4. App không cài do invalid signature.
5. UI đầu tiên xuất hiện chậm nhưng không crash.

### Hard — Launch budget

Thiết kế launch plan cho Global Commerce có:

- account session trong Keychain;
- Product cache 50 MB cần migration;
- remote feature flags;
- analytics SDK;
- deep link vào Order Detail.

Phân loại: pre-first-frame bắt buộc, có thể defer, lazy-on-feature và background-resumable. Với mỗi work, ghi owner, isolation, cancellation, fallback, metric và failure policy.

### Debugging Lab — First frame regression

**Bug report:** build mới tăng p90 cold launch 700 ms, warm resume không đổi.

**Available evidence:** build number, device cohort, Organizer launch chart; chưa có Instruments trace.

Bạn phải:

1. lập ít nhất bốn hypotheses qua pre-main/post-main;
2. chọn tool/experiment để bác bỏ từng hypothesis;
3. định nghĩa minimal timeline/signposts;
4. đề xuất mitigation an toàn trước root cause nếu rollout impact lớn;
5. thiết kế regression protection.

Không được kết luận “SDK mới gây chậm” chỉ từ recent change.

### Engineering / Design Exercise — Composition root

Refactor một `CommerceApp` đang tạo database, network client, repositories, image prefetcher, analytics, remote config và chạy ba request trong initializer. Mục tiêu:

- first UI sẵn sàng với dependency tối thiểu;
- feature dependency được tạo theo lifetime;
- auth/logout hủy đúng work;
- deep link vẫn route được khi data chưa sẵn sàng;
- unit test Catalog không cần launch app.

Ghi trade-off bằng [ADR template](../templates/adr-template.md).

## 18. Cheat Sheet

```text
BUILD-TIME
source
→ parse/type check
→ SIL
→ LLVM IR
→ target machine code/object files
→ link
→ app bundle/resources/entitlements
→ sign

LAUNCH-TIME
launch request
→ OS validation/process
→ dyld load/resolve
→ pre-main work
→ @main entry
→ UIKit/SwiftUI lifecycle
→ scene/first useful UI
→ event loop
```

```text
Compiler version ≠ language mode ≠ deployment target/SDK
Compiled ≠ zero runtime
@main entry ≠ first work in process
Task ≠ background thread
Struct/class semantics ≠ fixed stack/heap rule
```

Failure classification:

```text
Diagnostic → compiler stage
Undefined symbol → linker
Invalid/missing bundle resource → build packaging
Invalid signature → signing/platform validation
Library not loaded → dyld/embed/link configuration
Slow first frame → measure pre-main and post-main timeline
```

## 19. Chapter Summary

1. **Problem:** Một tap mở app che giấu hai pipeline build-time và launch-time; trộn chúng làm debugging sai lớp.
2. **Mental model:** Swift source được compiler lower qua SIL/LLVM để sinh native artifact; iOS sau đó validate/load artifact, đi qua entry point và framework lifecycle.
3. **Usage rule:** Luôn phân loại failure/cost vào stage trước khi chọn tool hoặc fix.
4. **Mistake nguy hiểm:** Coi `@main` là toàn bộ launch, hoặc coi native code là không có runtime/loader/lifecycle cost.
5. **Production lesson:** Slow launch là timeline. Dùng field metrics xác định cohort, Instruments tách pre-main/post-main và experiment để chứng minh root cause.

## Related Chapters

- Planned: Phase 01 — `let`, `var`, type inference và strong typing
- Planned: Phase 02 — Stack/Heap mental model; ARC và ownership
- Planned: Phase 03 — Điều gì thực sự xảy ra tại `await`?
- Planned: Phase 04 — App lifecycle và scene lifecycle
- Planned: Phase 09 — App launch: pre-main/post-main
- [Glossary](../GLOSSARY.md)
- [Production Playbook](../PRODUCTION_PLAYBOOK.md)
- [Cross-reference Index](../CROSS_REFERENCE_INDEX.md)

## References

Primary sources, truy cập/xác minh ngày 2026-08-08:

1. Swift.org, [Swift Compiler — Compiler Architecture](https://www.swift.org/documentation/swift-compiler/).
2. Swift.org, [Swift 6.3 Released](https://www.swift.org/blog/swift-6.3-released/).
3. Swift.org, [Install Swift](https://www.swift.org/install/) — stable toolchain status.
4. Swift.org, [Migrating to Swift 6](https://www.swift.org/migration/) — compiler version và language mode; incremental target migration.
5. The Swift Programming Language, [Attributes — `main`](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/attributes/).
6. The Swift Programming Language, [Declarations — Top-Level Code](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/declarations/).
7. Apple Developer Documentation, [SwiftUI `App`](https://developer.apple.com/documentation/swiftui/app).
8. Apple Developer Documentation, [About the app launch sequence](https://developer.apple.com/documentation/uikit/about-the-app-launch-sequence).
9. Apple Developer Documentation, [Responding to the launch of your app](https://developer.apple.com/documentation/uikit/responding-to-the-launch-of-your-app).
10. Apple Developer Documentation, [Reducing your app’s launch time](https://developer.apple.com/documentation/xcode/reducing-your-app-s-launch-time).
11. Apple Developer Documentation, [Using the latest code signature format](https://developer.apple.com/documentation/xcode/using-the-latest-code-signature-format).
12. Apple Developer Documentation, [Addressing missing framework crashes](https://developer.apple.com/documentation/xcode/addressing-missing-framework-crashes).

> **Accuracy note**
>
> Pipeline SIL/LLVM mô tả compiler architecture hiện hành từ Swift.org. OS security, UIKit/SwiftUI launch sequence và performance tooling dựa trên Apple documentation. Những optimization cụ thể chỉ được nêu như khả năng compiler có thể thực hiện khi chứng minh an toàn, không phải guarantee rằng mọi build sẽ thực hiện chúng.
