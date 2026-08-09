---
title: "App Store release engineering: signing, privacy, review và rollback"
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
  - "iOS CI/CD với Bitrise và fastlane"
  - "Release-only và device-specific bugs"
used_later:
  - "Production scenario interview"
  - "Mobile System Design interview"
competencies:
  - "Production"
  - "Security"
  - "CI/CD"
  - "Technical Leadership"
tags:
  - "app-store-connect"
  - "code-signing"
  - "testflight"
  - "privacy-manifest"
  - "release-rollback"
---

# App Store release engineering: signing, privacy, review và rollback

> **Version scope**
>
> App Store Connect, upload requirements, privacy/API policy và review rules thay đổi theo thời gian. Dùng official current documentation làm release input, không đóng băng checklist nhiều năm. Xác minh 2026-08-09.

## Story / Problem

Build chạy trên máy developer nhưng CI archive fail signing. Sau khi sửa, upload bị reject vì privacy manifest của SDK. Build khác qua TestFlight nhưng production crash do entitlement/environment. Khi rollout lỗi, team hỏi “rollback binary” rồi phát hiện App Store không giống server deploy. Release iOS là một hệ thống gồm identity, signing, capabilities, metadata, policy, review, staged distribution và runtime mitigation.

```text
Source + dependencies + configuration
            ↓ reproducible archive/sign
       validation/upload
            ↓
   TestFlight evidence → App Review → controlled release
            ↓
 telemetry/feature flags/API compatibility → mitigate/fix-forward
```

## Objectives

Sau chapter này, bạn có thể:

- giải thích quan hệ certificate, App ID, provisioning profile, entitlement và signature;
- vận hành archive/upload/TestFlight/App Review có traceability;
- audit Privacy Manifest, Required Reason API và third-party SDK;
- chọn manual/automatic release, phased rollout và monitoring gate;
- thiết kế rollback thực tế bằng pause, kill switch, server compatibility và fix-forward;
- điều tra release-only incident mà không “thử lại certificate” ngẫu nhiên.

## Prerequisites

- [iOS CI/CD với Bitrise và fastlane](19-ios-ci-cd-voi-bitrise-va-fastlane.md).
- [Release-only và device-specific bugs](15-release-only-va-device-specific-bugs.md).
- [Observability, SLO và incident response](18-observability-slo-va-incident-response.md).

## Used Later

- [Production scenario interview](../Phase-11-Interview/11-production-scenario-interview.md).
- [Mobile System Design interview](../Phase-11-Interview/14-mobile-system-design-interview.md).

## Mental Model

```text
Certificate          → ai/team ký
Bundle ID / App ID   → application identity
Entitlements         → capability binary yêu cầu
Provisioning profile → Apple-authorized binding của identity/certificate/capability
Code signature       → integrity + signer + entitlements được seal
```

Signing success không chứng minh service configuration đúng. Associated Domains, APNs, App Groups, iCloud/CloudKit, HealthKit hay IAP còn có server/container/App Store Connect side. Mỗi target/extension có bundle ID, capability và profile riêng.

## What?

Release pipeline tạo archive từ pinned source/dependencies/configuration, ký bằng đúng distribution identity/profile, validate artifact, upload build, xử lý App Store Connect processing, phân phối internal/external TestFlight, submit metadata/compliance/privacy cho review và release theo policy.

Build được nhận diện bằng marketing version và unique build number. Artifact đã test phải là artifact submit; không rebuild tùy tiện giữa QA và release. Commit SHA, Xcode/SDK, dependency lock, build number, symbols, privacy report, tests và approver được gắn thành release evidence.

## Why?

Signing asset có expiration/revocation/team ownership. Automatic signing tiện local nhưng CI nhiều app/extension vẫn cần ownership rõ. SDK mới có thể thêm entitlement, data collection hoặc Required Reason API. App Review đánh giá cả binary, metadata, login/demo, permission purpose và behavior server-side. Một app đã phát hành không thể đảm bảo mọi device lập tức quay lại binary cũ; propagation/update do App Store và user quyết định.

## How?

### Signing và entitlement investigation

Đầu tiên xác định exact target, configuration, bundle ID, team, archive và distribution method. So sánh requested entitlements trong built app với provisioning profile, không chỉ xem Xcode UI. Kiểm tra profile expiration, certificate chain/private key availability và capability bật ở Developer account. Với extension, kiểm tra App Group/Keychain Access Group/Associated Domains nhất quán nhưng scope tối thiểu.

CI dùng secret store, least-privilege App Store Connect API key và rotation/runbook. Không commit `.p12`, API private key, profile chứa thông tin team hoặc password. Signing asset change phải auditable; tránh một laptop cá nhân là single point of failure.

### App Store Connect và TestFlight

Upload build bằng supported Xcode/toolchain/API; theo dõi processing status và warnings. Internal testing xác minh smoke nhanh, external TestFlight kiểm tra review beta/real account/device/network. Checklist bao gồm clean install, upgrade từ production, login/logout, purchase/restore, push production, deep link, extension, background transfer, migration, localization/accessibility và privacy prompts.

App Review submission cần metadata chính xác, privacy URL, age/content/compliance, review notes, demo account và hướng dẫn hardware/backend nếu feature khó thấy. Review note không dùng để che behavior; server/test account phải ổn định trong review window.

