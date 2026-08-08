---
title: "<Problem-oriented title>"
phase: "<Phase name>"
difficulty: 1
importance: 1
interview_frequency: 1
status: draft
last_verified: YYYY-MM-DD
swift_baseline: "Swift 6 language mode"
levels:
  - L1
prerequisites: []
used_later: []
competencies: []
tags: []
---

# <Problem-oriented title>

> **Version scope**
>
> Nêu compiler/toolchain, language mode, iOS availability hoặc “version-independent” và ngày xác minh.

## Story / Problem

Mở bằng một tình huống khiến concept trở nên cần thiết. Không bắt đầu bằng định nghĩa nếu có thể dùng problem.

## Objectives

Sau chapter này, người đọc có thể:

- giải thích ...;
- phân biệt ...;
- triển khai ...;
- điều tra ... bằng evidence ...

## Prerequisites

- Link tới chapter đã hoàn chỉnh hoặc glossary; không dạy lại.

## Used Later

- Concept/feature sẽ tái xuất hiện và vai trò của nó.

## Mental Model

```text
Input / event → ownership/state/runtime step → observable result
```

Nêu rõ mental model hữu ích ở đâu và giới hạn của nó.

## What?

Định nghĩa chính xác bằng behavior có thể quan sát.

## Why?

Problem ngôn ngữ/framework giải quyết; cost nếu thiếu abstraction này.

## How?

Compiler/runtime/framework làm gì. Phân biệt documented behavior với implementation inference.

## When?

Khi nên dùng, tránh dùng và constraint quyết định.

## What if?

Failure mode khi assumption bị vi phạm.

### Review questions

1. ...?
2. ...?

## Runnable Swift Example

```swift
// Complete minimal example, prefer Global Commerce domain.
```

Ghi cách chạy và expected output. Nếu cần iOS/framework version, nêu rõ.

## iOS Runtime Behavior

Mô tả lifecycle/call order/ownership mà framework chapter cần.

## Memory Implications

Trả lời khi phù hợp:

```text
Who creates? → Who owns? → Who releases? → Expected deinit?
```

## Concurrency Implications

Trả lời khi phù hợp:

```text
Task owner? → isolation? → cancellation? → lifetime? → ordering?
```

## Architecture Notes

Dependency direction, boundary và testability; không ép thêm layer nếu complexity chưa cần.

## Production Case

### Context

### Symptom

### Hypotheses

### Investigation

### Root Cause

### Fix

### Prevention

## Debug / Instruments

Nêu tool, thao tác quan sát và evidence mong đợi. Không chỉ liệt kê tên tool.

## Historical Note

Chỉ giữ section này nếu lịch sử giúp hiểu current design; nếu không, xóa.

## Myth vs Reality

> **Myth:** ...
>
> **Reality:** ...

Chỉ giữ khi misconception phổ biến.

## Common Mistakes

- Symptom → vì sao sai → consequence.

## Best Practices

- Guidance gắn với context/assumption, tránh absolute law.

## Interview Questions

### Foundation

### Junior

### Middle

### Senior

### Production

Với câu quan trọng, dùng ba tầng: 30-second, 2–3 minute, Deep Dive.

## Exercises

### Easy

### Medium

### Hard

### Debugging Lab

### Engineering / Design Exercise

## Cheat Sheet

```text
Concept → observable behavior → selection rule → primary risk
```

## Chapter Summary

1. Problem động lực là gì?
2. Mental model trung tâm là gì?
3. Usage rule quan trọng nhất?
4. Mistake nguy hiểm nhất?
5. Production lesson phải nhớ?

## Related Chapters

- Chỉ link file tồn tại; planned chapter có thể ghi text không link.

## References

- Primary documentation, proposal, WWDC hoặc source. Kèm ngày truy cập nếu version-sensitive.

## Completion Checklist

- [ ] Objectives có thể kiểm chứng
- [ ] Mental model và giới hạn được nói rõ
- [ ] What/Why/How/When/What-if đầy đủ
- [ ] Code chạy được hoặc availability rõ
- [ ] Runtime/memory/concurrency implications đúng phạm vi
- [ ] Production case dựa trên evidence
- [ ] Review + interview + exercises + cheat sheet
- [ ] Internal links tồn tại
- [ ] Claim version-sensitive có primary source và ngày verify
- [ ] Không còn placeholder; chuyển front matter thành `status: complete`

