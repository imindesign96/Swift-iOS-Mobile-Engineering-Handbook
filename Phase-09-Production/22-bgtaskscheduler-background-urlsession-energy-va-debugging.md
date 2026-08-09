---
title: "BackgroundTasks và background URLSession: scheduling, expiration, energy và debugging"
phase: "Production"
difficulty: 5
importance: 5
interview_frequency: 5
status: complete
last_verified: 2026-08-09
swift_baseline: "Swift 6.3 toolchain; Swift 6 language mode"
levels:
  - L5
prerequisites:
  - "Background execution và interrupted work"
  - "Cancellation từ screen đến URLSession"
used_later:
  - "Production scenario interview"
competencies:
  - "Production"
  - "Concurrency"
  - "Networking"
  - "Performance"
tags:
  - "bgtaskscheduler"
  - "background-urlsession"
  - "expiration"
  - "energy-budget"
---

# BackgroundTasks và background URLSession: scheduling, expiration, energy và debugging

> **Version scope**
>
> Bao phủ `BGAppRefreshTask`, `BGProcessingTask`, background `URLSession` và finite-length background task. OS scheduling là policy động; `earliestBeginDate` không phải deadline. API background mới phải availability-gate theo SDK/OS. Xác minh 2026-08-09.

## Story / Problem

App đặt `earliestBeginDate` là 02:00 và kỳ vọng job chạy đúng giờ. Job không chạy, nên team thêm silent push mỗi phút. Khi job chạy, một detached task tiếp tục sau expiration và ghi database nửa chừng. Video upload dùng foreground session nên dừng lúc app suspended. Sai lầm chung là coi background runtime như server cron thay vì **cơ hội do hệ thống cấp, có deadline và resource policy**.

```text
Durable work intent → choose system mechanism → system grants opportunity
                                              ↓
                              bounded work + checkpoint + completion
```

## Objectives

Sau chapter này, bạn có thể:

- chọn đúng mechanism cho refresh, processing, transfer và foreground completion;
- register/schedule `BGTaskScheduler` đúng lifecycle;
- viết expiration-safe handler có cancellation, checkpoint và exactly-once completion;
- dùng background URLSession cho transfer hệ thống sở hữu;
- thiết kế idempotency, resume, account generation và protected-data constraints;
- debug trên device bằng logs/metrics thay vì chờ lịch thật.

## Prerequisites

- [Background execution và interrupted work](16-background-execution-va-interrupted-work.md).
- [Cancellation từ screen đến URLSession](../Phase-05-Networking/08-cancellation-tu-screen-en-urlsession.md).
- [Battery và energy diagnostics](13-battery-va-energy-diagnostics.md).

## Used Later

- [Production scenario interview](../Phase-11-Interview/11-production-scenario-interview.md).
- [Download Manager](../Phase-10-Mobile-System-Design/05-download-manager-ho-tro-resume-background.md).

## Mental Model

```text
beginBackgroundTask     → grace để kết thúc work foreground đang làm
BGAppRefreshTask        → refresh ngắn, system-scheduled
BGProcessingTask        → maintenance nặng hơn, condition-aware
background URLSession   → system sở hữu network transfer qua suspension/relaunch
silent push             → best-effort invalidation signal
```

Không mechanism nào bảo đảm chạy đúng thời điểm tùy ý. Requirement có deadline cứng phải được server/user-visible design xử lý, không “ép” iOS scheduler.

## What?

App khai báo permitted task identifiers/configuration, register handler sớm và submit request. `earliestBeginDate` chỉ nói không chạy trước thời điểm đó. Khi system launch task, handler thường schedule request tiếp theo, tạo scoped async work, gắn expiration handler để cancel, rồi gọi `setTaskCompleted(success:)` đúng một lần.

Background URLSession phù hợp upload/download lớn cần tiếp tục khi app suspended/terminated bởi system. Session có stable unique identifier và delegate; download hoàn tất đưa temporary file URL phải được move trước callback kết thúc. Nếu user force-quit, behavior/relaunch khác system termination—không hứa điều framework không guarantee.

## Why?

Scheduler xét usage pattern, pin, power, thermal, network và system budget. Job tốn pin/thất bại làm giảm cơ hội tương lai. Expiration có thể đến giữa transaction/network; nếu không checkpoint, retry tạo duplicate. Task completion gọi sớm làm OS nghĩ work xong; gọi thiếu làm ảnh hưởng scheduling/budget. Background session delegate có thể tới sau process relaunch, nên screen/ViewModel không thể là owner.

## How?

```swift
import BackgroundTasks

final class BackgroundCoordinator {
    static let refreshID = "com.example.commerce.refresh"
    private var running: Task<Void, Never>?

    func register() {
        BGTaskScheduler.shared.register(
            forTaskWithIdentifier: Self.refreshID,
            using: nil
        ) { [weak self] task in
            guard let refresh = task as? BGAppRefreshTask else {
                task.setTaskCompleted(success: false)
                return
            }
            self?.handle(refresh)
        }
    }

    func schedule() throws {
        let request = BGAppRefreshTaskRequest(identifier: Self.refreshID)
        request.earliestBeginDate = Date(timeIntervalSinceNow: 30 * 60)
        try BGTaskScheduler.shared.submit(request)
    }

    private func handle(_ task: BGAppRefreshTask) {
        try? schedule()
        let work = Task {
            let success = await RefreshUseCase.shared.runBounded()
            guard !Task.isCancelled else { return }
            task.setTaskCompleted(success: success)
        }
        running = work
        task.expirationHandler = { work.cancel() }
    }
}
```

