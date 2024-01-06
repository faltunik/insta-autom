import os
from datetime import datetime, timedelta
from instagrapi import Client
import concurrent.futures



VIDEO_TYPE = 2
IMAGE_TYPE = 1


class Instabot:
    def __init__(self, username, password, login_required=False):
        self.client = Client()
        if login_required:
            self.client.login(username, password)

    @staticmethod
    def get_username_from_link(link):
        """
        returns: String : Username
        """
        if link and link[-1] == "/":
            link = link[:-1]
        try:
            return link.split("/")[-1]
        except:
            print("PLEASE PASS CORRECT URL")
            return "-1"

    def scrape_url(self, link, filename, amount=25, last_date=-1):
        """ """
        username = Instabot.get_username_from_link(link)
        if username == "-1":
            return
        userid = self.client.user_id_from_username(username)
        if last_date != -1:
            last_date = datetime.now() - timedelta(days=last_date)
        medias = self.get_medias_list(userid, amount, start="", last_date=last_date, link= link)
        #medias = self.analyse_media(medias, link, filename)
        #self.write_on_file(medias, filename)
        return

    def get_medias_list(self, userid, amount=50, start="", last_date=-1, link = ''):
        response = []
        run = True
        iteration = 0
        INITIAL_AMOUNT = amount
        print(f'HERE WE ARE {userid}')
        while run and amount > 0 and iteration < 6:
            medias, end_cursor = self.client.user_medias_paginated_gql(
                userid, amount=49, sleep=2, end_cursor=start
            )
            try:
                if last_date != -1 and medias[-1].taken_at < last_date:
                    run = False
            except:
                pass
            medias = self.analyse_media(medias, link, filename)
            start = end_cursor
            amount -= len(medias)
            response.extend(medias)
            if len(response) > INITIAL_AMOUNT:
                run = False
            # check for date of last media, if it's older than last_data then we simply break the loop
            
            iteration +=1

        return response

    def analyse_media(self, medias, link, filename):
        response = []
        for obj in medias:
            if obj.media_type != VIDEO_TYPE:
                continue
            _dict = {}
            _dict["URL"] = link
            try:
                _dict["views"] = obj.view_count or obj.play_count
            except:
                continue
            try:
                _dict["comments"] = obj.comment_count
            except:
                _dict["comments"] = "NA"
            try:
                _dict["likes"] = obj.like_count
            except:
                _dict["likes"] = "NA"
            try:
                _dict['video_url'] = "https://www.instagram.com/p/" +str(obj.code) + "/"
            except:
                pass
            try:
                Instabot.write_on_file(filename, _dict)
            except:
                pass
            response.append(_dict)
        print(f" RESPINSE FOR {link}, {filename} = {response}")
        return response

    @staticmethod
    def write_on_file(csv_file_name, data):
        # Page name(url) / Video name (or link) / Views / Likes / Comments
        url = data.get("URL", "NA")
        video_link = data.get("video_url", "NA")
        views = data.get("views", "NA")
        likes = data.get("likes", "NA")
        comments = data.get("comments", "NA")
        with open(csv_file_name, "a+") as f:
            f.write(f"{url}, {video_link}, {views}, {likes}, {comments} \n")
        return
    
def read_url_from_file(file_name):
    url_list = []
    with open(file_name, "r") as f:
        urls = f.readlines()
        # add urls in list
        for url in urls:
            url_list.append(url.strip())
    return url_list

def main_executer(url_list, password, username, filename, amount, last_date=7, login_required=False):
    # create instabot object
    bot = Instabot(username, password, login_required=login_required)
    for url in url_list:
        try:
            bot.scrape_url(url, filename, amount=amount, last_date=last_date)
        except Exception as e:
            print("Error in scraping url: ", url)
            # log in error_scrapping.txt file and Date is following format: YYYY-MM-DD HH:MM:SS
            with open("error_scrapping.txt", "a+") as f:
                f.write(f"DATE  = {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} : {url} : Error: {str(e)}\n")
            pass



if __name__ == "__main__":
    # read url from file
    url_list = read_url_from_file("urls.txt")
    username = 'instragram username'
    password = 'instagram password'
    filename = 'data.csv'
    amount = 1
    last_date = 7
    print(f"STSRTTING URL LIST = {url_list}")
    # if you are getting 401 or some weird  Client error, make LOGIN_REQUIRED = True
    LOGIN_REQUIRED = False
    main_executer(url_list, password, username, filename, amount, last_date, login_required= LOGIN_REQUIRED)

    
