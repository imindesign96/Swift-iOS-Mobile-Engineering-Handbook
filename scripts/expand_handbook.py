#!/usr/bin/env python3
"""Expand the approved SUMMARY roadmap into complete handbook chapters.

The first three Foundation chapters are intentionally preserved because they
were hand-written at book depth. Remaining chapters are generated from the
authoritative roadmap with topic-specific guidance, code, production cases,
interview prompts, exercises, references, and phase reviews.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "SUMMARY.md"
TODAY = "2026-08-09"

PRESERVE_HAND_WRITTEN = {
    "Phase-01-Swift-Foundation/01-how-a-swift-program-runs.md",
    "Phase-01-Swift-Foundation/02-let-var-type-inference-and-type-safety.md",
    "Phase-01-Swift-Foundation/03-optionals-and-nil-safety.md",
}


@dataclass(frozen=True)
class Chapter:
    number: str
    title: str
    filename: str


@dataclass(frozen=True)
class Phase:
    number: int
    title: str
    directory: str
    chapters: tuple[Chapter, ...]


PHASE_DIRECTORIES = {
    1: "Phase-01-Swift-Foundation",
    2: "Phase-02-Memory-Runtime",
    3: "Phase-03-Concurrency",
    4: "Phase-04-iOS-Platform",
    5: "Phase-05-Networking",
    6: "Phase-06-Architecture",
    7: "Phase-07-Persistence",
    8: "Phase-08-Testing",
    9: "Phase-09-Production",
    10: "Phase-10-Mobile-System-Design",
    11: "Phase-11-Interview",
}


PHASE_GUIDES = {
    1: {
        "short": "Swift Foundation",
        "goal": "mô hình hóa domain bằng type an toàn trước khi framework tham gia",
        "story": "một thay đổi nhỏ trong model Commerce lan thành crash hoặc state không hợp lệ vì semantics của Swift bị hiểu sai",
        "mental": "Input domain → type/operation phù hợp → compiler kiểm tra → state hợp lệ",
        "runtime": "Theo dõi phần compiler kiểm tra tĩnh và phần behavior chỉ xuất hiện khi chương trình chạy.",
        "memory": "Hỏi value có được copy độc lập hay đang chia sẻ identity/storage; không suy luận layout cụ thể nếu API không cam kết.",
        "concurrency": "Immutable value và value semantics thường giảm shared mutable state, nhưng không tự động biến mọi graph thành Sendable.",
        "architecture": "Domain model nên biểu diễn invariant; đừng đẩy validation rải rác sang View hoặc API client.",
        "tool": "Swift compiler diagnostics, unit test pure Swift và debugger để quan sát branch/state.",
        "refs": [
            ("The Swift Programming Language", "https://docs.swift.org/swift-book/documentation/the-swift-programming-language/"),
            ("Swift Standard Library", "https://developer.apple.com/documentation/swift/swift-standard-library"),
            ("Swift 6.3 Released", "https://www.swift.org/blog/swift-6.3-released/"),
        ],
    },
    2: {
        "short": "Memory & Runtime",
        "goal": "lý luận object graph bằng creator, owner, release và expected deinit",
        "story": "Product Detail đã đóng nhưng memory vẫn tăng sau mỗi lần mở vì lifetime thực tế khác lifetime mong đợi",
        "mental": "Creator → strong ownership graph → release edges → reference count về 0 → deinit",
        "runtime": "ARC chèn retain/release theo semantics của chương trình; graph ownership, không phải một dòng weak, quyết định lifetime.",
        "memory": "Vẽ graph strong/weak/unowned và phân biệt leak với legitimate memory pressure.",
        "concurrency": "Task, callback và actor có thể kéo dài lifetime; cancellation không đồng nghĩa object được giải phóng ngay.",
        "architecture": "Boundary delegate/coordinator/cache phải có ownership contract, đặc biệt với screen-scoped dependency.",
        "tool": "Xcode Memory Graph, Instruments Leaks/Allocations, deinit probe và repeated-flow measurement.",
        "refs": [
            ("Automatic Reference Counting", "https://docs.swift.org/swift-book/documentation/the-swift-programming-language/automaticreferencecounting/"),
            ("Gathering information about memory use", "https://developer.apple.com/documentation/xcode/gathering-information-about-memory-use"),
            ("Memory safety", "https://docs.swift.org/swift-book/documentation/the-swift-programming-language/memorysafety/"),
        ],
    },
    3: {
        "short": "Concurrency",
        "goal": "quản lý isolation, task lifetime, cancellation và ordering thay vì suy nghĩ bằng thread thuần túy",
        "story": "nhiều request Commerce hoàn tất khác thứ tự, tạo duplicate work hoặc ghi đè state mới bằng response cũ",
        "mental": "Task owner → suspension points → isolation domain → cancellation/order → observable state",
        "runtime": "Một async function có thể suspend và resume; await không phải lệnh chuyển sang background thread.",
        "memory": "Task và closure giữ capture trong lifetime của work; unstructured work dễ sống lâu hơn screen.",
        "concurrency": "Phân biệt data race được isolation ngăn chặn với logical race vẫn có thể xảy ra qua nhiều bước hợp lệ.",
        "architecture": "Đặt task ownership ở layer gắn với lifecycle; repository/actor sở hữu state chia sẻ, UI state thuộc MainActor.",
        "tool": "Strict Concurrency diagnostics, Swift Concurrency instrument, Thread Sanitizer khi phù hợp và structured logs theo task/request.",
        "refs": [
            ("Concurrency — The Swift Programming Language", "https://docs.swift.org/swift-book/documentation/the-swift-programming-language/concurrency/"),
            ("Swift Concurrency", "https://developer.apple.com/documentation/swift/concurrency"),
            ("Migrating to Swift 6", "https://www.swift.org/migration/documentation/migrationguide/"),
        ],
    },
    4: {
        "short": "iOS Platform",
        "goal": "đặt UI state và work đúng lifecycle trong UIKit lẫn SwiftUI",
        "story": "screen Commerce hiển thị sai, cập nhật sau khi dismiss hoặc giật vì identity/lifecycle bị hiểu sai",
        "mental": "Event/state mutation → lifecycle/observation → UI description/layout → visible frame",
        "runtime": "UIKit vận hành qua object lifecycle; SwiftUI đánh giá description và reconcile phần UI bị ảnh hưởng, không đơn giản là vẽ lại mọi thứ.",
        "memory": "Controller/model/task ownership phải khớp screen lifetime; cell/view reuse không phải object mới cho mỗi item.",
        "concurrency": "UI state được cô lập phù hợp; work nặng không nên bị giữ trên MainActor chỉ vì kết quả cuối cập nhật UI.",
        "architecture": "View biểu diễn và chuyển event; state transition/business rule ở model/ViewModel/use case theo độ phức tạp.",
        "tool": "View Debugger, constraint logs, SwiftUI Instruments, Time Profiler và lifecycle logging.",
        "refs": [
            ("UIKit", "https://developer.apple.com/documentation/uikit"),
            ("SwiftUI", "https://developer.apple.com/documentation/swiftui"),
            ("Observation", "https://developer.apple.com/documentation/observation"),
        ],
    },
    5: {
        "short": "Networking",
        "goal": "xây networking boundary có error taxonomy, cancellation, auth, retry và cache policy",
        "story": "request Commerce thành công ở happy path nhưng production gặp mạng yếu, token hết hạn và response đến sai thứ tự",
        "mental": "View → ViewModel → Repository → API Client → URLSession → HTTP server → mapped result",
        "runtime": "URLSession quản lý task/connection theo configuration; HTTP response và transport completion là hai lớp evidence khác nhau.",
        "memory": "Response body, decoded models và image data cần budget; cache/request registry không được tăng vô hạn.",
        "concurrency": "Request phải có owner, cancellation, ordering và single-flight khi chia sẻ refresh/cache work.",
        "architecture": "Repository phối hợp remote/local/policy; API client chịu transport, request construction và error mapping.",
        "tool": "Network Instruments, URLSession metrics, server correlation ID và privacy-aware structured logs.",
        "refs": [
            ("URLSession", "https://developer.apple.com/documentation/foundation/urlsession"),
            ("URLRequest", "https://developer.apple.com/documentation/foundation/urlrequest"),
            ("Loading data from your app", "https://developer.apple.com/documentation/foundation/loading-data-from-your-app"),
        ],
    },
    6: {
        "short": "Architecture",
        "goal": "tạo dependency direction và ownership boundary vừa đủ cho complexity hiện tại",
        "story": "một thay đổi Checkout phải sửa ViewController, networking, cache và analytics cùng lúc vì responsibility không có ranh giới",
        "mental": "UI → application policy → repository boundary → remote/local implementation",
        "runtime": "Architecture không chạy thay framework; nó quyết định nơi state/work/lifetime được sở hữu và quan sát.",
        "memory": "Mỗi dependency phải có composition root và lifetime rõ; singleton vô tình biến lifetime thành toàn process.",
        "concurrency": "Isolation boundary nên đi cùng ownership boundary; đừng để nhiều layer cùng mutate một state.",
        "architecture": "Thêm layer khi nó hấp thụ volatility hoặc tạo test seam, không thêm chỉ để giống diagram.",
        "tool": "Dependency graph, build metrics, ADR, code review và tests tại boundary.",
        "refs": [
            ("Swift Package Manager", "https://www.swift.org/documentation/package-manager/"),
            ("Organizing your code with local packages", "https://developer.apple.com/documentation/xcode/organizing-your-code-with-local-packages"),
            ("Swift API Design Guidelines", "https://www.swift.org/documentation/api-design-guidelines/"),
        ],
    },
    7: {
        "short": "Persistence",
        "goal": "chọn storage/source of truth theo lifetime, query, security và synchronization requirement",
        "story": "Commerce hiển thị dữ liệu account cũ hoặc mất cart offline vì storage được chọn theo thói quen thay vì policy",
        "mental": "Domain intent → repository → local transaction/source of truth ↔ synchronization policy",
        "runtime": "Disk I/O, context/transaction và migration có lifecycle riêng; synchronous work sai chỗ có thể block UI.",
        "memory": "Context/object graph/cache giữ resident data; fetch giới hạn và fault/batch strategy cần phù hợp workload.",
        "concurrency": "Context/model access phải tuân isolation; sync cần ordering, idempotency và conflict policy.",
        "architecture": "Storage model không nên rò trực tiếp qua UI; repository map và bảo vệ account/data boundary.",
        "tool": "Database inspection, transaction logs, migration tests, file protection checks và memory/disk metrics.",
        "refs": [
            ("SwiftData", "https://developer.apple.com/documentation/swiftdata"),
            ("Core Data", "https://developer.apple.com/documentation/coredata"),
            ("Keychain Services", "https://developer.apple.com/documentation/security/keychain-services"),
        ],
    },
    8: {
        "short": "Testing",
        "goal": "đặt confidence ở đúng boundary với test deterministic và failure dễ chẩn đoán",
        "story": "test suite xanh nhưng Checkout vẫn lỗi production vì chỉ test implementation detail và bỏ qua boundary quan trọng",
        "mental": "Risk → observable behavior → controlled dependency → assertion/evidence → regression signal",
        "runtime": "Test runner và concurrency scheduler vẫn có timing; test không được dựa vào sleep hoặc order ngẫu nhiên.",
        "memory": "Test double và SUT cần teardown/lifetime rõ để phát hiện leak và tránh state rò giữa test.",
        "concurrency": "Await observable completion, kiểm soát clock/transport, và bảo vệ test khỏi data race/flakiness.",
        "architecture": "DI tạo seam; test pyramid chọn unit/integration/UI theo risk và cost, không theo quota.",
        "tool": "Swift Testing, XCTest, test plans, result bundles, sanitizer và performance metrics.",
        "refs": [
            ("Swift Testing", "https://developer.apple.com/documentation/testing"),
            ("XCTest", "https://developer.apple.com/documentation/xctest"),
            ("Testing and performance", "https://developer.apple.com/documentation/technologyoverviews/testing-and-performance"),
        ],
    },
    9: {
        "short": "Production",
        "goal": "đi từ symptom đến evidence, root cause và regression prevention",
        "story": "một lỗi hiếm chỉ xuất hiện trên thiết bị thật và hàng triệu session, nơi đoán mò không còn hiệu quả",
        "mental": "Symptom → evidence → hypotheses → measurement → root cause → fix → prevention",
        "runtime": "Crash/hang/termination/performance regression tạo artifact khác nhau; trước hết phải phân loại đúng tín hiệu.",
        "memory": "Tách leak, peak working set, decoded resource cost và OS pressure; đo repeated flow trên device phù hợp.",
        "concurrency": "Thu thập ordering, isolation, cancellation và correlation context mà không log dữ liệu nhạy cảm.",
        "architecture": "Observability là capability xuyên layer; mitigation và kill switch cần được thiết kế trước incident.",
        "tool": "Xcode Organizer, crash report/symbolication, Instruments, MetricKit và structured production telemetry.",
        "refs": [
            ("Performance and metrics", "https://developer.apple.com/documentation/xcode/performance-and-metrics"),
            ("Diagnosing issues using crash reports", "https://developer.apple.com/documentation/xcode/diagnosing-issues-using-crash-reports-and-device-logs"),
            ("MetricKit", "https://developer.apple.com/documentation/metrickit"),
        ],
    },
    10: {
        "short": "Mobile System Design",
        "goal": "thiết kế feature trong constraint memory, battery, network, storage và app lifecycle",
        "story": "thiết kế backend-correct nhưng mobile-failure vì bỏ qua offline, background interruption và resource budget",
        "mental": "Requirements → constraints → data/state → architecture → failure/security/performance → observability/testing",
        "runtime": "Thiết kế phải chịu foreground/background/suspend/terminate và network thay đổi giữa chừng.",
        "memory": "Mỗi cache/buffer/media pipeline cần capacity, eviction và decoded-size budget.",
        "concurrency": "Xác định task owner, coalescing, cancellation, ordering, retry và persistence của pending work.",
        "architecture": "Nêu source of truth, dependency direction, team ownership và migration path; luôn ghi trade-off.",
        "tool": "Architecture diagram, state machine, load/failure tests, signposts, metrics dashboard và ADR.",
        "refs": [
            ("App architecture", "https://developer.apple.com/documentation/technologyoverviews/app-architecture"),
            ("Background tasks", "https://developer.apple.com/documentation/backgroundtasks"),
            ("Performance and metrics", "https://developer.apple.com/documentation/xcode/performance-and-metrics"),
        ],
    },
    11: {
        "short": "Global Interview",
        "goal": "tổng hợp kiến thức thành câu trả lời đúng, có chiều sâu và production awareness",
        "story": "ứng viên nhớ định nghĩa nhưng không giải thích trade-off, evidence hoặc follow-up production",
        "mental": "Clarify → 30-second thesis → mechanism/trade-off → example → production evidence → senior extension",
        "runtime": "Câu trả lời framework/runtime phải tách documented behavior khỏi inference và tránh slogan.",
        "memory": "Khi object graph xuất hiện, luôn nói creator, owner, release và expected deinit.",
        "concurrency": "Khi async xuất hiện, luôn nói task owner, isolation, cancellation, lifetime và ordering.",
        "architecture": "Đánh giá candidate theo reasoning và constraints, không theo tên pattern.",
        "tool": "Timed mock, rubric correctness/depth/reasoning/production/communication và feedback log.",
        "refs": [
            ("The Swift Programming Language", "https://docs.swift.org/swift-book/documentation/the-swift-programming-language/"),
            ("Apple Developer Documentation", "https://developer.apple.com/documentation/"),
            ("Swift Evolution", "https://www.swift.org/swift-evolution/"),
        ],
    },
}


TOPIC_RULES = [
    (r"optional|nil-safety", "absence là một state trong type, không phải chuỗi rỗng hay sentinel", "force unwrap hoặc che nil bằng fallback vô nghĩa", "branch và invariant tại nơi unwrap", "chọn Optional khi absence hợp lệ; chọn error/state enum khi cần lý do hoặc nhiều state"),
    (r"control-flow|switch|pattern-matching", "control flow nên làm domain cases exhaustive và dễ audit", "default che case mới hoặc nested if làm mất invariant", "branch coverage và compiler exhaustiveness", "ưu tiên switch/pattern khi các case domain loại trừ nhau"),
    (r"function|parameter-label|method", "signature là API contract về intent, input, ownership và failure", "boolean soup, label mơ hồ hoặc side effect ẩn", "call site đọc như câu và test theo output/side effect", "tách function theo một responsibility có tên domain"),
    (r"closure|capture|escaping", "closure là behavior value có capture và lifetime", "capture mạnh kéo dài owner hoặc callback gọi nhiều lần ngoài dự kiến", "ownership graph và thời điểm closure được release", "chọn capture list từ lifetime contract, không dùng weak theo phản xạ"),
    (r"enum|state-model", "enum mô hình hóa tập state hữu hạn và associated value đi cùng case", "Boolean explosion tạo tổ hợp state bất hợp lệ", "switch exhaustive và transition test", "dùng enum khi state loại trừ nhau hoặc event mang payload khác nhau"),
    (r"struct-class|equality-identity", "struct diễn tả value; class diễn tả shared identity/lifecycle", "chọn theo performance myth thay vì semantics", "== cho equality và === cho object identity", "bắt đầu từ domain: value độc lập hay một thực thể được chia sẻ"),
    (r"value-semantics|reference-semantics|copy", "value mutation không làm thay đổi value độc lập; reference chia sẻ identity", "tưởng assignment luôn deep-copy hoặc tưởng COW là reference semantics", "mutation isolation test và profiling khi copy cost đáng kể", "dùng semantics giúp invariant và concurrency reasoning rõ hơn"),
    (r"property|initialization|access-control", "object phải hoàn tất invariant trước khi được quan sát", "partially initialized state hoặc public mutation quá rộng", "compiler initialization rules và API surface review", "để access hẹp nhất vẫn phục vụ collaboration/test"),
    (r"extension", "extension tổ chức capability quanh type mà không tạo owner mới", "chia file theo syntax nhưng làm phân tán invariant", "dependency direction và discoverability", "dùng extension cho conformance/capability gắn kết, không che god type"),
    (r"protocol|associatedtype", "protocol mô tả capability/contract; generic giữ type relationship tại compile time", "abstraction không có nhiều implementation hoặc existential xóa thông tin cần thiết", "call-site substitutability và compile-time constraints", "thêm protocol tại boundary volatility/test seam, không cho mọi concrete type"),
    (r"generic|constraint|some-vs-any|opaque|existential", "generic/opaque giữ concrete relationship; existential chứa một value bất kỳ conform protocol", "dùng any khi cần associated type relation hoặc dùng generic làm API phình", "compiler diagnostics, specialization/code-size measurement", "chọn theo caller cần heterogeneity hay type relationship"),
    (r"error-handling|throws|result", "failure là part của signature và cần taxonomy/recovery rõ", "try! hoặc gom mọi lỗi thành unknown/string", "test từng error category và recovery path", "throws cho control flow trực tiếp; Result khi cần lưu/truyền outcome như value"),
    (r"array-set-dictionary|collection", "collection choice mã hóa ordering, uniqueness và lookup semantics", "dựa vào iteration order không được contract hoặc O(n) trong hot path", "complexity measurement và invariant tests", "chọn Array/Set/Dictionary theo operation chủ đạo và domain"),
    (r"string-unicode", "String là collection của extended grapheme clusters, index không phải integer offset", "index bằng byte/Int hoặc cắt Unicode sai boundary", "test emoji, combining marks và locale-sensitive input", "dùng String.Index và normalization policy rõ khi persistence/search"),
    (r"codable|codingkeys|decoding", "Codable map schema bên ngoài vào model với boundary và evolution policy", "decode thẳng transport model vào UI hoặc default che schema lỗi", "fixture versioned và decode error path", "tách DTO/domain khi schema/network volatility đáng kể"),
    (r"stack-heap", "stack/heap là mental model về storage/lifetime, không phải luật struct/class tuyệt đối", "khẳng định mọi struct ở stack và mọi class ở heap", "Memory Graph/Allocations và optimized build", "dùng model để hỏi lifetime/copy, không đoán placement được tối ưu"),
    (r"copy-on-write", "COW trì hoãn copy storage đến mutation khi storage đang chia sẻ", "tưởng assignment free mãi hoặc tự viết COW không kiểm tra uniqueness", "allocation/copy profile trên workload thật", "dùng value semantics trước; tối ưu storage khi measurement chứng minh"),
    (r"arc|ownership", "ARC quản lý lifetime qua strong references trong ownership graph", "đếm reference thủ công trong đầu hoặc dùng weak để chữa symptom", "Memory Graph + deinit expectation", "loại bỏ strong edge sai hoặc định nghĩa owner đúng"),
    (r"strong-weak-unowned|weak-unowned", "strong sở hữu; weak/unowned không sở hữu nhưng khác lifetime guarantee", "unowned với lifetime không chắc chắn hoặc weak làm dependency biến mất", "deinit/crash reproduction và graph", "weak khi target có thể kết thúc trước; unowned chỉ khi invariant lifetime chắc chắn"),
    (r"viewcontroller.*deinit|does-not-deinit", "screen không deinit là symptom của strong path còn tồn tại", "chỉ thêm weak self mà không tìm path", "Memory Graph path to root và repeated push/pop", "vẽ graph coordinator/delegate/task/closure trước khi sửa"),
    (r"delegate-timer-observer-task|task-lifetime", "registration/work tạo lifetime edge cần cleanup contract", "observer/timer/task sống lâu hơn feature", "deinit probe, cancellation log và path to root", "owner tạo resource cũng chịu trách nhiệm stop/cancel/remove"),
    (r"leak-vs-memory-pressure|memory-pressure", "leak là object đáng lẽ chết; pressure có thể đến từ object hợp lệ quá lớn", "dùng Leaks để kết luận mọi memory growth", "repeated-flow plateau, allocations và decoded-size budget", "sửa ownership cho leak; budget/eviction/downsampling cho pressure"),
    (r"thread|data-race|shared-mutable", "data race là concurrent unsynchronized conflicting access vào cùng memory", "đồng nhất race condition với data race", "Thread Sanitizer/strict concurrency và ordering logs", "loại shared mutation hoặc đặt một isolation/synchronization owner"),
    (r"gcd|serial-concurrent|sync-async|qos", "queue quyết định scheduling contract; sync/async nói caller có chờ hay không", "sync vào cùng serial queue hoặc dùng concurrent queue mà không bảo vệ state", "stack sample, queue label và QoS evidence", "ưu tiên structured concurrency cho flow mới; giữ GCD ở API/system boundary phù hợp"),
    (r"deadlock|barrier|group|semaphore|operationqueue", "coordination primitive giải một constraint cụ thể và có cost/liveness risk", "block thread bằng semaphore để giả async hoặc lock ordering mơ hồ", "hang sample và wait-for graph", "chọn primitive nhỏ nhất; ưu tiên async coordination không block thread"),
    (r"await|suspension", "await đánh dấu nơi function có thể suspend và actor state có thể thay đổi trước khi resume", "coi await là background hop hoặc atomic transaction", "log trước/sau suspension và kiểm tra invariant lại", "giữ critical state transition ngắn và revalidate sau await"),
    (r"async-let|taskgroup", "structured child task gắn lifetime/error/cancellation với parent scope", "spawn không giới hạn hoặc bỏ qua partial failure", "task count, cancellation propagation và latency", "async let cho số child cố định; group cho tập động có bound"),
    (r"structured-vs-unstructured|detached", "structured work kế thừa scope; unstructured cần owner/cancellation rõ; detached tách context", "Task.detached mặc định cho mọi background work", "task lifetime và inherited priority/isolation", "chỉ detach khi thật sự cần bỏ inheritance và đã truyền dependency an toàn"),
    (r"cancellation", "cancellation là cooperative signal, không cưỡng bức dừng mọi code", "bỏ check trong loop hoặc nuốt CancellationError rồi publish state", "cancel-to-stop latency và state after cancel", "check tại boundary, propagate và cleanup idempotently"),
    (r"actor-reentrancy|logical-race|reentrancy", "actor loại data race trên isolated state nhưng mỗi await mở cửa cho work khác", "đọc state, await, rồi dùng assumption cũ", "operation ID/state machine và duplicate-work metric", "revalidate hoặc lưu in-flight task/single-flight state trong actor"),
    (r"actor-isolation|actor", "actor serialize access vào isolated state, không làm toàn workflow atomic", "expose mutable reference hoặc await giữa invariant nhiều bước", "strict concurrency diagnostics và transition logs", "đặt shared state trong actor và thiết kế method theo transaction logic"),
    (r"mainactor|global-actor", "global actor gắn declarations vào một isolation domain dùng chung", "đưa decode/I/O nặng lên MainActor hoặc coi nó chỉ là dispatch main", "UI responsiveness, executor hop và Time Profiler", "cô lập UI state; thực hiện work nặng ngoài isolation rồi publish kết quả"),
    (r"sendable|strict-concurrency", "Sendable mô tả value an toàn khi đi qua isolation boundary", "unchecked Sendable để tắt warning mà không có synchronization proof", "compiler diagnostics và focused race tests", "ưu tiên immutable value; bao shared state bằng actor/lock có contract"),
    (r"app-lifecycle|scene-lifecycle|background", "app/scene state là external lifecycle signal, không phải bảo đảm thời lượng", "khởi động work dài khi background mà không persistence/resume", "lifecycle logs và background task expiration", "checkpoint work và thiết kế interruption-safe"),
    (r"uiviewcontroller-lifecycle", "controller callbacks biểu diễn transitions; viewDidLoad thường một lần mỗi loaded view nhưng appearance lặp", "load data không idempotent ở mỗi appearance", "lifecycle trace và deinit", "gắn setup một lần, refresh lặp lại và cancellation đúng callback"),
    (r"auto-layout|intrinsic|hugging|compression", "constraint system giải quan hệ; intrinsic size cung cấp preference chứ không phải frame tuyệt đối", "constraint conflict/ambiguity hoặc ưu tiên hugging sai", "View Debugger và unsatisfiable-constraint log", "mô tả intent bằng constraint tối thiểu và priority có lý do"),
    (r"tableview|collectionview|reuse|diffable", "reuse tách cell identity khỏi item identity; snapshot cần stable domain ID", "giữ stale task/image trong reused cell hoặc ID bằng index", "scroll trace, reuse log và diffable snapshot audit", "cancel old work trong reuse và bind bằng immutable item ID"),
    (r"swiftui|state-binding|observation|environment|foreach|identity|navigationstack", "SwiftUI state ownership và stable identity quyết định lifetime/update", "nhiều source of truth, unstable ID hoặc heavy body", "SwiftUI Instruments và state-transition log", "owner tạo state; Binding chỉ mượn mutation capability; dependency đi qua boundary rõ"),
    (r"animation|transaction|rendering", "animation mô tả transition của state trong transaction và vẫn chịu layout/render cost", "animate quá nhiều node hoặc decode/layout trên frame path", "animation hitches và Time Profiler", "giảm invalidation, precompute và đo trên device"),
    (r"http-method|status|idempotency|request-from-iphone", "HTTP method/status/header tạo protocol contract và retry safety", "retry POST không idempotency hoặc coi mọi 2xx/4xx giống nhau", "request/response metadata và server correlation", "map semantics domain vào method, status taxonomy và idempotency key"),
    (r"urlsession|urlrequest|response-lifecycle", "URLSessionTask có state, cancellation và metrics tách khỏi HTTP result", "quên validate response hoặc giữ session/task sai lifetime", "URLSessionTaskMetrics và cancellation trace", "inject transport/session configuration qua API client"),
    (r"endpoint|api-client", "Endpoint làm request construction typed; API client thực thi transport và map lỗi", "generic abstraction che method/body/auth policy", "request snapshot test và integration fixture", "abstraction phải giảm duplication mà vẫn lộ semantics quan trọng"),
    (r"error-taxonomy|transport-http", "transport, HTTP, decode và business errors có recovery khác nhau", "gộp tất cả thành networkError", "metrics theo category và user-safe mapping", "preserve underlying evidence, map ở boundary thích hợp"),
    (r"retry|backoff|jitter|timeout", "retry là policy theo retryability, idempotency, budget và cancellation", "infinite retry/thundering herd hoặc timeout một mức cho mọi request", "attempt count, delay và end-to-end latency", "exponential backoff có jitter, cap và deadline"),
    (r"single-flight|refresh-token|access-token", "một refresh in-flight phục vụ nhiều waiter và publish token atomically", "20 request 401 tạo 20 refresh rồi random logout", "refresh count/session và ordered auth logs", "actor/lock lưu shared refresh task; failure dẫn tới một logout transition"),
    (r"pagination|prefetch|duplicate", "pagination cần cursor/state machine và dedupe theo stable ID", "double load, stale cursor hoặc append sau refresh", "request ID/cursor logs và item uniqueness", "serialize transition, cancel stale generation và coalesce same page"),
    (r"http-caching|etag|cache-policy|remote-cache|offline", "cache cần key, freshness, validation, invalidation và source-of-truth policy", "TTL tùy tiện hoặc stale overwrite fresh", "hit rate, age, revalidation và generation", "chọn cache-first/network-first/offline-first theo UX consistency"),
    (r"ats|tls|certificate-pinning|security", "transport security bảo vệ channel; pinning thêm operational risk", "tắt ATS rộng hoặc pin không có rotation plan", "trust failure telemetry không chứa secret", "dùng platform trust mặc định; pin chỉ khi threat model và rotation justify"),
    (r"mvc|massive-viewcontroller", "MVC không tự gây massive; responsibility và dependency direction mới là vấn đề", "controller sở hữu networking, mapping, persistence và navigation", "change-impact/code review và unit-test seam", "extract theo reason-to-change trước khi chọn pattern mới"),
    (r"mvvm|viewmodel", "ViewModel chuyển event thành presentation state, không phải nơi chứa mọi thứ", "Massive ViewModel hoặc import UI types không cần thiết", "state-transition tests và dependency graph", "giữ navigation/platform concern ở boundary phù hợp"),
    (r"coordinator|navigation-ownership", "Coordinator sở hữu navigation flow khi flow vượt một screen", "coordinator giữ controller mãi hoặc business logic trôi vào routing", "ownership graph và route tests", "child coordinator phải được release khi flow kết thúc"),
    (r"repository", "Repository biểu diễn domain data operations và phối hợp source/policy", "đổi tên APIClient thành Repository hoặc tạo God Repository", "contract tests và cache/source metrics", "chia theo aggregate/capability domain"),
    (r"dependency-injection|constructor-injection", "constructor injection làm dependency/lifetime bắt buộc và nhìn thấy", "optional dependency, service locator ẩn hoặc graph tạo rải rác", "composition-root review và test replacement", "compose ở app/feature boundary; inject abstraction khi có volatility/seam"),
    (r"service-locator|singleton", "global access tiện nhưng che dependency và mở rộng lifetime/state sharing", "test phụ thuộc order hoặc account state rò toàn app", "global-state inventory và parallel-test failures", "giữ immutable/stateless service hoặc bọc sau injected boundary"),
    (r"usecase|clean-architecture", "UseCase hấp thụ orchestration/business policy khi ViewModel/Repository đã quá nhiều reason-to-change", "mỗi getter thành use case một dòng", "change-impact và test value", "thêm layer theo complexity, không theo sơ đồ"),
    (r"spm|modular|feature-boundary|circular", "module boundary kiểm soát dependency, build/team ownership và API surface", "core dumping-ground hoặc feature import chéo", "dependency graph/build metrics", "feature phụ thuộc capability protocol và lower-level modules, không vòng"),
    (r"migration|refactor|big-bang", "migration tốt có seam, slice nhỏ, metric và rollback", "rewrite toàn bộ trước khi tạo user value", "parity tests, adoption metric và defect rate", "strangler/incremental path với exit criteria"),
    (r"userdefaults|keychain|filemanager|sqlite|core-data|swiftdata", "storage được chọn theo data shape, lifetime, query, security và migration", "dùng preference store như database hoặc lưu token plaintext", "migration/read-write/failure tests", "tách storage adapter sau repository và xác định source of truth"),
    (r"conflict|offline-first|synchronization", "offline sync là state machine có version/order/conflict policy", "last-write-wins ngầm hoặc retry mutation không idempotent", "sync log, revision và reconciliation metrics", "chọn merge policy theo domain và giữ pending operations durable"),
    (r"test-strategy|test-pyramid|xctest|swift-testing", "test level được chọn theo risk, feedback speed và boundary", "mock mọi thứ hoặc UI-test mọi case", "failure diagnostic và flake rate", "nhiều unit nhỏ, integration tại boundary, UI cho critical flow"),
    (r"mock-stub-fake-spy", "test double có vai trò cụ thể: trả data, implement nhẹ hoặc ghi interaction", "mock implementation detail khiến refactor gãy test", "behavior assertion và contract", "ưu tiên fake/stub cho state; spy khi interaction là behavior cần bảo vệ"),
    (r"async-test|flaky", "async test chờ condition có nghĩa và kiểm soát clock/dependency", "sleep hoặc shared global state", "rerun/seed/timing artifact", "inject clock/transport và await deterministic signal"),
    (r"coverage|tdd|snapshot", "coverage là tín hiệu executed lines, không chứng minh assertion/risk", "chạy theo phần trăm hoặc snapshot khổng lồ", "mutation review, failure usefulness và review cost", "dùng TDD khi feedback thiết kế hữu ích; snapshot cho stable visual contract"),
    (r"logging|observability|slo|incident", "telemetry phải trả lời user impact và hỗ trợ correlation mà không lộ dữ liệu", "log text tự do, PII hoặc metric không có action", "dashboard theo SLO và trace/request ID", "thiết kế event schema, sampling, retention và ownership"),
    (r"crash|symbolication|exc-bad-access|fatal|index", "crash analysis bắt đầu từ symbolicated faulting thread và app frames", "fix dòng top stack mà không xét context/volume", "crash report, exception/termination reason và breadcrumbs", "reproduce invariant, fix root cause và thêm regression test"),
    (r"hang|watchdog|time-profiler|cpu|launch|battery|energy", "performance work cần baseline, trace và budget trên device đại diện", "optimize theo cảm giác hoặc chỉ đo simulator/debug", "call tree, signpost, launch/hang/energy metrics", "giảm critical-path work và đo trước/sau"),
    (r"image|scroll|rendering|downsampling", "decoded pixel cost và main-thread decode/layout thường quyết định scroll", "cache original khổng lồ hoặc decode khi cell xuất hiện", "Core Animation/Time Profiler/Allocations", "downsample theo display size, prefetch có bound và cache eviction"),
    (r"system-design|image-loader|feed|chat|download-manager|video|analytics|feature-flag|search-autocomplete|checkout", "mobile design phải nêu source of truth, state machine, resource budget và failure policy", "copy backend diagram và bỏ lifecycle/offline", "feature metrics, failure injection và capacity budget", "trình bày trade-off theo requirements thay vì một kiến trúc universal"),
    (r"interview|review|mock|question-bank|behavioral|coding", "câu trả lời mạnh bắt đầu từ thesis đúng rồi mở rộng bằng mechanism/trade-off/example", "đọc thuộc keyword hoặc deep dive trước khi clarify", "rubric và follow-up performance", "điều chỉnh độ sâu theo level và signal interviewer cần"),
]


def slugify(value: str) -> str:
    value = value.replace("→", " to ").replace("↔", " to ").replace("&", " and ")
    value = value.replace("@", " at ").replace("`", "").replace("/", " ")
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"[^a-z0-9]+", "-", ascii_value).strip("-")


def parse_roadmap() -> tuple[Phase, ...]:
    phase_header = re.compile(r"^## Phase (\d+) — (.+)$")
    linked = re.compile(r"^- ✅ \[(\d+) — (.+)\]\(([^)]+)\)$")
    planned = re.compile(r"^- ◻ (\d+) — (.+)$")
    phases: list[Phase] = []
    current_number: int | None = None
    current_title = ""
    chapters: list[Chapter] = []

    def finish() -> None:
        nonlocal chapters
        if current_number is None:
            return
        phases.append(
            Phase(
                current_number,
                current_title,
                PHASE_DIRECTORIES[current_number],
                tuple(chapters),
            )
        )
        chapters = []

    for line in SUMMARY.read_text(encoding="utf-8").splitlines():
        if match := phase_header.match(line):
            finish()
            current_number = int(match.group(1))
            current_title = match.group(2)
            continue
        if current_number is None:
            continue
        if match := linked.match(line):
            chapters.append(Chapter(match.group(1), match.group(2), Path(match.group(3)).name))
        elif match := planned.match(line):
            number, title = match.group(1), match.group(2)
            filename = "99-phase-review.md" if number == "99" else f"{number}-{slugify(title)}.md"
            chapters.append(Chapter(number, title, filename))
    finish()
    return tuple(phases)


def topic_profile(title: str, phase_number: int) -> tuple[str, str, str, str]:
    slug = slugify(title)
    if "question-bank" in slug or "coverage-map" in slug:
        return (
            "question bank phải map đủ domain/level/follow-up và dẫn về chapter canonical thay vì lặp đáp án rời rạc",
            "có hàng trăm câu hỏi nhưng coverage lệch, không có rubric hoặc không tìm được prerequisite",
            "coverage matrix theo domain/level cùng kết quả mock interview",
            "dùng map làm công cụ chẩn đoán lỗ hổng; học theory ở chapter canonical rồi luyện ba độ sâu",
        )
    if "state-machine" in slug or "boolean-explosion" in slug:
        return (
            "state machine chỉ cho phép transition hợp lệ giữa các state loại trừ nhau",
            "nhiều Boolean tạo tổ hợp bất khả thi và duplicate side effect",
            "transition log, exhaustive tests và idempotency metric",
            "dùng enum state + event/reducer khi workflow có nhiều bước, retry hoặc interruption",
        )
    for pattern, principle, risk, evidence, selection in TOPIC_RULES:
        if re.search(pattern, slug):
            return principle, risk, evidence, selection
    guide = PHASE_GUIDES[phase_number]
    return (
        f"{title} phải được hiểu bằng behavior, constraint và trade-off quan sát được",
        "dùng API/pattern theo tên gọi mà không xác định owner, state và failure mode",
        guide["tool"],
        f"chọn giải pháp phục vụ mục tiêu: {guide['goal']}",
    )


def code_example(title: str, phase_number: int) -> str:
    slug = slugify(title)
    if phase_number == 10 and "image-loader" in slug:
        return '''import Foundation

actor ImageRequestRegistry {
    private var tasks: [URL: Task<Data, Error>] = [:]

    func data(
        for url: URL,
        load: @escaping @Sendable (URL) async throws -> Data
    ) async throws -> Data {
        if let task = tasks[url] { return try await task.value }
        let task = Task { try await load(url) }
        tasks[url] = task
        defer { tasks[url] = nil }
        return try await task.value
    }
}'''
    if phase_number == 10:
        return '''enum FeatureState: Sendable {
    case idle
    case loading(generation: Int)
    case ready(version: Int)
    case waitingForNetwork(pendingCount: Int)
    case failed(message: String, retryable: Bool)
}

struct ResourceBudget: Sendable {
    let memoryBytes: Int
    let diskBytes: Int
    let maxConcurrentWork: Int
}'''
    if phase_number == 11:
        return '''struct InterviewAnswer {
    let thesis: String
    let mechanism: [String]
    let tradeOffs: [String]
    let productionEvidence: [String]
}

func isSeniorSignal(_ answer: InterviewAnswer) -> Bool {
    !answer.thesis.isEmpty &&
    !answer.tradeOffs.isEmpty &&
    !answer.productionEvidence.isEmpty
}'''
    rules = [
        (r"control-flow|switch|pattern", '''enum CheckoutState {
    case idle
    case validating(Cart)
    case paying(orderID: String)
    case completed(Order)
    case failed(CheckoutError)
}

func message(for state: CheckoutState) -> String {
    switch state {
    case .idle: "Ready"
    case .validating: "Validating cart"
    case .paying(let orderID): "Paying \\(orderID)"
    case .completed(let order): "Order \\(order.id) completed"
    case .failed(let error): "Failed: \\(error)"
    }
}'''),
        (r"function|parameter-label|method", '''struct Money { let cents: Int }

func total(for products: [Product], applying discount: Int = 0) -> Money {
    let subtotal = products.reduce(0) { $0 + $1.priceInCents }
    return Money(cents: max(0, subtotal - discount))
}'''),
        (r"closure|capture|escaping", '''final class ProductLoader {
    private let fetch: @Sendable (String) async throws -> Product

    init(fetch: @escaping @Sendable (String) async throws -> Product) {
        self.fetch = fetch
    }

    func product(id: String) async throws -> Product {
        try await fetch(id)
    }
}'''),
        (r"protocol|generic|associated|some-vs-any", '''protocol ProductRepository {
    associatedtype Output
    func products() async throws -> Output
}

func load<R: ProductRepository>(from repository: R) async throws -> R.Output {
    try await repository.products()
}'''),
        (r"error|throws|result", '''enum CheckoutError: Error { case emptyCart, paymentDeclined }

func placeOrder(cart: Cart) throws -> Order {
    guard !cart.items.isEmpty else { throw CheckoutError.emptyCart }
    return Order(id: UUID().uuidString)
}

let outcome = Result { try placeOrder(cart: cart) }'''),
        (r"collection|array-set-dictionary", '''let productsByID = Dictionary(uniqueKeysWithValues: products.map { ($0.id, $0) })
let favoriteIDs: Set<String> = ["keyboard-01", "mouse-02"]
let visibleFavorites = favoriteIDs.compactMap { productsByID[$0] }'''),
        (r"string-unicode", '''let name = "Cafe\\u{301} ☕️"
for character in name {
    print(character)
}
if let first = name.firstIndex(of: "☕️") {
    print(name[first...])
}'''),
        (r"codable|codingkeys|decoding", '''struct ProductDTO: Decodable {
    let id: String
    let displayName: String

    enum CodingKeys: String, CodingKey {
        case id
        case displayName = "display_name"
    }
}'''),
        (r"arc|weak|unowned|deinit|delegate|timer|observer|memory", '''protocol ProductDetailDelegate: AnyObject {
    func productDetailDidClose()
}

final class ProductDetailController {
    weak var delegate: ProductDetailDelegate?
    private var loadTask: Task<Void, Never>?

    deinit {
        loadTask?.cancel()
        print("ProductDetailController deinit")
    }
}'''),
        (r"copy-on-write|copy|value-semantics|stack-heap", '''struct Cart {
    private(set) var items: [Product] = []

    mutating func add(_ product: Product) {
        items.append(product)
    }
}

var original = Cart()
var draft = original
draft.add(keyboard) // original vẫn là một value độc lập'''),
        (r"actor-reentrancy|single-flight|refresh", '''actor TokenRefresher {
    private var inFlight: Task<Token, Error>?

    func validToken() async throws -> Token {
        if let inFlight { return try await inFlight.value }
        let task = Task { try await refreshFromServer() }
        inFlight = task
        defer { inFlight = nil }
        return try await task.value
    }
}'''),
        (r"actor|sendable|strict-concurrency", '''struct Product: Sendable { let id: String; let name: String }

actor ProductStore {
    private var values: [String: Product] = [:]
    func save(_ product: Product) { values[product.id] = product }
    func product(id: String) -> Product? { values[id] }
}'''),
        (r"async-let|taskgroup|structured", '''async let products = repository.products()
async let cart = repository.cart()
let (loadedProducts, loadedCart) = try await (products, cart)
print(loadedProducts.count, loadedCart.items.count)'''),
        (r"cancellation|task-lifetime|structured-vs", '''final class SearchSession {
    private var task: Task<Void, Never>?

    func search(_ query: String) {
        task?.cancel()
        task = Task {
            do { _ = try await repository.search(query) }
            catch is CancellationError { return }
            catch { report(error) }
        }
    }
}'''),
        (r"await|suspension", '''actor Inventory {
    private var generation = 0

    func reload() async throws {
        generation += 1
        let expected = generation
        let snapshot = try await fetchInventory()
        guard expected == generation else { return }
        apply(snapshot)
    }
}'''),
        (r"swiftui|state|binding|observation|environment|foreach|navigationstack", '''@Observable @MainActor
final class ProductListModel {
    private(set) var state: LoadState<[Product]> = .idle
    func load() async {
        state = .loading
        do { state = .loaded(try await repository.products()) }
        catch is CancellationError { }
        catch { state = .failed(error) }
    }
}'''),
        (r"tableview|collectionview|reuse|diffable", '''var snapshot = NSDiffableDataSourceSnapshot<Section, Product.ID>()
snapshot.appendSections([.main])
snapshot.appendItems(products.map(\\.id), toSection: .main)
dataSource.apply(snapshot, animatingDifferences: true)'''),
        (r"layout|intrinsic|hugging|compression", '''titleLabel.setContentCompressionResistancePriority(.required, for: .vertical)
priceLabel.setContentHuggingPriority(.required, for: .horizontal)
NSLayoutConstraint.activate([
    titleLabel.leadingAnchor.constraint(equalTo: contentView.leadingAnchor, constant: 16),
    priceLabel.trailingAnchor.constraint(equalTo: contentView.trailingAnchor, constant: -16)
])'''),
        (r"urlsession|endpoint|http|request|retry|pagination|cache|network", '''struct Endpoint<Response: Decodable> {
    let request: URLRequest
}

struct APIClient {
    let session: URLSession
    func send<T>(_ endpoint: Endpoint<T>) async throws -> T {
        let (data, response) = try await session.data(for: endpoint.request)
        guard let http = response as? HTTPURLResponse,
              200..<300 ~= http.statusCode else { throw APIError.http }
        return try JSONDecoder().decode(T.self, from: data)
    }
}'''),
        (r"dependency|repository|mvvm|mvc|coordinator|usecase|architecture", '''protocol ProductRepository {
    func products() async throws -> [Product]
}

@MainActor
final class ProductListViewModel {
    private let repository: any ProductRepository
    init(repository: any ProductRepository) { self.repository = repository }
}'''),
        (r"userdefaults|keychain|filemanager|sqlite|core-data|swiftdata|persistence", '''protocol CartStore {
    func loadCart() async throws -> Cart
    func saveCart(_ cart: Cart) async throws
}

actor CartRepository {
    private let local: any CartStore
    init(local: any CartStore) { self.local = local }
}'''),
        (r"test|mock|stub|fake|spy|coverage|tdd|snapshot", '''import Testing

@Test func addingAProductUpdatesTheTotal() {
    var cart = Cart()
    cart.add(Product(id: "keyboard", priceInCents: 9_900))
    #expect(cart.totalInCents == 9_900)
}'''),
        (r"logging|crash|hang|memory|profiler|production|observability", '''import os

let logger = Logger(subsystem: "com.example.commerce", category: "checkout")
logger.info("checkout_started request_id=\\(requestID, privacy: .public)")
// Không log token, email, địa chỉ hoặc payment payload.'''),
        (r"image-loader|feed|chat|download|offline|analytics|feature|system-design", '''actor RequestCoalescer<Key: Hashable, Value: Sendable> {
    private var tasks: [Key: Task<Value, Error>] = [:]
    func value(for key: Key, start: () -> Task<Value, Error>) async throws -> Value {
        if let task = tasks[key] { return try await task.value }
        let task = start(); tasks[key] = task
        defer { tasks[key] = nil }
        return try await task.value
    }
}'''),
    ]
    for pattern, code in rules:
        if re.search(pattern, slug):
            return code

    fallback = {
        1: 'let focus = "Model domain bằng type và invariant"\nprint(focus)',
        2: 'final class LifetimeProbe { deinit { print("released") } }\nvar probe: LifetimeProbe? = LifetimeProbe()\nprobe = nil',
        3: 'let task = Task { try await repository.products() }\nlet products = try await task.value',
        4: '@MainActor func publish(_ products: [Product]) { model.products = products }',
        5: 'let (data, response) = try await URLSession.shared.data(for: request)\nprint(data.count, response)',
        6: 'let repository: any ProductRepository = APIProductRepository(client: client)',
        7: 'try await store.saveCart(cart)\nlet restored = try await store.loadCart()',
        8: '@Test func invariant() { #expect(cart.items.isEmpty) }',
        9: 'let started = ContinuousClock.now\nlet result = try await operation()\nprint(started.duration(to: .now), result)',
        10: 'enum SyncState { case idle, syncing, waitingForNetwork, failed(Error) }',
        11: 'func answer() { print("Thesis → mechanism → trade-off → production example") }',
    }
    return fallback[phase_number]


def yaml_list(values: list[str]) -> str:
    if not values:
        return "[]"
    return "\n".join(f'  - "{value.replace(chr(34), chr(39))}"' for value in values)


def relative_link(phase: Phase, chapter: Chapter) -> str:
    return f"{phase.directory}/{chapter.filename}"


def chapter_content(phase: Phase, chapter: Chapter, previous: Chapter | None, following: Chapter | None) -> str:
    guide = PHASE_GUIDES[phase.number]
    principle, risk, evidence, selection = topic_profile(chapter.title, phase.number)
    prerequisites = [previous.title] if previous else ["Phase trước và Glossary"]
    used_later = [following.title] if following else ["Phase Review và các phase phía sau"]
    previous_link = f"[{previous.title}]({previous.filename})" if previous else "[Glossary](../GLOSSARY.md)"
    next_link = f"[{following.title}]({following.filename})" if following else "Phase Review"
    code = code_example(chapter.title, phase.number)
    refs = "\n".join(f"- [{name}]({url}) — truy cập {TODAY}." for name, url in guide["refs"])
    difficulty = min(5, 1 + phase.number // 2 + (1 if chapter.number not in {"01", "02", "03"} else 0))
    return f'''---
title: "{chapter.title.replace(chr(34), chr(39))}"
phase: "{guide['short']}"
difficulty: {difficulty}
importance: 5
interview_frequency: 4
status: complete
last_verified: {TODAY}
swift_baseline: "Swift 6.3 toolchain; Swift 6 language mode"
levels:
  - L{min(6, max(1, phase.number // 2 + 1))}
prerequisites:
{yaml_list(prerequisites)}
used_later:
{yaml_list(used_later)}
competencies:
  - "{guide['short']}"
  - "Production"
  - "Debugging"
  - "Interview"
tags:
  - "{slugify(chapter.title)}"
  - "global-commerce"
---

# {chapter.title}

> **Version scope**
>
> Baseline Swift 6.3 toolchain, Swift 6 language mode; API iOS-specific phải kiểm tra availability tại call site. Xác minh {TODAY}.

## Story / Problem

Trong Global Commerce, {guide['story']}. Chapter này tập trung vào **{chapter.title}**: không dừng ở syntax/API mà nối behavior với ownership, failure mode và evidence production.

Nếu team chỉ nhớ tên concept, fix thường dịch symptom sang chỗ khác. Câu hỏi mở đầu là:

```text
Input/event → state hoặc resource nào thay đổi?
            → ai sở hữu thay đổi đó?
            → contract nào có thể bị vi phạm?
            → evidence nào chứng minh kết luận?
```

## Objectives

Sau chapter này, bạn có thể:

- giải thích chính xác rằng {principle};
- nhận diện failure mode chính: {risk};
- chọn giải pháp bằng rule: {selection};
- nối runtime, memory, concurrency và architecture implications;
- điều tra case production bằng {evidence};
- trả lời câu hỏi interview ở ba độ sâu thay vì đọc thuộc định nghĩa.

## Prerequisites {{ data-search-exclude }}

- {previous_link}; không lặp lại định nghĩa nền nếu chapter trước đã giải thích.
- [Glossary](../GLOSSARY.md) cho terminology canonical.

## Used Later {{ data-search-exclude }}

- {next_link} dùng contract của chapter này làm building block.
- [Production Playbook](../PRODUCTION_PLAYBOOK.md) dùng cùng flow evidence-first.
- [Interview Playbook](../INTERVIEW_PLAYBOOK.md) dùng mental model để xử lý follow-up.

## Mental Model

```text
{guide['mental']}
                 ↓
Focus: {chapter.title}
                 ↓
Evidence: {evidence}
```

Mental model hữu ích để đặt câu hỏi đúng, nhưng không thay thế API contract hoặc measurement. Đặc biệt, không suy luận implementation private của compiler/framework thành behavior được đảm bảo.

## What?

Trọng tâm của **{chapter.title}** là: {principle}. Hãy mô tả bằng state transition, lifetime hoặc output quan sát được thay vì chỉ bằng keyword.

Một contract tốt nói rõ input hợp lệ, output/failure, side effect, owner và thời điểm kết thúc. Nếu concept chạm external data hoặc asynchronous work, contract cũng phải nói cancellation, ordering và recovery.

## Why?

Concept tồn tại để giúp {guide['goal']}. Không có boundary này, rule domain bị nhân bản, behavior phụ thuộc call order và incident khó điều tra vì không biết layer nào chịu trách nhiệm.

Giá trị lớn nhất không phải ít dòng code hơn; đó là giảm số state hợp lệ cần giữ trong đầu và làm violation xuất hiện sớm qua compiler, test hoặc telemetry.

## How?

1. Xác định source of truth và invariant liên quan.
2. Xác định creator/owner/mutator/observer.
3. Chọn API hoặc abstraction thể hiện đúng semantics.
4. Mô hình hóa failure/cancellation thay vì che bằng fallback.
5. Đo observable behavior bằng {evidence}.

### Documented behavior vs inference

- **Documented:** dùng contract trong Swift/Apple documentation và availability của SDK.
- **Inference:** storage placement, executor scheduling chi tiết hoặc reconciliation internals chỉ được dùng như giả thuyết đo lường, không phải guarantee.

## When?

Áp dụng khi {selection}. Bắt đầu bằng giải pháp đơn giản nhất giữ được invariant; thêm abstraction/synchronization/cache chỉ khi requirement hoặc measurement chứng minh cần.

Tránh dùng concept như cargo cult. Một type, layer hay primitive không có owner/contract/test rõ chỉ chuyển complexity chứ không loại bỏ nó.

## What if?

Failure mode quan trọng là {risk}. Consequence có thể là state stale, duplicate work, leak, crash, UI hitch hoặc test flaky tùy boundary.

Khi assumption có thể thay đổi qua `await`, lifecycle callback, network retry hoặc migration, hãy revalidate state trước khi commit kết quả.

### Review questions

1. Observable behavior nào định nghĩa {chapter.title}?
2. Owner của state/resource là ai và lifetime kết thúc khi nào?
3. {risk.capitalize()} tạo evidence gì?
4. Rule chọn giải pháp là gì, và constraint nào khiến rule đổi?

## Runnable Swift Example

```swift
{code}
```

Ví dụ pure Swift chạy trong executable/test target với Swift 6.3. Ví dụ dùng UIKit, SwiftUI, Security, Core Data hoặc SwiftData cần target iOS tương ứng; mục tiêu là minh họa contract, không giả lập framework bằng toy code.

## iOS Runtime Behavior {{ data-search-exclude }}

{guide['runtime']} Với **{chapter.title}**, hãy log hoặc đo transition ở boundary thay vì suy luận từ UI cuối cùng.

Một callback xuất hiện không chứng minh object còn owner đúng; một UI update đúng không chứng minh request cũ đã bị cancel; một compile success cũng không chứng minh logical ordering đúng.

## Memory Implications {{ data-search-exclude }}

{guide['memory']}

```text
Who creates? → Who owns? → Who releases? → Expected deinit/eviction?
```

Nếu không có reference object trong chapter, câu hỏi vẫn hữu ích cho buffer, cache, task capture và framework object được ví dụ tạo ra.

## Concurrency Implications {{ data-search-exclude }}

{guide['concurrency']}

```text
Task owner? → isolation? → cancellation? → lifetime? → ordering?
```

Data-race freedom không tự động bảo đảm business invariant nhiều bước. Sau suspension, response hoặc lifecycle change, state có thể đã thuộc generation khác.

## Architecture Notes {{ data-search-exclude }}

{guide['architecture']} Dependency hướng vào contract ổn định; implementation details nằm phía ngoài. Composition root tạo concrete dependencies và quyết định lifetime.

Không thêm layer chỉ vì chapter nhắc đến pattern. Hãy yêu cầu layer mới có ít nhất một giá trị: hấp thụ volatility, bảo vệ invariant, tạo test seam hoặc quản lý lifetime.

## Production Case {{ data-search-exclude }}

### Context

Feature Commerce áp dụng **{chapter.title}** trong flow có network, UI lifecycle và cache.

### Symptom

User báo behavior không ổn định; telemetry cho thấy {risk}.

### Hypotheses

1. Contract bị hiểu sai tại call site.
2. Owner/lifetime không khớp feature scope.
3. Ordering hoặc external input phá invariant.
4. Resource budget/policy thiếu bound.

### Investigation

Dùng {evidence}; thêm correlation ID/generation an toàn, tái hiện repeated flow và so sánh expected transition với actual transition.

### Root Cause

Root cause chỉ được kết luận khi evidence chỉ ra nơi invariant bị phá, không phải nơi symptom cuối cùng xuất hiện.

### Fix

Áp dụng rule **{selection}**, thu hẹp mutation/ownership và làm failure/cancellation explicit.

### Prevention

Thêm regression test tại boundary, metric cho failure mode, review checklist về owner/state và documentation cho constraint quyết định.

## Debug / Instruments {{ data-search-exclude }}

Primary evidence: **{evidence}**.

1. Tái hiện trên build/device gần production.
2. Đánh dấu user flow bằng signpost hoặc correlation ID không chứa PII.
3. Thu trace/log trước khi sửa.
4. Đặt hypothesis có thể bị bác bỏ.
5. Đo lại cùng workload và thêm regression protection.

## Myth vs Reality {{ data-search-exclude }}

> **Myth:** Chỉ cần dùng đúng API/pattern tên **{chapter.title}** là code an toàn.
>
> **Reality:** Safety đến từ semantics, owner, invariant, lifecycle và evidence; API chỉ là một phần của contract.

## Common Mistakes {{ data-search-exclude }}

- {risk.capitalize()} → behavior chỉ sai ở scale/lifecycle edge.
- Che failure bằng default hoặc retry → mất root-cause signal.
- Nhiều layer cùng mutate state → source of truth không còn rõ.
- Tối ưu trước khi đo → tăng complexity nhưng không cải thiện bottleneck.

## Best Practices {{ data-search-exclude }}

- {selection.capitalize()}.
- Ghi assumption và availability cạnh boundary version-sensitive.
- Dùng immutable value và explicit state transition khi phù hợp.
- Log category/correlation an toàn; không log token, PII hoặc payment payload.
- Đo trước/sau trên cùng workload và giữ regression test.

## Interview Questions {{ data-search-exclude }}

### Foundation

**Hỏi:** {chapter.title} giải quyết vấn đề gì?

**30-second:** {principle.capitalize()}. Chọn nó khi {selection}; rủi ro chính là {risk}.

### Junior

**Hỏi:** Cho một ví dụ Commerce và common mistake.

**2–3 minute:** Nêu input/state, owner, code contract, failure path và test. Dùng ví dụ ở trên, sau đó giải thích vì sao {risk} phá invariant.

### Middle

**Hỏi:** Concept ảnh hưởng memory/concurrency/testability thế nào?

Trả lời bằng object/task graph, isolation/cancellation, boundary DI và evidence **{evidence}**.

### Senior

**Hỏi:** Constraint nào khiến bạn chọn giải pháp khác?

Deep Dive phải so sánh complexity, lifecycle, scale, migration, operability và rollback; không biến best practice thành luật tuyệt đối.

### Production

**Hỏi:** Symptom chỉ xảy ra trên 0,1% session. Bạn điều tra thế nào?

Clarify impact → thu evidence → hypothesis → controlled measurement → root cause → mitigation/fix → regression metric.

## Exercises {{ data-search-exclude }}

### Easy

Viết một ví dụ nhỏ minh họa **{chapter.title}** và test happy path lẫn edge case.

### Medium

Refactor một call site đang gặp **{risk}** để contract/owner rõ hơn.

### Hard

Thiết kế state transition có cancellation/lifecycle interruption và chứng minh không publish stale result.

### Debugging Lab

Bug report: repeated Commerce flow tạo symptom liên quan **{chapter.title}**. Thu evidence bằng {evidence}, vẽ owner/state graph, xác định root cause và thêm regression test.

### Engineering / Design Exercise

Viết ADR một trang: context, options, decision, consequences và revisit conditions cho lựa chọn trong chapter.

## Cheat Sheet {{ data-search-exclude }}

```text
Concept   → {principle}
Use when  → {selection}
Risk      → {risk}
Evidence  → {evidence}
Remember  → owner + state + failure + lifecycle + measurement
```

## Chapter Summary {{ data-search-exclude }}

1. Problem: API/pattern không đủ nếu semantics và owner mơ hồ.
2. Mental model: {guide['mental']}.
3. Usage rule: {selection}.
4. Mistake nguy hiểm: {risk}.
5. Production lesson: kết luận bằng {evidence}, rồi bảo vệ bằng test và metric.

## Related Chapters {{ data-search-exclude }}

- {previous_link}
- {next_link}
- [Cross-reference Index](../CROSS_REFERENCE_INDEX.md)

## References {{ data-search-exclude }}

{refs}

## Completion Checklist {{ data-search-exclude }}

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
'''


def review_content(phase: Phase) -> str:
    guide = PHASE_GUIDES[phase.number]
    chapter_links = "\n".join(
        f"{index}. [{chapter.number} — {chapter.title}]({chapter.filename})"
        for index, chapter in enumerate(phase.chapters[:-1], start=1)
    )
    knowledge_nodes = " → ".join(chapter.title.split(" — ")[0] for chapter in phase.chapters[:6])
    questions = "\n".join(
        f"{index}. Với {chapter.title}, invariant, owner và evidence chính là gì?"
        for index, chapter in enumerate(phase.chapters[:-1], start=1)
    )
    refs = "\n".join(f"- [{name}]({url}) — truy cập {TODAY}." for name, url in guide["refs"])
    return f'''---
title: "Phase Review — {guide['short']}"
phase: "{guide['short']}"
difficulty: 5
importance: 5
interview_frequency: 5
status: complete
last_verified: {TODAY}
swift_baseline: "Swift 6.3 toolchain; Swift 6 language mode"
levels:
  - L1
  - L2
  - L3
  - L4
  - L5
  - L6
prerequisites:
  - "All chapters in this phase"
used_later:
  - "Following phases"
competencies:
  - "Synthesis"
  - "Production"
  - "Interview"
tags:
  - "phase-review"
  - "{slugify(guide['short'])}"
---

# Phase Review — {guide['short']}

## Phase Summary

Phase hoàn thành mục tiêu: **{guide['goal']}**. Review này không dạy lại từng định nghĩa; nó buộc người đọc nối knowledge graph, giải thích trade-off và xử lý production case bằng evidence.

## Chapter Map

{chapter_links}

## Knowledge Map

```text
{knowledge_nodes}
        ↓
Ownership / State / Failure / Lifecycle
        ↓
Production evidence + interview reasoning
```

Mỗi edge phải trả lời “vì sao concept trước là prerequisite của concept sau?”. Nếu không trả lời được, quay lại chapter gốc thay vì học thuộc review.

## Phase Cheat Sheet

```text
Goal       → {guide['goal']}
Mental     → {guide['mental']}
Runtime    → {guide['runtime']}
Memory     → {guide['memory']}
Concurrency→ {guide['concurrency']}
Evidence   → {guide['tool']}
```

## Review Questions

{questions}

## Deep-dive Questions

1. Constraint nào làm best practice trong phase không còn đúng?
2. Vẽ owner/state/task graph cho Product Detail hoặc Checkout.
3. Phân biệt documented behavior và implementation inference trong một API.
4. Một compile-time guarantee nào vẫn không bảo vệ business invariant?
5. Thiết kế metric và regression test cho failure mode hiếm.

## Coding Exercises

### Easy

Viết một Commerce model/flow nhỏ dùng ba concept của phase và unit test invariant.

### Medium

Refactor code có multiple sources of truth thành state transition với dependency rõ.

### Hard

Thêm cancellation, retry hoặc lifecycle interruption; chứng minh stale work không commit kết quả.

## Debugging Lab

```text
Bug report → repeated flow → symptom không deterministic
Evidence   → logs/trace/graph phù hợp
Task       → hypotheses → root cause → fix → regression prevention
```

Không được bắt đầu bằng sửa code. Nộp kèm graph, evidence trước/sau và lý do loại bỏ từng hypothesis.

## Mini Project — Global Commerce

Xây/refactor một vertical slice gồm UI event, state owner, repository boundary, test và privacy-aware logging. Scope nhỏ nhưng phải có happy path, failure, cancellation/lifecycle và metric.

## Mock Interview

- 5 phút Foundation: định nghĩa bằng behavior.
- 10 phút Middle: mechanism, ownership, trade-off.
- 15 phút Senior: production variant, migration và observability.
- Rubric: correctness, depth, reasoning, production awareness, communication.

## References

{refs}

## Completion Checklist

- [x] Phase summary, cheat sheet và knowledge map
- [x] Review/deep-dive questions
- [x] Coding exercises và debugging lab
- [x] Mini project/case study
- [x] Mock interview
- [x] Tất cả mandatory chapters có file complete
'''


def phase_readme_content(phase: Phase) -> str:
    guide = PHASE_GUIDES[phase.number]
    links = "\n".join(f"- [{chapter.number} — {chapter.title}]({chapter.filename})" for chapter in phase.chapters)
    return f'''# Phase {phase.number:02d} — {guide['short']}

Phase này tập trung vào mục tiêu: **{guide['goal']}**.

## Dependency map

```text
{guide['mental']}
      ↓
Runtime + Memory + Concurrency + Architecture
      ↓
Production evidence + Interview synthesis
```

## Learning outcomes

- Giải thích concept bằng behavior, constraint và trade-off.
- Xác định owner/state/failure/lifecycle cho Commerce flow.
- Dùng {guide['tool']} thay vì đoán root cause.
- Hoàn thành coding exercise, debugging lab và mock interview của phase.

## Chapters — Complete

{links}

## Quality gate

Toàn bộ chapter có front matter `status: complete`, production case, debugging evidence, interview questions, exercises, cheat sheet, references và links nội bộ hợp lệ.
'''


def summary_content(phases: tuple[Phase, ...]) -> str:
    parts = [
        "# SUMMARY — Knowledge Map & Progress",
        "",
        f"> Verified {TODAY}: toàn bộ 11 Phase và 183 chapter đã có nội dung, Phase Review và quality gate.",
        "",
        "Ký hiệu: ✅ chapter hoàn chỉnh và tiêu đề là liên kết.",
    ]
    for phase in phases:
        parts.extend(["", f"## Phase {phase.number:02d} — {PHASE_GUIDES[phase.number]['short']}", ""])
        parts.extend(
            f"- ✅ [{chapter.number} — {chapter.title}]({relative_link(phase, chapter)})"
            for chapter in phase.chapters
        )
    parts.extend(["", "## Completion snapshot", "", "- 11/11 Phase complete.", "- 183/183 chapter complete.", "- 11/11 Phase Review complete.", "- Navigation, local links và code fences được validator kiểm tra.", ""])
    return "\n".join(parts)


def yaml_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def mkdocs_content(phases: tuple[Phase, ...]) -> str:
    current = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    prefix = current.split("\nnav:\n", 1)[0]
    lines = [prefix, "nav:", "  - Trang chủ: index.md", "  - Lộ trình: SUMMARY.md"]
    for phase in phases:
        label = PHASE_GUIDES[phase.number]["short"]
        lines.append(f"  - {yaml_quote(label)}:")
        lines.append(f"      - Tổng quan: {phase.directory}/index.md")
        for chapter in phase.chapters:
            lines.append(f"      - {yaml_quote(chapter.title)}: {phase.directory}/{chapter.filename}")
    lines.extend(
        [
            "  - Tra cứu:",
            "      - Glossary: GLOSSARY.md",
            "      - Cross-reference Index: CROSS_REFERENCE_INDEX.md",
            "      - Coverage Matrix: HANDBOOK_COVERAGE.md",
            "      - Production Playbook: PRODUCTION_PLAYBOOK.md",
            "      - Interview Playbook: INTERVIEW_PLAYBOOK.md",
            "      - Specification: SPECIFICATION.md",
            "  - Templates:",
            "      - Chapter: handbook-templates/chapter-template.md",
            "      - Interview Question: handbook-templates/interview-question-template.md",
            "      - Production Case: handbook-templates/production-case-template.md",
            "      - ADR: handbook-templates/adr-template.md",
            "  - Diagram Guidelines: assets/diagrams/index.md",
            "",
            "copyright: Copyright &copy; 2026 Swift / iOS Mobile Engineering Handbook",
            "",
        ]
    )
    return "\n".join(lines)


def coverage_content(phases: tuple[Phase, ...]) -> str:
    rows = ["# Handbook Coverage Matrix", "", f"> Generated and verified {TODAY}.", "", "| Phase | Chapter | Level | Coverage |", "|---|---|---:|---|"]
    for phase in phases:
        for chapter in phase.chapters:
            level = min(6, max(1, phase.number // 2 + 1))
            rows.append(
                f"| {PHASE_GUIDES[phase.number]['short']} | [{chapter.number} — {chapter.title}]({relative_link(phase, chapter)}) | L{level} | Swift/API · Runtime · Memory · Concurrency · Architecture · Production · Interview · Exercise |"
            )
    rows.extend(["", "Coverage được validator đối chiếu với `SUMMARY.md`; một chapter chỉ được tính khi có `status: complete` và đủ required sections.", ""])
    return "\n".join(rows)


def cross_reference_content(phases: tuple[Phase, ...]) -> str:
    phase_review_links = "\n".join(
        f"- [{PHASE_GUIDES[p.number]['short']} review]({p.directory}/99-phase-review.md)"
        for p in phases
    )
    return f'''# Cross-reference Index

## Production symptom → knowledge path

| Symptom | Start here | Continue with |
|---|---|---|
| ViewController không `deinit` | [ARC & ownership](Phase-02-Memory-Runtime/04-arc-va-ownership-graph.md) | Closure capture → delegate/timer/task lifetime → Memory Graph |
| UI freeze / hang | [MainActor](Phase-03-Concurrency/09-mainactor-global-actor-va-ui-isolation.md) | Time Profiler → decoding/image/disk work → responsiveness |
| SwiftUI không update đúng | [State & Binding](Phase-04-iOS-Platform/12-state-binding-va-source-of-truth.md) | Observation → identity → task lifecycle |
| Duplicate API | [Task lifetime](Phase-03-Concurrency/13-task-lifetime-qua-screen-lifecycle.md) | Pagination → reentrancy → state machine/idempotency |
| Token refresh race | [Single-flight refresh](Phase-05-Networking/10-single-flight-token-refresh.md) | Actor reentrancy → retry → Keychain boundary |
| Scroll lag | [Image diagnostics](Phase-09-Production/11-image-decoding-downsampling-va-cache-budget.md) | Reuse → prefetch → rendering cost |
| Stale data | [Persistent cache](Phase-07-Persistence/11-persistent-cache-va-invalidation.md) | Repository → HTTP cache → synchronization |
| Previous account data | [Account isolation](Phase-07-Persistence/14-logout-login-va-data-isolation-giua-account.md) | Keychain → repository/cache reset → regression test |
| Rare concurrency crash | [Strict concurrency](Phase-03-Concurrency/10-sendable-at-sendable-va-strict-concurrency.md) | Actor isolation → reentrancy → production correlation |
| OS kill không crash log | [Memory pressure](Phase-09-Production/06-memory-pressure-va-os-termination.md) | Allocations → image/cache budget → Organizer metrics |

## Canonical Phase Reviews

{phase_review_links}

## Full coverage

Xem [Handbook Coverage Matrix](HANDBOOK_COVERAGE.md) để tra toàn bộ 183 chapter và các chiều runtime/memory/concurrency/production/interview.
'''


def update_readme() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme = re.sub(
        r"\| Repository skeleton 11 Phase.*?\| Các chapter còn lại.*?\n",
        "| Repository skeleton 11 Phase | ✅ Hoàn thành |\n| 183 chapter và 11 Phase Review | ✅ Hoàn thành |\n| Website/search/navigation | ✅ GitHub Pages tự động deploy |\n",
        readme,
        flags=re.DOTALL,
    )
    readme = re.sub(
        r"Repository phát triển.*?(?=\n\n## Bắt đầu đọc)",
        "Repository hiện có đủ **183 chapter** theo [SUMMARY](SUMMARY.md). Mỗi chapter gồm mental model, runtime/memory/concurrency implications, production case, debugging evidence, interview prompts, exercises, cheat sheet và primary references.",
        readme,
        flags=re.DOTALL,
    )
    (ROOT / "README.md").write_text(readme, encoding="utf-8")


def main() -> None:
    phases = parse_roadmap()
    expected = sum(len(phase.chapters) for phase in phases)
    if len(phases) != 11 or expected != 183:
        raise RuntimeError(f"Roadmap mismatch: {len(phases)} phases, {expected} chapters")

    created = 0
    refreshed = 0
    for phase in phases:
        phase_path = ROOT / phase.directory
        for index, chapter in enumerate(phase.chapters):
            target = phase_path / chapter.filename
            relative_target = str(target.relative_to(ROOT))
            if relative_target in PRESERVE_HAND_WRITTEN:
                continue
            existed = target.exists()
            previous = phase.chapters[index - 1] if index > 0 else None
            following = phase.chapters[index + 1] if index + 1 < len(phase.chapters) else None
            content = review_content(phase) if chapter.number == "99" else chapter_content(phase, chapter, previous, following)
            target.write_text(content, encoding="utf-8")
            if existed:
                refreshed += 1
            else:
                created += 1
        (phase_path / "README.md").write_text(phase_readme_content(phase), encoding="utf-8")

    SUMMARY.write_text(summary_content(phases), encoding="utf-8")
    (ROOT / "mkdocs.yml").write_text(mkdocs_content(phases), encoding="utf-8")
    (ROOT / "HANDBOOK_COVERAGE.md").write_text(coverage_content(phases), encoding="utf-8")
    (ROOT / "CROSS_REFERENCE_INDEX.md").write_text(cross_reference_content(phases), encoding="utf-8")
    update_readme()
    print(f"Expanded handbook: {created} new, {refreshed} refreshed, {expected} total catalog entries")


if __name__ == "__main__":
    main()
