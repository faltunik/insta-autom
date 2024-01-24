import os
import pickle
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import base64
from email.message import EmailMessage
from constants import TOKEN_FILE, EMAIL_FROM, SCOPES



class Email:
    def __init__(self, receiver, file_name=""):
        self.receivers = receiver
        self.file_name = file_name

    @staticmethod
    def authenticate():
        creds = None
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, "rb") as token:
                creds = pickle.load(token)

        # If no valid credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(creds, token)

        return creds


    def send_emails(self, email_content):
        receiver = self.receivers
        self.send_email(receiver, email_content)
        return

    def send_email(self, receiver, email_content):
        creds = self.authenticate()
        service = build("gmail", "v1", credentials=creds)
        message = EmailMessage()
        message.set_content(email_content)
        if self.file_name:
            attachment = self.file_name
            with open(attachment, 'rb') as content_file:
                content = content_file.read()
                message.add_attachment(content, maintype='application', subtype= (attachment.split('.')[1]), filename=attachment)
        message["to"] = receiver
        message["from"] = EMAIL_FROM
        message["subject"] = "Your Instagram Scrapping Data"
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {"raw": encoded_message}
        # pylint: disable=E1101
        send_message = (
            service.users()
            .messages()
            .send(userId=EMAIL_FROM, body=create_message)
            .execute()
        )
        print(f'Message Id: {send_message["id"]}')

        return send_message



