import os
import base64
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Quyền truy cập
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    creds = None
    
    # Lấy client_id và client_secret từ biến môi trường
    client_id = os.environ.get('GOOGLE_CLIENT_ID')
    client_secret = os.environ.get('GOOGLE_CLIENT_SECRET')
    
    # Xác thực và tạo Credentials
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_dict(
                {
                    'installed': {
                        'client_id': client_id,
                        'client_secret': client_secret,
                        'redirect_uris': ['urn:ietf:wg:oauth:2.0:oob'],
                    }
                },
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Lưu thông tin xác thực vào file token.json
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    # Gọi API Gmail
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=10).execute()
    messages = results.get('messages', [])

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
