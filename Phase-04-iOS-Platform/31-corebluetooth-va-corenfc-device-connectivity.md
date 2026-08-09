---
title: "CoreBluetooth và Core NFC: device connectivity an toàn"
phase: "iOS Platform"
difficulty: 5
importance: 3
interview_frequency: 3
status: complete
last_verified: 2026-08-09
swift_baseline: "Swift 6.3 toolchain; Swift 6 language mode"
levels:
  - L4
  - L5
prerequisites:
  - "State machine thay cho boolean explosion"
  - "Background execution và interrupted work"
used_later:
  - "App Store release engineering: signing, privacy, review và rollback"
competencies:
  - "iOS Platform"
  - "Architecture"
  - "Security"
  - "Production"
tags:
  - "corebluetooth"
  - "core-nfc"
  - "ble"
  - "device-connectivity"
---

# CoreBluetooth và Core NFC: device connectivity an toàn

> **Version scope**
>
> BLE và NFC phụ thuộc hardware, entitlement, region và device. Simulator không thay thế thiết bị/peripheral/tag thật. HCE/payment capability có entitlement và điều kiện riêng; không suy rộng từ NDEF reader. Xác minh 2026-08-09.

## Story / Problem

Ứng dụng kho kết nối máy quét BLE rồi thỉnh thoảng “Connected” nhưng không nhận dữ liệu; NFC session đóng với error dù tag đã đọc thành công. Team dùng hai boolean `isConnected` và `hasTag`, bỏ qua state machine của radio, discovery, service/characteristic, session invalidation và timeout.

```text
BLE: manager state → scan → discover → connect → discover services/chars
     → subscribe/read/write → disconnect/restore

NFC: capability → user starts session → detect/connect/read/write → invalidate
```

Callbacks là event; state hiện tại phải được mô hình hóa và validate trước khi thực hiện command tiếp theo.

## Objectives

Sau chapter này, bạn có thể:

- thiết kế BLE central flow có state, timeout, retry và restoration;
- hiểu peripheral identity, service/characteristic discovery và notification subscription;
- kiểm soát scanning, duplicate advertisements, battery và background constraint;
- cấu hình NFC capability, usage description, session và tag protocol đúng scope;
- phân loại expected invalidation, user cancellation, transport và protocol error;
- bảo vệ command/data khỏi spoofing, replay và assumption sai về radio proximity.

## Prerequisites

- [State machine](../Phase-06-Architecture/09-state-machine-thay-cho-boolean-explosion.md).
- [Background execution](../Phase-09-Production/16-background-execution-va-interrupted-work.md).
- [CoreLocation permission và energy](22-corelocation-permission-accuracy-background-va-energy.md) cho permission/energy thinking.

## Used Later

- [App Store release engineering](../Phase-09-Production/21-app-store-release-engineering-signing-privacy-review-va-rollback.md) audit capability/entitlement/purpose string.
- [Production scenario interview](../Phase-11-Interview/11-production-scenario-interview.md).

## Mental Model

```text
Radio discovery ≠ authenticated identity
Connected       ≠ service ready
Write accepted  ≠ device applied command
NFC proximity   ≠ trusted payload
```

BLE UUID quảng bá và peripheral identifier hỗ trợ discovery/retrieval nhưng không tự là security identity. Protocol ứng dụng cần version, message framing, sequence, acknowledgement và authentication/integrity nếu command có giá trị.

## What?

`CBCentralManager` quản lý scan/discover/connect; chỉ bắt đầu work khi state `.poweredOn`. `CBPeripheral` đại diện peer; sau connect phải discover service/characteristic cần thiết rồi read/write/subscribe. Delegate callbacks có queue contract và có thể đến sau user đã rời screen, nên một session owner giữ generation/cancellation.

Core NFC tạo reader session do user khởi động, yêu cầu capability/entitlement và `NFCReaderUsageDescription`. `NFCNDEFReaderSession` phù hợp NDEF; `NFCTagReaderSession` cho ISO7816/ISO15693/FeliCa/MIFARE theo configuration. Session có thời hạn và invalidation là terminal event; một số invalidation code là expected completion, không phải lỗi báo user.

## Why?

Scan vô hạn đốt pin và thu duplicate advertisements. Auto-reconnect vô hạn có thể chiếm radio, spam log và làm thiết bị khác không kết nối được. Write without response tăng throughput nhưng không cho application acknowledgement. NFC tag có thể chứa URL độc hại; mở thẳng hoặc tin payload định giá tạo injection/fraud.

## How?

```swift
import CoreBluetooth

enum BLEState: Equatable {
    case unavailable
    case scanning
    case connecting(UUID)
    case discovering(UUID)
    case ready(UUID)
    case failed(String)
}

final class Scanner: NSObject, CBCentralManagerDelegate {
    private lazy var manager = CBCentralManager(delegate: self, queue: nil)
    private(set) var state: BLEState = .unavailable

    func centralManagerDidUpdateState(_ central: CBCentralManager) {
        guard central.state == .poweredOn else {
            state = .unavailable
            return
        }
        state = .scanning
        central.scanForPeripherals(withServices: [DeviceProtocol.serviceUUID])
    }
}
```