### Privacy Manifest và Required Reason API

Mỗi app/SDK khai báo data collection/tracking và Required Reason API đúng responsibility. `PrivacyInfo.xcprivacy` phải hợp lệ; tạo privacy report từ archive và so sánh với App Store privacy answers. Inventory SDK theo owner/version/data/network/API; upgrade hoặc loại SDK không cung cấp manifest hợp lệ. Approved reason phải phản ánh actual feature, không chọn reason để qua validation.

### Release strategy

Manual release cho phép business/engineering chọn thời điểm sau approval. Phased release giảm blast radius nhưng không thay observability và kill switch; user vẫn có thể update thủ công. Gate rollout bằng crash-free sessions, hang, launch, auth/purchase success, backend errors và support signal theo app version. Segment canary không chứa PII và metric có baseline phiên bản trước.

### Rollback reality

Binary mobile thường **fix-forward**. Khi incident:

1. xác nhận impact/version/feature và đóng băng rollout;
2. pause phased release nếu đang chạy;
3. tắt feature/config/endpoint bằng kill switch an toàn;
4. giữ backend backward-compatible với binary đang lưu hành;
5. phát hotfix, request expedited review khi đủ điều kiện;
6. hướng dẫn support/user và theo dõi adoption.

Remove app khỏi sale không gỡ binary khỏi device đã cài. Server bắt client update bắt buộc chỉ là last resort vì có thể khóa user và làm review/recovery khó hơn. Database migration cần forward/backward compatibility hoặc remote disable trước khi binary mới ghi schema không thể quay lại.

## Production Case

### Context

Version 8.4 phát hành phased, thay auth refresh và thêm SDK analytics.

### Symptom

Crash-free giảm ở iOS cũ; một số user bị logout loop. Privacy warning xuất hiện khi upload hotfix.

### Investigation

Release dashboard theo version/OS chỉ ra feature flag mới. Symbolicated trace nằm trong adapter SDK gọi Required Reason API; auth API mới không tương thích request từ version cũ khi token refresh fallback.

### Root Cause

Rollout không có compatibility matrix; SDK inventory/privacy audit chỉ chạy sau upload.

### Fix

Pause phased release, disable adapter bằng remote flag, phục hồi endpoint backward-compatible, cập nhật SDK/manifest và phát hotfix từ same release branch.

### Prevention

Privacy report diff trong CI, upgrade-from-production E2E, API N/N-1 contract test, release canary và documented kill switch owner.

## Interview Questions

### Foundation

**Provisioning profile làm gì?** Nó bind App ID/capability với certificate và distribution context được Apple cho phép; signature seal artifact/entitlements.

### Middle

**TestFlight pass có đảm bảo App Store production đúng?** Không; account/environment/review/rollout và production backend khác, vẫn cần production capability test và telemetry.

### Senior

**Rollback iOS release thế nào?** Pause rollout, remote mitigate, giữ backend compatible, fix-forward/hotfix và monitor; không giả định cài lại binary cũ tức thì.

## Exercises

### Easy

Vẽ signing chain cho app + Notification Service Extension + widget.

### Medium

Tạo release checklist gồm upgrade, purchase, push, privacy và observability gates.

### Hard

Thiết kế backward-compatible API/schema rollout cho ba app versions cùng tồn tại.

### Debugging Lab

So sánh entitlements của archive/profile cho một lỗi App Group giả lập; xác định exact mismatch bằng evidence.

## Cheat Sheet

```text
artifact       → build once, promote same archive
signing        → identity + profile + entitlements + signature
TestFlight     → real distribution evidence, chưa phải production guarantee
privacy        → manifest + Required Reason APIs + SDK inventory + disclosure
phased release → giảm blast radius, không thay kill switch
rollback       → pause + mitigate remotely + compatible server + fix-forward
release metric → version/OS/feature segmented, privacy-safe
```

## Chapter Summary

1. Signing là authorization/integrity chain, không phải phép thử may rủi.
2. Release artifact cần reproducibility và traceability.
3. Privacy manifest/SDK inventory là CI input, không chờ upload mới audit.
4. TestFlight, review và staged release đều cần explicit evidence gates.
5. Mobile rollback chủ yếu là remote mitigation và fix-forward.

## Related Chapters

- [CI/CD với Bitrise và fastlane](19-ios-ci-cd-voi-bitrise-va-fastlane.md)
- [Release-only bugs](15-release-only-va-device-specific-bugs.md)
- [Observability và incident response](18-observability-slo-va-incident-response.md)

## References

- [Apple — Certificates overview](https://developer.apple.com/help/account/create-certificates/certificates-overview)
- [Apple — Capabilities overview](https://developer.apple.com/help/account/capabilities/capabilities-overview)
- [Apple — Upload builds](https://developer.apple.com/help/app-store-connect/manage-builds/upload-builds/)
- [Apple — Adding a privacy manifest](https://developer.apple.com/documentation/bundleresources/adding-a-privacy-manifest-to-your-app-or-third-party-sdk)
- [Apple — Describing use of required reason API](https://developer.apple.com/documentation/bundleresources/describing-use-of-required-reason-api)
- [App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)
