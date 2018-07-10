"""
Shows basic usage of the Gmail API.

Lists the user's Gmail labels.
"""
from __future__ import print_function
import json

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# Setup the Gmail API
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('gmail', 'v1', http=creds.authorize(Http()))

last_message = 0
while(True):
    results = service.users().messages().list(userId='me', q='from:noreply@tradingview.com').execute()
    messages = results.get('messages', [])
    if not messages:
        print('No messages found.')
    else:
        if (last_message != messages[0]['id']):
            last_message = messages[0]['id']
            res = service.users().messages().get(userId='me',id=messages[0]['id']).execute()
            headers = res['payload']['headers']
            for header in headers:
                if header['name'] == 'Subject':
                    print('received mail' + header['value'])
                    info = json.loads(header['value'][19:])
                    print(info['direction'])
