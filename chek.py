import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Nếu bạn thay đổi các quyền truy cập, hãy xóa file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    creds = None
    print("Checking for token.json...")
    
    # Kiểm tra xem token.json có tồn tại không
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        print("Token found.")
    else:
        print("Token not found, proceeding with authentication.")
        # Nếu không có token, yêu cầu người dùng đăng nhập
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json',
            SCOPES
        )
        creds = flow.run_local_server(port=0)

        # Lưu thông tin xác thực để sử dụng lần sau
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Tạo dịch vụ Gmail
    service = build('gmail', 'v1', credentials=creds)

    # Gọi API Gmail để lấy email
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=10).execute()
    messages = results.get('messages', [])

    # Kiểm tra và in ra số lượng email
    print(f"Messages found: {len(messages)}")
    if not messages:
        print('No messages found.')
    else:
        print('Messages:')
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            msg_snippet = msg['snippet']
            print(f'- {msg_snippet}')

if __name__ == '__main__':
    main()
