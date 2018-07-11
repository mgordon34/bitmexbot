"""
Shows basic usage of the Gmail API.

Lists the user's Gmail labels.
"""
from __future__ import print_function
import json

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

class Mail():
    def __init__(self):
        self.last_message = 0
        self.service = None

    def connect(self):
        # Setup the Gmail API
        SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
        store = file.Storage('credentials.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
            creds = tools.run_flow(flow, store)
        self.service = build('gmail', 'v1', http=creds.authorize(Http()))

    def check_for_mail(self):
        results = self.service.users().messages().list(userId='me', q='from:noreply@tradingview.com').execute()
        messages = results.get('messages', [])
        if not messages:
            print('Error: No messages at all')
            return None
        else:
            if (self.last_message != messages[0]['id']):
                self.last_message = messages[0]['id']
                res = self.service.users().messages().get(userId='me',id=messages[0]['id']).execute()
                headers = res['payload']['headers']
                for header in headers:
                    if header['name'] == 'Subject':
                        info = json.loads(header['value'][19:])
                        return info
            else:
                return None
