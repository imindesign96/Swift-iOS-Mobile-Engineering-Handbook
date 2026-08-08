# Interview Playbook

Mục tiêu là trình bày mental model và trade-off, không học thuộc câu khẩu hiệu.

## 1. Cách xây câu trả lời

### 30 giây

```text
Definition chính xác → khác biệt cốt lõi → rule theo context → một risk
```

Ví dụ với “Struct vs Class”: nói value/reference semantics và identity trước, sau đó mới đến syntax/inheritance/ARC.

### 2–3 phút

```text
Mental model
→ Example trong Global Commerce
→ trade-off memory/concurrency/API design
→ common mistake
```

### Deep Dive

Mở rộng theo follow-up thật: CoW, ARC, existential, actor isolation, lifecycle, Instruments hoặc production failure. Không đổ tất cả knowledge vào câu trả lời đầu.

## 2. Khung trả lời technical question

1. Làm rõ ngữ cảnh/version nếu behavior phụ thuộc platform.
2. Định nghĩa bằng behavior quan sát được, không chỉ bằng syntax.
3. Giải thích vì sao feature tồn tại.
4. Nêu một example nhỏ.
5. Chọn/không chọn dựa trên constraint.
6. Nêu failure mode và cách kiểm chứng.

## 3. Khung production scenario

Interviewer thường đánh giá quá trình điều tra hơn là đoán đúng root cause đầu tiên.

```text
Clarifying questions
  ↓
Scope + timeline + recent changes
  ↓
Ranked hypotheses
  ↓
Evidence/tool cho từng hypothesis
  ↓
Fix + rollout + regression prevention
```

Câu hỏi mở đầu tốt:

- chỉ build production hay cả debug?
- xảy ra trên OS/device/network/cohort nào?
- symptom là crash, hang, kill hay UI không phản hồi?
- metric thay đổi từ release nào?
- có log/stack/memory graph/request timeline gì?

## 4. Khung Mobile System Design

```text
Functional + non-functional requirements
→ mobile constraints
→ user/data flow
→ source of truth + state ownership
→ architecture/network/persistence/concurrency
→ cache/offline/failure/security/performance
→ observability/testing
→ trade-offs + evolution
```

Đừng vẽ layer trước khi biết requirements. Với mọi flow, hỏi app bị background/terminate, network chập chờn, disk đầy, low-memory và request lặp thì chuyện gì xảy ra.

## 5. Coding interview

### Trước khi code

- restate input/output và constraint;
- hỏi edge cases;
- đưa brute force rồi cải thiện;
- chọn Swift type phù hợp (`Array`, `Set`, `Dictionary`, `Deque` abstraction nếu cần);
- nói rõ complexity.

### Khi code Swift

- không giả định `String` index là integer;
- tránh force unwrap không có invariant;
- đặt tên phản ánh domain;
- test empty, one element, duplicate, Unicode/overflow khi liên quan;
- với concurrent code, nói rõ ownership/isolation/cancellation.

### Sau khi code

- dry-run một case thường và một edge case;
- nêu time/space complexity;
- chỉ ra production changes: observability, retry/idempotency, persistence, limits, testability.

## 6. Thang độ sâu

| Level | Tín hiệu kỳ vọng |
|---|---|
| L1 Foundation | behavior cơ bản đúng, example đơn giản |
| L2 Junior | biết chọn API/type và common pitfalls |
| L3 Strong Junior | nối memory/testing/lifecycle |
| L4 Middle | reasoning về concurrency, architecture, production |
| L5 Strong Middle | trade-off đa chiều và migration |
| L6 Senior | constraint, failure mode, observability, team/system evolution |

YOE không tự động quyết định level.

## 7. Self-assessment rubric

Chấm mỗi chiều 0–4:

| Chiều | 0 | 2 | 4 |
|---|---|---|---|
| Correctness | sai bản chất | đúng phần chính | chính xác cả edge/version |
| Depth | khẩu hiệu | có mental model/example | nối runtime + trade-off |
| Reasoning | đoán | có giả thuyết | evidence-driven, biết falsify |
| Production | không xét | nêu một risk | lifecycle/observability/prevention |
| Communication | rời rạc | cấu trúc hiểu được | concise trước, deep dive đúng lúc |

Tổng điểm không thay thế feedback định tính; dùng rubric để thấy dimension cần luyện.

## 8. Một buổi mock interview 60 phút

- 5 phút: intro và scope;
- 10 phút: Swift Core/Memory;
- 10 phút: Concurrency/UI;
- 10 phút: Networking/Architecture/Testing;
- 15 phút: production scenario hoặc coding;
- 10 phút: system design/behavioral + feedback.

Ghi lại câu trả lời bằng [interview question template](templates/interview-question-template.md), rồi viết lại bản 30 giây và 2–3 phút sau buổi mock.

