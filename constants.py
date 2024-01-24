import json

cred_file = 'insta_scrap.json'
data = json.load(open(cred_file))

EMAIL_FROM = 'nikhilsannat.py@gmail.com'

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://mail.google.com/",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.send",
]
TOKEN_FILE = "token.pickle"
ACCESS_KEY = data["s3_cred"]["auth_key"]
SECRET_KEY = data["s3_cred"]["secret_key"]
BUCKET_NAME = "instascrapdata"
APP_KEY = data['firbase_cred']['APP_KEY']
EMAIL = "Your File can be downloaded from here:"
