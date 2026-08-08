# Production Playbook

Playbook này là điểm vào theo incident. Chapter chuyên sâu sẽ bổ sung kỹ thuật và case; quy trình dưới đây dùng được ngay.

## 1. Nguyên tắc điều tra

```text
Symptom
  ↓
Scope + severity
  ↓
Collect evidence
  ↓
Rank hypotheses
  ↓
Measure / reproduce / falsify
  ↓
Root cause
  ↓
Mitigate → fix → verify → prevent
```

Không sửa chỉ vì một giả thuyết “nghe hợp lý”. Ghi rõ evidence nào sẽ bác bỏ từng giả thuyết.

## 2. Incident intake

Thu thập tối thiểu:

- version/build, OS, device class, locale và network type;
- thời điểm, feature/screen, user action ngay trước symptom;
- tần suất, cohort, rollout/flag liên quan;
- crash/hang/memory/network evidence có correlation ID;
- thay đổi gần nhất có thể ảnh hưởng;
- mức độ dữ liệu, payment, security hoặc privacy bị tác động.

> **Warning**
>
> Không đưa token, password, full request body, PII hoặc payment data vào log/ticket.

## 3. Triage theo severity

| Mức | Ví dụ | Hành động đầu |
|---|---|---|
| Critical | payment duplicate, data loss, security exposure, crash diện rộng | giảm impact: kill switch/rollback/disable path nếu an toàn |
| High | flow chính không dùng được, hang hoặc crash cohort lớn | khoanh cohort, giữ evidence, chuẩn bị hotfix |
| Medium | degradation có workaround | đo tần suất và ưu tiên fix có regression test |
| Low | cosmetic/rare không mất chức năng | theo dõi trend, gom vào normal release |

Mitigation có thể đi trước root cause hoàn hảo khi user impact nghiêm trọng, nhưng phải bảo toàn evidence.

## 4. Crash / exception

Checklist:

1. Xác nhận report đã symbolicate đúng build và dSYM.
2. Xác định exception/termination reason và faulting thread.
3. Tìm app frames đầu tiên; đọc cả call stack, không chỉ dòng top.
4. So sánh cohort theo OS/device/build/feature flag.
5. Nối với breadcrumbs/state transition an toàn.
6. Tạo reproduction nhỏ nhất hoặc test kích hoạt invariant.

Common families:

- `fatalError`, force unwrap, index out of range: kiểm tra invariant và input/order;
- `EXC_BAD_ACCESS`: lifetime, unsafe access, bridging, data race;
- watchdog/hang: main-thread stall, deadlock, synchronous I/O;
- concurrency runtime failure: isolation/Sendable assumption và migration boundary.

## 5. Memory

Phân biệt trước:

```text
Leak: object đáng lẽ chết nhưng còn ownership path
Pressure: object hợp lệ nhưng tổng footprint vượt budget
```

### Leak path

- đặt `deinit` probe có chủ đích;
- lặp flow open/close để xem instance count;
- dùng Memory Graph tìm path từ root tới object;
- kiểm tra closure, delegate, observer, timer, task, coordinator và cache;
- sửa ownership edge, lặp lại experiment và thêm regression guard.

### Pressure path

- xem allocation category và lifetime;
- kiểm tra decoded image size, cache bound, large response, duplicate buffer;
- đo peak và steady-state trên thiết bị RAM thấp;
- giảm/stream/downsample/evict theo budget, không chỉ “xóa cache khi warning”.

## 6. UI freeze / scrolling hitch

1. Ghi lại exact interaction và duration.
2. Profile trên build/device gần production.
3. Tìm main-thread call tree/hang stack.
4. Phân loại: decode, disk I/O, JSON, layout, formatting, lock, state churn.
5. Dời hoặc chia nhỏ work chỉ sau khi biết cost; bảo vệ state/isolation khi đổi concurrency.
6. Đo lại cùng scenario và đặt performance regression threshold phù hợp.

## 7. Network failure

Phân loại trước retry:

| Lớp lỗi | Ví dụ | Hướng xử lý |
|---|---|---|
| Transport | offline, DNS, TLS, timeout | connectivity evidence, timeout/cancel, retry có policy |
| HTTP | 401, 404, 429, 5xx | contract theo status/header |
| Decode | schema/type/missing field | payload version an toàn, tolerant model khi hợp lý |
| Business | out of stock, payment declined | domain state và UX, thường không retry mù |

Retry checklist: retryable? max attempts? exponential backoff? jitter? cancellation? idempotent? server hint (`Retry-After`)?

## 8. Duplicate action / logical race

Timeline cần dựng:

```text
User event → state before → Task/request ID → suspension
→ interleaving event → response → state after → side effect
```

Bảo vệ theo nhiều lớp khi side effect quan trọng:

- UI feedback/disable action;
- client state machine chỉ cho transition hợp lệ;
- coalesce cùng in-flight operation;
- idempotency key;
- server-side uniqueness/transaction.

Actor có thể loại data race nhưng vẫn cho logical race qua `await`; kiểm tra lại invariant sau suspension.

## 9. Stale/offline data

Luôn trả lời:

- source of truth là server hay local store?
- freshness được định nghĩa bằng TTL, version hay event?
- stale data có được phép hiển thị không?
- write offline xếp hàng và retry ra sao?
- conflict phát hiện/resolve thế nào?
- dữ liệu có partition theo account không?

## 10. Background/lifecycle failure

- work có API background phù hợp hay chỉ là Task sống trong process?
- trạng thái cần resume đã persist chưa?
- app bị suspend/terminate tại mọi transition thì sao?
- callback/delegate có được reconnect sau relaunch không?
- user cancel/logout có hủy và cleanup work không?

## 11. Fix verification & prevention

Definition of fixed:

- reproduction cũ không còn;
- metric/evidence cải thiện trong cùng điều kiện;
- không phá cancellation, lifecycle, privacy hoặc performance khác;
- có regression test/monitor/alert hoặc guard phù hợp;
- incident note ghi root cause, contributing factors và revisit condition.

## 12. Production case record

Dùng [production case template](templates/production-case-template.md) để lưu evidence và reasoning nhất quán.