Production code dùng completion gate để bảo đảm expiration và success race không gọi `setTaskCompleted` hai lần. Cancellation phải truyền xuống URLSession/database loop; handler ghi checkpoint/outbox trước khi kết thúc. Register trước khi application launch path hoàn tất theo framework requirement, không đợi screen xuất hiện.

### Choosing and scheduling

Refresh dùng cho fetch nhỏ giúp UI mới hơn; processing cho index/cleanup/model work có thể cần network/external power. Đặt constraints thật sự cần, vì constraint rộng hơn tăng cơ hội schedule. Coalesce nhiều feature vào một maintenance plan ưu tiên theo budget thay vì mỗi module spam request. Kiểm tra pending requests và handle submit errors; scheduling lại có policy tránh duplicate.

### Background URLSession

```swift
let configuration = URLSessionConfiguration.background(
    withIdentifier: "com.example.commerce.media-upload"
)
configuration.isDiscretionary = false
configuration.sessionSendsLaunchEvents = true
```

Tạo upload từ file khi background configuration yêu cầu; persist mapping task identifier ↔ domain upload ID/account generation. Delegate owner sống ở app composition root và reconstruct state sau relaunch. Xử lý progress, response/status, retry-after, checksum và atomic move. Khi system báo background events hoàn tất, gọi saved app completion handler sau khi delegate events đã drain.

### Expiration-safe architecture

Work unit nhỏ, idempotent và checkpointed. Mỗi commit mang operation ID/generation. Expiration cancel work, lưu remaining cursor nếu safe và hoàn thành task. Không mở transaction dài xuyên network. Nếu protected data unavailable khi device locked, defer hoặc chỉ dùng data accessible theo explicit security policy—đừng hạ file protection chỉ để job chạy.

### Energy và debugging

Đo runtime, bytes, wakeups, retry, completion/expiration và usefulness (bao nhiêu refresh thực sự được user thấy). Batch network/disk, tránh polling, dừng khi không còn account/feature. Dùng Xcode debugger/device logs và framework-supported simulate launch/expiration workflow; kiểm tra identifier/config/capability trước khi kết luận scheduler “bug”. Test release configuration trên physical device.

## Production Case

### Context

App upload video bằng chứng và refresh order list.

### Symptom

Upload restart từ đầu sau relaunch; refresh đôi khi đánh dấu success dù database chưa cập nhật.

### Investigation

Logs theo background session ID/task ID/operation ID cho thấy mapping chỉ nằm trong ViewModel. Refresh gọi completion ngay sau start detached task, không đợi commit.

### Root Cause

Owner gắn screen lifecycle và completion semantics sai.

### Fix

Persist transfer mapping/outbox ở repository, delegate tại app root, upload từ file; refresh await bounded use case và dùng completion gate sau durable commit.

### Prevention

Kill/relaunch tests, expiration ở từng checkpoint, duplicate callback, logout/account switch, disk full, 401 refresh, network change và energy dashboard.

## Interview Questions

### Foundation

**`earliestBeginDate` có phải lịch chạy không?** Không; chỉ là thời điểm sớm nhất, system quyết định cơ hội thực tế.

### Middle

**Khi nào dùng background URLSession?** Transfer lớn/cần system tiếp tục qua suspension/relaunch; không dùng BGTask để giữ process sống trong cả upload.

### Senior

**Thiết kế background work reliable?** Durable intent, đúng mechanism, idempotent/checkpointed units, cancellation/expiration, app-lifetime owner, account isolation, protected data, telemetry và user-visible recovery.

## Exercises

### Easy

Map năm workload sang finite task, refresh, processing, background transfer hoặc server push.

### Medium

Viết completion gate chống race success/expiration.

### Hard

Thiết kế media upload manager survive suspension, relaunch, retry, logout và duplicate callback.

### Debugging Lab

Simulate launch rồi expiration giữa database commit; chứng minh checkpoint nhất quán và task completion đúng một lần.

## Cheat Sheet

```text
schedule          → request opportunity, không cron guarantee
register          → early app lifecycle
handler           → reschedule + scoped work + expiration + complete once
work              → bounded + idempotent + checkpointed
URLSession(bg)    → system-owned transfer + persistent mapping + delegate root
force quit        → không hứa auto relaunch
energy            → batch, no polling, measure usefulness
debug             → device + release config + simulated launch/expiration
```

## Chapter Summary

1. Chọn background mechanism theo loại work, không theo mong muốn “chạy lâu”.
2. BGTaskScheduler cấp cơ hội, không bảo đảm lịch chính xác.
3. Expiration/cancellation và completion phải là contract đúng một lần.
4. Background URLSession cần persistent identity và app-lifetime delegate.
5. Reliability đến từ durable intent, idempotency, checkpoint và evidence.

## Related Chapters

- [Background execution](16-background-execution-va-interrupted-work.md)
- [Download Manager](../Phase-10-Mobile-System-Design/05-download-manager-ho-tro-resume-background.md)
- [APNs end-to-end](../Phase-04-iOS-Platform/27-apns-push-notification-end-to-end.md)

## References

- [Apple — Background Tasks](https://developer.apple.com/documentation/backgroundtasks)
- [Apple — Choosing Background Strategies for Your App](https://developer.apple.com/documentation/backgroundtasks/choosing-background-strategies-for-your-app)
- [Apple — Using background tasks to update your app](https://developer.apple.com/documentation/backgroundtasks/using-background-tasks-to-update-your-app)
- [Apple — Downloading files in the background](https://developer.apple.com/documentation/foundation/downloading-files-in-the-background)
