import os
import requests
import random
import time
from base64 import b64encode
from nacl import encoding, public

CLIENT_ID = os.environ.get('CLIENT_ID')
REFRESH_TOKEN = os.environ.get('REFRESH_TOKEN')
GH_TOKEN = os.environ.get('GH_TOKEN')
REPO = os.environ.get('GITHUB_REPOSITORY')

def get_new_tokens():
    url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
    # Không cần client_secret nữa
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': REFRESH_TOKEN,
        'client_id': CLIENT_ID
    }
    response = requests.post(url, data=data).json()
    return response.get('access_token'), response.get('refresh_token')

def update_github_secret(new_refresh_token):
    headers = {
        'Authorization': f'token {GH_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    key_url = f'https://api.github.com/repos/{REPO}/actions/secrets/public-key'
    key_response = requests.get(key_url, headers=headers).json()
    
    public_key = public.PublicKey(key_response['key'].encode("utf-8"), encoding.Base64Encoder)
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(new_refresh_token.encode("utf-8"))
    encrypted_value = b64encode(encrypted).decode("utf-8")
    
    secret_url = f'https://api.github.com/repos/{REPO}/actions/secrets/REFRESH_TOKEN'
    data = {'encrypted_value': encrypted_value, 'key_id': key_response['key_id']}
    requests.put(secret_url, headers=headers, json=data)

def call_graph_api(access_token):
    endpoints = [
        'https://graph.microsoft.com/v1.0/me',
        'https://graph.microsoft.com/v1.0/users',
        'https://graph.microsoft.com/v1.0/me/drive',
        'https://graph.microsoft.com/v1.0/me/drive/root',
        'https://graph.microsoft.com/v1.0/me/messages',
        'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules',
        'https://graph.microsoft.com/v1.0/me/calendars',
        'https://graph.microsoft.com/v1.0/me/events',
        'https://graph.microsoft.com/v1.0/me/contacts'
    ]
    
    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
    
    # Chọn ngẫu nhiên 3 API để gọi trong mỗi lần chạy
    selected_endpoints = random.sample(endpoints, 3)
    
    for endpoint in selected_endpoints:
        try:
            req = requests.get(endpoint, headers=headers)
            print(f"Đã gọi: {endpoint} | Status: {req.status_code}")
        except Exception as e:
            print(f"Lỗi khi gọi {endpoint}: {e}")
        
        # Ngủ ngẫu nhiên từ 3 đến 10 giây giữa các lần gọi
        time.sleep(random.randint(3, 10))

if __name__ == "__main__":
    access_token, new_refresh_token = get_new_tokens()
    if access_token and new_refresh_token:
        print("Lấy token thành công, đang ghi đè Secret...")
        update_github_secret(new_refresh_token)
        print("Đang gọi Microsoft Graph API ngẫu nhiên...")
        call_graph_api(access_token)
        print("Hoàn tất quy trình.")
    else:
        print("Lỗi: Không thể lấy token. Token có thể đã bị Microsoft khóa.")
