# Production Case — <Symptom, not root cause>

## Context

- App/build/OS/device/network/cohort:
- Feature and expected behavior:
- Impact and severity:
- Recent changes:

## Bug Report

Mô tả symptom quan sát được, không lộ root cause.

## Available Evidence

- Crash/hang report:
- Structured logs/correlation IDs:
- Metrics/traces:
- Reproduction details:
- Evidence chưa có:

## Timeline

```text
Event → state/work → suspension/lifecycle → next event → symptom
```

## Hypotheses

| Rank | Hypothesis | Evidence ủng hộ | Evidence có thể bác bỏ |
|---|---|---|---|
| 1 | | | |

## Investigation

### Tool / experiment

- Vì sao chọn:
- Quan sát gì:
- Kết quả:
- Hypothesis nào bị loại/được tăng độ tin cậy:

## Root Cause

Tách:

- triggering condition;
- technical root cause;
- contributing factors;
- vì sao test/monitor cũ không bắt được.

## Mitigation

Giảm user impact và cách bảo toàn evidence.

## Fix

Code/design/config change và trade-off.

## Verification

- reproduction cũ;
- metric trước/sau cùng điều kiện;
- cohort/build rollout;
- adverse effects đã kiểm tra.

## Prevention

- regression test;
- invariant/guard;
- log/metric/alert;
- process/design change;
- owner và revisit condition.

## Privacy & Security Review

Xác nhận evidence và telemetry không chứa sensitive data.

## Interview Mode

Nếu dùng làm bài phỏng vấn, chia evidence thành từng round và không lộ Root Cause trước khi candidate đặt câu hỏi/đề xuất phép đo.

