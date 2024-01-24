from service import vaildate_auth, listener
from utils import get_last_date, get_login_required, get_max_video, check_valid_email, get_url_list
from datetime import datetime, timedelta
from scrapper import Instabot
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel



class Item(BaseModel):
    username: str | None = None
    uid : str | None = None
    email: str | None = None
    password: str | None = None
    urls: str | None = None
    last_date: int | None = 7
    amount: int | None = 2
    login_required: bool | None = False
    access_token : str | None = ''

    
class AuthItem(BaseModel):
    auth_key: str | None = None

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/start")
async def root(item:Item):
    try:
        username = item.username
        password = item.password
        uid = item.uid
        email = check_valid_email(item.email)
        amount = get_max_video(item.amount)
        login_required = True # get_login_required(item.login_required)
        last_date = get_last_date(item.last_date)
        auth_key = item.access_token
        url_list = get_url_list(item.urls) 

        if not vaildate_auth(auth_key):
             raise Exception("AUTH TOKEN NOT VALID")
        # try:
        #     Instabot.valid_cred(username, password)
        # except Exception as e:
        #      raise HTTPException(status_code=401, detail=e)
        listener(username, password, url_list, uid, email, amount, last_date, login_required)
    except Exception as e:
        with open("app_error.text", "a+") as f:
                f.write(f"DATE  = {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} : Error While Receving the Request: {str(e)}\n")
        raise HTTPException(status_code=401, detail=e)
    return {"message": "Requested Listed! You will get your file in your email"}



@app.get("/validate_auth")
async def validate_auth_token(auth_key:str = ""):
    try:
        print("auth_key",auth_key)
        if vaildate_auth(auth_key) :
             return {"status" : 200, "message": "Valid Auth Key"}
        else:
             raise HTTPException(status_code=401, detail="Token Not Valid")
    except Exception as e:
        with open("app_error.text", "a+") as f:
                f.write(f"DATE  = {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} : Error While Receving the Request: {str(e)}\n")
        raise HTTPException(status_code=401, detail="Token Not Valid")
