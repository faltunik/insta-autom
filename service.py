import datetime
import os
import requests
from s3_services import S3
from scrapper import main_executer
from email_service import  Email
import concurrent.futures
import threading
from constants import APP_KEY, EMAIL



s3_obj = S3()


def generate_csv_file(username, password, url_list, uid, email, amount = 2, last_date=7, login_required=True):
    # read url from file
    date = datetime.datetime.now()
    date_str = date.strftime("%Y_%m_%d_%H_%M_%S")
    username = 'instragram username'
    password = 'instagram password'
    filename = f"{uid}_{date_str}.csv"
    amount = amount
    last_date = last_date
    print(f"STSRTTING URL LIST = {url_list}")
    
    try:
        main_executer(url_list, password, username, filename, amount, last_date, login_required)
        email_service = Email(receiver=email, file_name=filename)
        email_service.send_emails(EMAIL)
        # if filename path exists, delete it
        try:
            s3_obj.upload_file(filename)
            os.remove(filename)
        except:
            print("Error while deleting the file")
        print(f"EMAIL DONE FOR {email}")
    except Exception as e:
        print(e)
        email_service = Email(receiver=email)
        email_service.send_emails(e)
        with open("app_error.text", "a+") as f:
                f.write(f"DATE  = {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} : Error While Generating CSV : {str(e)}\n")
        return False



def vaildate_auth(auth_key):
    url = "https://identitytoolkit.googleapis.com/v1/accounts:lookup?key=" + APP_KEY
    payload = "{\"idToken\":\"" + auth_key + "\"}"
    headers = {
         'Content-Type': 'text/plain'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        return True
    else:
        return False



def listener(username, password, url_list, uid, email, amount, last_date, login_required):
    try:
        job_ins = threading.Thread(target=generate_csv_file, args = (username, password, url_list, uid, email, amount, last_date, login_required ))
        job_ins.start()
    except Exception as e:
        with open("app_error.text", "a+") as f:
                f.write(f"DATE  = {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} : Error While Starting the Thread: {str(e)}\n")
                raise Exception(e)
    return True


    