Production code phải stop scan theo deadline/selection, dedupe theo identifier + advertisement semantics, connect với timeout và chuyển `.ready` chỉ sau required characteristic discovery/notification subscription. Không đưa raw delegate object trực tiếp vào ViewModel; adapter biến callbacks thành typed events/testable state transition.

### BLE protocol và restoration

Định nghĩa framing vì một logical message có thể split/merge theo MTU. Serialize writes theo device capability; checksum/crypto không thay thế business authentication. Reconnect dùng bounded backoff và chỉ khi product cần. State restoration dùng stable restore identifier và rebuild graph từ callback; không giả định mọi callback cũ vẫn hợp lệ sau process relaunch.

Background mode không cấp runtime vô hạn. Scan/advertising behavior thay đổi và system tối ưu năng lượng. Hãy persist minimal session intent, xử lý delayed event idempotently và có foreground recovery.

### NFC session và security

```swift
import CoreNFC

func beginNDEFScan(delegate: NFCNDEFReaderSessionDelegate) -> NFCNDEFReaderSession? {
    guard NFCNDEFReaderSession.readingAvailable else { return nil }
    let session = NFCNDEFReaderSession(
        delegate: delegate,
        queue: nil,
        invalidateAfterFirstRead: true
    )
    session.alertMessage = "Giữ iPhone gần nhãn sản phẩm."
    session.begin()
    return session
}
```

Giữ strong reference tới session đến invalidation. Validate record type/length/schema/signature/domain allowlist trước action. Background tag reading cho supported URL types và Universal Links, không phải tùy ý chạy app logic; luôn có in-app scan fallback.

## Production Case

### Context

Nhân viên dùng BLE scanner và NFC tag để xác nhận hàng.

### Symptom

Đơn đôi khi được xác nhận hai lần sau reconnect; UI hiển thị lỗi sau NFC scan thành công.

### Investigation

Trace event sequence cho thấy write được retry sau disconnect mà không có command ID; thiết bị đã áp dụng lần đầu. NFC delegate coi `readerSessionInvalidationErrorFirstNDEFTagRead` như fatal.

### Root Cause

Protocol thiếu idempotency/acknowledgement và error taxonomy không phân biệt expected terminal state.

### Fix

Thêm command ID + device ack ledger, reconcile trước retry; map NFC first-read/user-cancel thành success/cancel thay vì alert error.

### Prevention

Hardware-in-loop test cho disconnect giữa write/ack, RF noise, duplicate tag, malformed record, permission off và app relaunch/restoration.

## Interview Questions

### Foundation

**BLE connected đã sẵn sàng trao đổi dữ liệu chưa?** Chưa; còn discover service/characteristic và subscribe/read/write contract.

### Middle

**Vì sao NFC proximity không đủ để trust dữ liệu?** Tag có thể bị sao chép/thay thế; phải validate schema, origin và chữ ký/authority nếu action nhạy cảm.

### Senior

**Thiết kế device workflow chịu disconnect?** State machine, command ID, framing, ack, timeout, bounded retry, restoration, persistence, hardware tests và telemetry.

## Exercises

### Easy

Vẽ BLE state machine từ poweredOff đến ready/disconnected.

### Medium

Thiết kế parser cho framed message bị split qua nhiều characteristic notifications.

### Hard

Thiết kế idempotent command protocol cho mở khóa thiết bị, gồm authentication và replay protection.

### Debugging Lab

Tắt Bluetooth giữa write/ack, relaunch app và chứng minh không áp command hai lần; scan NFC malformed tag và giữ UI recoverable.

## Cheat Sheet

```text
BLE poweredOn         → mới scan/connect
connected             → chưa ready
scan                   → filter + deadline + stop
write                  → cần framing/ack/idempotency tùy risk
restoration            → stable identifier + rebuild state
NFC                    → user session + entitlement + timeout
tag payload            → untrusted input
validation             → device thật/hardware-in-loop
```

## Chapter Summary

1. BLE/NFC là event-driven state machine chịu hardware lifecycle.
2. Discovery/connect không chứng minh identity hay command completion.
3. Energy và background runtime phải bounded.
4. NFC session invalidation cần taxonomy, payload cần validation.
5. Workflow giá trị cao cần application-level security và idempotency.

## Related Chapters

- [State machine](../Phase-06-Architecture/09-state-machine-thay-cho-boolean-explosion.md)
- [Background execution](../Phase-09-Production/16-background-execution-va-interrupted-work.md)
- [Universal Links](23-universal-links-aasa-routing-fallback-va-security.md)

## References

- [Apple — CBCentralManager](https://developer.apple.com/documentation/corebluetooth/cbcentralmanager)
- [Apple — Central Manager State Restoration](https://developer.apple.com/documentation/corebluetooth/central-manager-state-restoration-options)
- [Apple — Core NFC](https://developer.apple.com/documentation/corenfc)
- [Apple — Building an NFC Tag-Reader App](https://developer.apple.com/documentation/corenfc/building-an-nfc-tag-reader-app)
