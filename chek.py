import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Nếu bạn thay đổi các quyền truy cập, hãy xóa file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']  # Thay đổi quyền truy cập

def main():
    creds = None
    print("Checking for token.json...")
    
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        print("Token found.")
    else:
        print("Token not found, proceeding with authentication.")
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json',
            SCOPES
        )
        creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=10).execute()
    messages = results.get('messages', [])

    print(f"Messages found: {len(messages)}")
    if not messages:
        print('No messages found.')
    else:
        print('Messages:')
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            msg_snippet = msg['snippet']
            print(f'- {msg_snippet}')

            # Đánh dấu email là đã xem
            service.users().messages().modify(
                userId='me',
                id=message['id'],
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            print(f'Marked message {message["id"]} as read.')

if __name__ == '__main__':
    main()
