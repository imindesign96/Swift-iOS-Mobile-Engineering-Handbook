# Phase 01 — Swift Foundation

Phase này tập trung vào mục tiêu: **mô hình hóa domain bằng type an toàn trước khi framework tham gia**.

## Dependency map

```text
Input domain → type/operation phù hợp → compiler kiểm tra → state hợp lệ
      ↓
Runtime + Memory + Concurrency + Architecture
      ↓
Production evidence + Interview synthesis
```

## Learning outcomes

- Giải thích concept bằng behavior, constraint và trade-off.
- Xác định owner/state/failure/lifecycle cho Commerce flow.
- Dùng Swift compiler diagnostics, unit test pure Swift và debugger để quan sát branch/state. thay vì đoán root cause.
- Hoàn thành coding exercise, debugging lab và mock interview của phase.

## Chapters — Complete

- [01 — Một chương trình Swift chạy như thế nào?](01-how-a-swift-program-runs.md)
- [02 — `let`, `var`, type inference và strong typing](02-let-var-type-inference-and-type-safety.md)
- [03 — Optional và nil safety](03-optionals-and-nil-safety.md)
- [04 — Control flow, `switch` và pattern matching](04-control-flow-switch-va-pattern-matching.md)
- [05 — Function, parameter label và method](05-function-parameter-label-va-method.md)
- [06 — Closure, capture và `@escaping`](06-closure-capture-va-at-escaping.md)
- [07 — Enum và state modeling](07-enum-va-state-modeling.md)
- [08 — Struct, class, equality và identity](08-struct-class-equality-va-identity.md)
- [09 — Value semantics vs reference semantics](09-value-semantics-vs-reference-semantics.md)
- [10 — Property, initialization và access control](10-property-initialization-va-access-control.md)
- [11 — Extension và tổ chức capability](11-extension-va-to-chuc-capability.md)
- [12 — Protocol và protocol-oriented design](12-protocol-va-protocol-oriented-design.md)
- [13 — Generics, constraint và `associatedtype`](13-generics-constraint-va-associatedtype.md)
- [14 — `some` vs `any`: opaque và existential types](14-some-vs-any-opaque-va-existential-types.md)
- [15 — Error handling, `throws` và `Result`](15-error-handling-throws-va-result.md)
- [16 — Array, Set, Dictionary và collection semantics](16-array-set-dictionary-va-collection-semantics.md)
- [17 — String, Unicode và indexing](17-string-unicode-va-indexing.md)
- [18 — Codable fundamentals](18-codable-fundamentals.md)
- [99 — Phase Review: Swift Foundation](99-phase-review.md)

## Quality gate

Toàn bộ chapter có front matter `status: complete`, production case, debugging evidence, interview questions, exercises, cheat sheet, references và links nội bộ hợp lệ.
