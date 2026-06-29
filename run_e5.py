import os
import httpx
import asyncio
import random

# Lấy thông tin từ GitHub Secrets
CLIENT_ID = os.getenv("E5_CLIENT_ID")
CLIENT_SECRET = os.getenv("E5_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("E5_REFRESH_TOKEN")

async def main():
    async with httpx.AsyncClient() as client:
        # 1. Gọi API lấy Access Token và Refresh Token mới
        token_endpoint = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': REFRESH_TOKEN,
            'client_id': CLIENT_ID,
            'redirect_uri': 'http://localhost:53682/'
        }
        
        response = await client.post(token_endpoint, data=data)
        response_data = response.json()

        if 'access_token' not in response_data:
            print("Lỗi khi lấy token:", response_data)
            return

        access_token = response_data['access_token']
        new_refresh_token = response_data.get('refresh_token')

        # 2. Ghi Refresh Token mới ra file để GitHub Actions cập nhật
        if new_refresh_token:
            with open("new_refresh_token.txt", "w") as f:
                f.write(new_refresh_token)

        # 3. Random danh sách API và gọi để giữ E5
        graph_endpoints = [
            'https://graph.microsoft.com/v1.0/me/drive/root',
            'https://graph.microsoft.com/v1.0/me/drive',
            'https://graph.microsoft.com/v1.0/drive/root',
            'https://graph.microsoft.com/v1.0/users',
            'https://graph.microsoft.com/v1.0/me/messages',
            'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules',
            'https://graph.microsoft.com/v1.0/me/drive/root/children',
            'https://api.powerbi.com/v1.0/myorg/apps',
            'https://graph.microsoft.com/v1.0/me/mailFolders',
            'https://graph.microsoft.com/v1.0/me/outlook/masterCategories',
            'https://graph.microsoft.com/v1.0/applications?$count=true',
            'https://graph.microsoft.com/v1.0/me/?$select=displayName,skills',
            'https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages/delta',
            'https://graph.microsoft.com/beta/me/outlook/masterCategories',
            'https://graph.microsoft.com/beta/me/messages?$select=internetMessageHeaders&$top=1',
            'https://graph.microsoft.com/v1.0/sites/root/lists',
            'https://graph.microsoft.com/v1.0/sites/root',
            'https://graph.microsoft.com/v1.0/sites/root/drives'
        ]
        
        random.shuffle(graph_endpoints)
        headers = {
            'Authorization': f"{access_token}",
            'Content-Type': 'application/json'
        }

        for endpoint in graph_endpoints:
            # Ngủ random từ 2-6 giây giữa các lần gọi API như người thật
            await asyncio.sleep(random.randint(2, 6))
            try:
                await client.get(endpoint, headers=headers)
                print(f"Đã gọi thành công: {endpoint}")
            except Exception as e:
                print(f"Lỗi khi gọi {endpoint}: {e}")

if __name__ == "__main__":
    asyncio.run(main())
