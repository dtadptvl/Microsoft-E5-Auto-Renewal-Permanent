import httpx
import urllib.parse

# 1. ĐIỀN CLIENT ID CỦA BẠN VÀO ĐÂY (Trong ngoặc kép)
CLIENT_ID = "ĐIỀN CLIENT ID CỦA BẠN VÀO ĐÂY"
REDIRECT_URI = "http://localhost:53682/"

def main():
    # Khai báo các quyền cần thiết
    scopes = ['Directory.Read.All', 'Directory.ReadWrite.All', 'Files.Read', 'Files.Read.All', 'Files.ReadWrite', 'Files.ReadWrite.All', 'Mail.Read', 'Mail.ReadWrite', 'MailboxSettings.Read', 'MailboxSettings.ReadWrite', 'offline_access', 'Sites.Read.All', 'Sites.ReadWrite.All', 'User.Read', 'User.Read.All', 'User.ReadWrite.All']
    scope_str = "+".join(scopes)
    
    # Tạo link đăng nhập
    auth_url = f"https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={urllib.parse.quote(REDIRECT_URI, safe='')}&scope={scope_str}"
    
    print("=== BƯỚC 1: ĐĂNG NHẬP ===")
    print("Copy link dưới đây, dán vào trình duyệt và đăng nhập tài khoản E5 của bạn:\n")
    print(auth_url)
    print("\n--------------------------------------------------")
    print("=== BƯỚC 2: LẤY MÃ CODE ===")
    print("Sau khi đăng nhập, trình duyệt sẽ báo lỗi 'Không thể truy cập trang web này' (This site can't be reached). ĐIỀU NÀY LÀ BÌNH THƯỜNG!")
    print("Hãy nhìn lên thanh địa chỉ của trình duyệt, nó sẽ có dạng:")
    print("http://localhost:53682/?code=MÃ_CODE_DÀI_NGOẰNG_Ở_ĐÂY&session_state=...")
    
    # Nhập mã code
    raw_url = input("\nCopy TOÀN BỘ cái link bị lỗi trên thanh địa chỉ và dán vào đây, rồi ấn Enter: ")
    
    try:
        # Lọc lấy đoạn code từ link
        parsed_url = urllib.parse.urlparse(raw_url)
        code = urllib.parse.parse_qs(parsed_url.query)['code'][0]
        
        # Đổi code lấy Refresh Token (KHÔNG CẦN CLIENT SECRET)
        print("\nĐang xử lý để lấy Refresh Token...")
        token_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': CLIENT_ID,
            'redirect_uri': REDIRECT_URI,
            'code': code
        }
        
        response = httpx.post(token_url, data=data)
        response_data = response.json()
        
        if 'refresh_token' in response_data:
            print("\n🎉 THÀNH CÔNG! ĐÂY LÀ REFRESH TOKEN MỚI CỦA BẠN (Copy phần bên dưới):")
            print("======================================================================")
            print(response_data['refresh_token'])
            print("======================================================================")
        else:
            print("\n❌ LỖI TỪ MICROSOFT:", response_data)
            
    except Exception as e:
        print("\n❌ LỖI: Link bạn dán không hợp lệ hoặc không chứa mã code. Chi tiết:", e)

if __name__ == "__main__":
    main()
