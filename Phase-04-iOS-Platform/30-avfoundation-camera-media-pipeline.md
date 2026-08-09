---
title: "AVFoundation: camera, audio/video và media pipeline"
phase: "iOS Platform"
difficulty: 5
importance: 4
interview_frequency: 3
status: complete
last_verified: 2026-08-09
swift_baseline: "Swift 6.3 toolchain; Swift 6 language mode"
levels:
  - L4
  - L5
prerequisites:
  - "Thread, shared mutable state và data race"
  - "Memory pressure và OS termination"
used_later:
  - "Video Feed và resource budgeting"
competencies:
  - "iOS Platform"
  - "Concurrency"
  - "Performance"
  - "Production"
tags:
  - "avfoundation"
  - "camera"
  - "audio-video"
  - "media-pipeline"
---

# AVFoundation: camera, audio/video và media pipeline

> **Version scope**
>
> Tập trung contract ổn định của capture/playback/export. Camera format, codec, HDR, rotation API và hardware support khác theo device/SDK; query capability và test trên thiết bị thật. Xác minh 2026-08-09.

## Story / Problem

Màn scan sản phẩm chạy tốt trên Simulator nhưng giật trên iPhone cũ, xoay preview sai, memory tăng dần và cuộc gọi đến làm audio session hỏng. Team đang xem camera như một `UIView`, trong khi AVFoundation là pipeline thời gian thực gồm hardware, session graph, buffer, queue, orientation, audio policy và interruption.

```text
Device input → capture session/connection → output buffers/files
                       ↓                         ↓
                 preview layer          processing/export/upload
```

Mỗi frame có deadline. Giữ buffer quá lâu hoặc xử lý trên main thread tạo backpressure, dropped frames và thermal cost.

## Objectives

Sau chapter này, bạn có thể:

- cấu hình capture session theo input/output/connection và capability;
- quản lý permission, session queue, start/stop và interruption lifecycle;
- chọn photo, file, sample-buffer hoặc asset pipeline theo requirement;
- kiểm soát orientation, mirroring, audio session và app backgrounding;
- giảm memory/CPU bằng pixel format, downsampling, frame dropping và bounded processing;
- điều tra dropped frames, black preview, export failure và device-only bug.

## Prerequisites

- [Thread và data race](../Phase-03-Concurrency/01-thread-shared-mutable-state-va-data-race.md).
- [Image decoding và cache budget](../Phase-09-Production/11-image-decoding-downsampling-va-cache-budget.md).
- [Memory pressure](../Phase-09-Production/06-memory-pressure-va-os-termination.md).

## Used Later

- [Video Feed và resource budgeting](../Phase-10-Mobile-System-Design/07-video-feed-va-resource-budgeting.md).
- [Battery và energy diagnostics](../Phase-09-Production/13-battery-va-energy-diagnostics.md).

## Mental Model

```text
Session graph mutation → serialized configuration boundary
Frame delivery         → high-frequency producer
Processing/upload      → bounded consumer with cancellation/backpressure
Preview                → display path, không phải captured file authority
```

`AVCaptureSession` điều phối exclusive access và data flow. Input đại diện device/media source; output quyết định photo, movie file hoặc sample buffer; connection mang orientation/mirroring/stabilization. Preview có thể đúng trong khi output sai nếu chỉ cấu hình một connection.

## What?

Capture flow: xin permission đúng value moment, chọn device/format, `beginConfiguration`, add input/output sau `canAdd`, configure connections, `commitConfiguration`, rồi start session ngoài main thread. Session state được serialize trên một queue/actor boundary; UI state quay về MainActor.

Playback thường dùng `AVPlayer`/`AVPlayerItem`; editing/export dùng `AVAsset`, tracks, reader/writer hoặc export session tùy độ kiểm soát. Photo picker nên được ưu tiên nếu requirement chỉ cần user chọn media—không xin camera/photo-library quyền rộng vô ích.

## Why?

`startRunning()` có thể block; gọi trên main tạo UI freeze. Video data output nhanh hơn model inference sẽ backlog nếu giữ mọi frame. Copy pixel buffer/Data/Image nhiều lần làm tăng working set. Capture có thể bị interrupt bởi phone call, multitasking, system pressure hoặc device unavailable; code happy-path sẽ để UI “đang quay” trong khi session đã dừng.

## How?

```swift
import AVFoundation

final class CameraController: NSObject {
    let session = AVCaptureSession()
    private let sessionQueue = DispatchQueue(label: "camera.session")
    private let photoOutput = AVCapturePhotoOutput()

    func configure() {
        sessionQueue.async { [session, photoOutput] in
            session.beginConfiguration()
            defer { session.commitConfiguration() }

            guard let device = AVCaptureDevice.default(
                .builtInWideAngleCamera, for: .video, position: .back
            ),
            let input = try? AVCaptureDeviceInput(device: device),
            session.canAddInput(input), session.canAddOutput(photoOutput)
            else { return }

            session.addInput(input)
            session.addOutput(photoOutput)
        }
    }

    func start() {
        sessionQueue.async { [session] in
            guard !session.isRunning else { return }
            session.startRunning()
        }
    }
}
```

