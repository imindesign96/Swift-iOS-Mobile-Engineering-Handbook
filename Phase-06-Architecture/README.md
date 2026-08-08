# Phase 06 — Architecture

Phase này bắt đầu từ code đơn giản rồi tăng mức phân lớp theo độ phức tạp thực tế.

```text
View → ViewModel → Repository → Remote/Local
                  ↓ khi cần
                UseCase
```

Người học sẽ nhận diện Massive ViewController/ViewModel, thiết kế dependency direction, chọn Coordinator/Repository/DI có chủ đích, chia SPM modules theo feature boundary và lập migration plan tránh big-bang rewrite.

Roadmap chi tiết nằm trong [SUMMARY](../SUMMARY.md).

