# GMAIL PYTHON CLIENT.

from apiclient import discovery
from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
import base64
from bs4 import BeautifulSoup
import re
import time
import dateutil.parser as parser
from datetime import datetime
import datetime
import email

# scope can be modified to send/delete/trash mails.
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))

# get all the messages with provided labels.
def get_all_messages_with_labels(labelids, userid='me'):
    response = GMAIL.users().messages().list(userId=userid,labelIds=labelids).execute()
    messages = []
    if 'messages' in response:
        messages.extend(response['messages'])
    while 'nextPageToken' in response:
        pagetoken = response['nextPageToken']
        response = GMAIL.users().messages().list(userId=userid,labelIds=labelids,pageToken=pagetoken).execute()
        messages.extend(response['messages'])
    return messages

# get all the label ids.
def get_all_label_ids(userid='me'):
    labelids = []
    results = GMAIL.users().labels().list(userId=userid).execute()
    labels = results.get('labels',[])
    for label in labels:
        labelids.append(label['id'])
    return labelids

# get unread messages from front page only.
def get_top_unread_messages(userid='me'):
    response = GMAIL.users().messages().list(userId=userid,labelIds=['UNREAD']).execute()
    messages = []
    if 'messages' in response:
        messages.extend(response['messages'])
    return messages

# print message headers.
def print_message_headers(messages, userid='me'):
    for message in messages:
        msgid = message['id']
        message = GMAIL.users().messages().get(userId=userid, id=msgid).execute()
        payload = message['payload']
        headers = payload['headers']
        for header in headers:
            if header['name'] == 'From':
                fromstr = header['value']
            if header['name'] == 'Subject':
                subject = header['value']
            if header['name'] == 'Date':
                date = header['value']
        print ('From: ' + fromstr, 'Subject: ' + subject, 'Date: ' + date, sep='\n')
        print ('-'*80)