Production implementation cần idempotent reconfiguration khi đổi camera, permission-denied state, observer cho interruption/runtime error và teardown rõ. Không gọi session graph mutation đồng thời từ UI callbacks.

### Real-time buffer policy

Với `AVCaptureVideoDataOutput`, đặt queue riêng, chọn pixel format phù hợp downstream và thường discard late frames nếu chỉ cần latest observation. Dùng pool/reuse, tránh convert `CVPixelBuffer → CIImage → CGImage → UIImage` không cần thiết. Nếu ML/encode chậm, sample theo tốc độ consumer hoặc giữ slot latest-frame; không tạo unbounded Task cho mỗi callback.

### Orientation và audio

Tách device orientation, interface orientation và encoded media orientation. Update đúng capture/preview connection tại lifecycle an toàn; front camera có mirroring policy khác file output. Với audio/video recording, định nghĩa `AVAudioSession` category/mode/options, activation ownership, interruption và route change. Không tự resume recording sau mọi interruption nếu privacy/user expectation không cho phép.

### Media persistence

Ghi file tạm atomic, đặt quota và cleanup; không giữ `Data` video lớn trong memory. Upload dùng background URLSession khi cần survive suspension. Metadata có thể chứa location; strip hoặc xin consent theo product contract. Export phải có cancel/progress, disk-space error và lifecycle sau app termination.

## Production Case

### Context

App scan barcode và upload video bằng chứng đóng gói.

### Symptom

Sau 90 giây, preview giật và app bị jetsam trên thiết bị RAM thấp.

### Investigation

Time Profiler, Allocations và signpost frame pipeline cho thấy mỗi buffer tạo một unstructured Task; consumer chậm hơn producer, tasks giữ pixel buffers và intermediate UIImage.

### Root Cause

Không có backpressure/bounded concurrency; representation bị copy ba lần.

### Fix

Dùng single-slot latest frame, xử lý serial ngoài MainActor, giữ pixel buffer tới đúng boundary, downsample output và upload từ file URL.

### Prevention

Performance test 5 phút trên device tier thấp, metric dropped frames/thermal/memory peak, cancel khi screen disappear và resource budget được ghi trong ADR.

## Interview Questions

### Foundation

**Input, output và connection khác nhau thế nào?** Input cung cấp source, output tiêu thụ media, connection mô tả link và property như orientation/stabilization.

### Middle

**Tại sao không xử lý mọi frame bằng Task mới?** Producer có thể vượt consumer, gây backlog giữ buffer/memory; cần sampling/backpressure/bounded work.

### Senior

**Thiết kế camera pipeline production?** Nói về permission, session serialization, device capability, buffer format, backpressure, orientation/audio interruption, persistence/upload, privacy, metrics và device test.

## Exercises

### Easy

Vẽ capture graph cho chụp ảnh và preview.

### Medium

Thiết kế latest-frame processor có cancellation và chỉ một inference in-flight.

### Hard

Thiết kế record → atomic file → background upload → retry/cleanup chịu được app terminate.

### Debugging Lab

Profile camera 5 phút, đổi orientation/camera, giả lập interruption và chứng minh memory quay về baseline.

## Cheat Sheet

```text
session graph     → mutate serially
startRunning      → tránh main thread
sample buffers    → bounded consumer/backpressure
preview/output    → connections riêng, kiểm tra orientation
audio session     → category + route + interruption policy
large media       → file URL, không Data graph trong RAM
quality           → test device thật + thermal/memory/frame metrics
```

## Chapter Summary

1. AVFoundation là real-time resource pipeline, không chỉ UI camera.
2. Session graph cần serialized ownership.
3. Buffer processing phải bounded để tránh dropped frame và jetsam.
4. Orientation, audio interruption và device capability là production contract.
5. File lifecycle, privacy và background upload phải được thiết kế cùng capture.

## Related Chapters

- [Image decoding và cache budget](../Phase-09-Production/11-image-decoding-downsampling-va-cache-budget.md)
- [Background URLSession](../Phase-09-Production/22-bgtaskscheduler-background-urlsession-energy-va-debugging.md)
- [Video Feed](../Phase-10-Mobile-System-Design/07-video-feed-va-resource-budgeting.md)

## References

- [Apple — AVFoundation](https://developer.apple.com/documentation/avfoundation)
- [Apple — Setting up a capture session](https://developer.apple.com/documentation/avfoundation/setting-up-a-capture-session)
- [Apple — AVCaptureVideoDataOutput](https://developer.apple.com/documentation/avfoundation/avcapturevideodataoutput)
- [Apple — AVAudioSession](https://developer.apple.com/documentation/avfaudio/avaudiosession)
