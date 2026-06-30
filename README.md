# 🔄 Microsoft E5 Auto Renew (Public Client Edition)

Kịch bản Python tự động gọi Microsoft Graph API để duy trì gói đăng ký Microsoft 365 E5 Developer. Phiên bản này sử dụng luồng xác thực **Public Client (Mobile and desktop applications)**, giúp loại bỏ hoàn toàn sự phụ thuộc vào Client Secret (vốn bị giới hạn thời hạn tối đa 24 tháng bởi Microsoft).

Hệ thống được thiết kế để chạy hoàn toàn tự động trên **GitHub Actions** và tự động ghi đè Refresh Token mới vào GitHub Secrets sau mỗi lần chạy.

> [!WARNING]
> **Rủi ro Cảnh báo (Impossible Travel):** Việc sử dụng Public Client trên GitHub Actions sẽ khiến tài khoản có nguy cơ bị khóa Token do địa chỉ IP thay đổi liên tục qua các quốc gia (GitHub Actions cấp phát IP ngẫu nhiên). Thuật toán của Microsoft có thể nhận diện đây là hành vi đánh cắp thiết bị. Để an toàn tuyệt đối, khuyến nghị chạy kịch bản này trên một thiết bị có IP tĩnh (ví dụ: Raspberry Pi hoặc máy tính cá nhân sử dụng Self-hosted Runner).

## 📂 Cấu trúc Repository

Để hệ thống tinh gọn và hoạt động tốt nhất, repo này chỉ giữ lại các tệp tin cốt lõi:

* `auto_renew.py`: Kịch bản chính dùng để gọi API ngẫu nhiên và làm mới Token.
* `get_token.py`: Công cụ hỗ trợ (Device Code Flow) dùng để lấy Refresh Token ban đầu (hoặc dùng để cấp cứu khi chuỗi token bị đứt).
* `.github/workflows/renew.yml`: Cấu hình lịch chạy CI/CD của GitHub Actions.

---

## ⚙️ Hướng dẫn Cài đặt & Thiết lập

### Bước 1: Cấu hình ứng dụng trên Azure Portal
1. Truy cập [Azure Active Directory > App registrations](https://portal.azure.com/#view/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/~/RegisteredApps) và tạo một ứng dụng mới (hoặc chọn ứng dụng hiện có).
2. Chuyển đến mục **Authentication**.
3. Nhấp vào **Add a platform** và chọn **Mobile and desktop applications**.
4. Trong phần *Custom redirect URIs*, nhập chính xác: `http://localhost`.
5. Lưu lại. (Bạn có thể bỏ qua hoàn toàn mục *Certificates & secrets*).

### Bước 2: Lấy Refresh Token lần đầu
Vì không sử dụng Client Secret, bạn cần lấy token lần đầu thông qua luồng thiết bị (Device Code Flow).

1. Tải file `get_token.py` về máy tính cá nhân.
2. Mở file, thay thế biến `CLIENT_ID` bằng Application (client) ID của bạn.
3. Mở Terminal/Command Prompt và chạy kịch bản:
   ```bash
   pip install requests
   python get_token.py
