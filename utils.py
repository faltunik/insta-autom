import re

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

INSTAGRAM_URL = 'https://www.instagram.com/'

def get_max_video(obj):
    try:
        vid = max(int(obj), 50)
        return vid
    
    except:
        return 5
    
def get_last_date(obj):
    try:
        last = max(int(obj), 30)
    except:
        return 7
    
def get_login_required(obj):
    try:
        obj = bool(obj)
        return obj
    except:
        return True
    
def get_url_list(url_list):
    try:
        url_list = url_list.split("##")
        full_url_list = []
        for url in url_list:
            try:
                full_link = INSTAGRAM_URL + url + '/' 
                full_url_list.append(full_link)
            except:
                    continue
        url_list = full_url_list

        return url_list

    except:
        return []


def check_valid_email(email):
    if(re.fullmatch(regex, email)):
        return email
    else:
        raise Exception("EMAIL IS NOT VALID")
