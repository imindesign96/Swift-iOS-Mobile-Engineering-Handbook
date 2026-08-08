# Glossary

Glossary là định nghĩa canonical. Chapter liên kết về đây thay vì định nghĩa lại theo cách mâu thuẫn.

## Actor

Reference type bảo vệ mutable state của nó bằng actor isolation. Actor ngăn data race trên state được isolation đúng, nhưng không tự ngăn logical race qua suspension point.

## Actor isolation

Quy tắc xác định code/state nào được đồng bộ tuần tự trong cùng một actor domain và khi nào caller phải `await` để đi qua isolation boundary.

## ARC (Automatic Reference Counting)

Cơ chế quản lý lifetime của class instance bằng cách chèn retain/release theo ownership semantics. Khi không còn strong ownership, instance có thể `deinit`. ARC không phải tracing garbage collector.

## Cache invalidation

Chính sách quyết định lúc dữ liệu cache không còn hợp lệ, cần xóa, refresh hoặc được phục vụ dưới dạng stale. Nó bao gồm trigger, TTL/version, source of truth và failure policy.

## Cancellation

Tín hiệu yêu cầu asynchronous work dừng sớm. Trong Swift Concurrency, cancellation mang tính cooperative: code phải kiểm tra hoặc gọi API có phản ứng với cancellation và cleanup đúng.

## Copy-on-Write (CoW)

Optimization cho phép nhiều value tạm chia sẻ storage; storage chỉ được copy khi một bên cần mutation và không còn unique ownership. CoW là implementation strategy, còn value semantics là behavior mà caller quan sát.

## Data race

Hai execution context truy cập cùng memory đồng thời, ít nhất một access là write và thiếu synchronization phù hợp. Swift 6 language mode tăng compile-time checking để ngăn nhiều lớp data race.

## Existential type

Giá trị runtime có thể chứa một concrete value bất kỳ conform protocol, viết bằng `any Protocol`. Tính linh hoạt đi kèm type erasure/dynamic dispatch và có thể làm mất thông tin type cần cho một số operation.

## Global actor

Actor được chia sẻ toàn chương trình và dùng annotation để gom declarations vào một isolation domain. `MainActor` là global actor chuẩn thường dùng để cô lập UI state/work phù hợp.

## Idempotency

Thuộc tính cho phép lặp lại cùng một operation mà không tạo thêm side effect ngoài kết quả của lần đầu. Với payment/order, idempotency cần bảo vệ cả client state lẫn server contract.

## Identity

Khái niệm “cùng một thực thể” xuyên thời gian, khác với hai giá trị có nội dung bằng nhau. Class instance có reference identity; SwiftUI dùng stable identity để liên kết state/lifecycle với view description.

## Isolation domain

Biên sở hữu và tuần tự hóa access vào mutable state, ví dụ một actor, global actor hoặc primitive synchronization được thiết kế rõ. Hỏi “state thuộc domain nào?” giúp tránh shared mutable state vô chủ.

## Logical race

Kết quả sai do interleaving hoặc ordering không như business invariant yêu cầu, dù chương trình có thể không chứa data race. Actor reentrancy là một nguồn phổ biến: state có thể thay đổi trong lúc function đang suspended.

## MainActor

Global actor đại diện cho main-actor isolation. Dùng `@MainActor` nói về isolation contract, không nên rút gọn thành “mọi thứ chắc chắn chạy trên một OS thread trong mọi chi tiết implementation”.

## Opaque type

Return type viết bằng `some Protocol`: implementation chọn một concrete underlying type cố định, caller thấy capability của protocol nhưng compiler vẫn giữ type identity.

## Ownership

Quan hệ quyết định ai chịu trách nhiệm giữ một resource/object sống và khi nào quyền giữ đó kết thúc. Với ARC, strong reference thể hiện owning edge; weak/unowned là non-owning edge với lifetime assumptions khác nhau.

## Optional

Value type `Optional<Wrapped>` biểu diễn hai trạng thái: `.some(Wrapped)` hoặc `.none` (`nil`). Optional phù hợp khi absence là một state có nghĩa; nó không thay thế error detail hoặc workflow có nhiều hơn hai state.

## Reference semantics

Nhiều biến có thể tham chiếu cùng một identity; mutation qua một reference có thể quan sát được qua reference khác. Phù hợp khi domain cần shared identity/lifecycle.

## Retain cycle

Chu trình strong ownership khiến các object trong chu trình tiếp tục giữ nhau dù owner bên ngoài đã biến mất. Cycle phải được phá ở edge thực sự không sở hữu, không phải thêm `weak` ngẫu nhiên.

## Sendable

Protocol/marker diễn tả value có thể đi qua concurrency domain mà vẫn giữ data-race safety theo checking model của Swift. Conformance không thay thế việc thiết kế ownership và business invariant.

## Source of Truth

Nơi có quyền quyết định trạng thái hiện tại của một dữ liệu/feature. Một hệ thống có thể phối hợp server và local store, nhưng phải có policy rõ ràng thay vì nhiều source vô tình cạnh tranh.

## Suspension point

Vị trí asynchronous function có thể tạm dừng để executor chạy work khác, thường được đánh dấu bằng `await`. Suspension không đồng nghĩa block thread hay tự động chuyển sang background thread.

## Value semantics

Mỗi biến cư xử như một giá trị độc lập: mutation của một biến không làm caller quan sát biến khác thay đổi chỉ vì từng gán từ nhau. Implementation có thể dùng CoW để tránh copy storage ngay lập tức.

## Weak / Unowned

Cả hai là non-owning reference. `weak` thường Optional và tự về `nil` sau deallocation; `unowned` biểu diễn assumption rằng object còn sống khi access, vi phạm assumption có thể gây runtime failure.
