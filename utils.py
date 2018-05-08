from instabot import API
import dataset
import random
import time
from itertools import cycle

def sleep(seconds):
    return time.sleep(random.random() * seconds)

# inits

def init_db():
    with dataset.connect() as db:
        db.query('''
            CREATE TABLE IF NOT EXISTS instagram_users (
              user_id VARCHAR(15),
              username TEXT NOT NULL, fullname TEXT, biography TEXT,
              is_private BOOL NOT NULL, is_business BOOL,
              follower_count INT, following_count INT, media_count INT, usertags_count INT,
              mean_likes FLOAT, mean_comments FLOAT,
              last_update TIMESTAMP default CURRENT_TIMESTAMP
            );
        ''')
        db.query('''
            CREATE TABLE IF NOT EXISTS instagram_credentials (
              username TEXT NOT NULL,
              password TEXT NOT NULL,
              is_main_account BOOL default FALSE
            );
        ''')
        db.query('''
            CREATE TABLE IF NOT EXISTS instagram_medias (
              media_id VARCHAR(20),
              author_id VARCHAR(15) NOT NULL,
              author_username TEXT NOT NULL,
              caption TEXT,
              like_count INT,
              comment_count INT, 
              taken_at datetime,          
              media_type INT, 
              lat FLOAT, lng FLOAT,
              link TEXT,
              last_update TIMESTAMP default CURRENT_TIMESTAMP
            );
        ''')
        db.query('''
            CREATE TABLE IF NOT EXISTS instagram_followships (
              follower_id VARCHAR(15), followee_id VARCHAR(15), 
              last_update TIMESTAMP default CURRENT_TIMESTAMP
            );
        ''')
        db.query('''
            CREATE TABLE IF NOT EXISTS instagram_mipt_users (
              user_id VARCHAR(15)
            );
        ''')

# instagram api and credentials

def add_instagram_credentials(username, password, main=False):
    api = API()
    if api.login(username=username, password=password):
        with dataset.connect() as db:
            data = dict(username=username, password=password, is_main_account=main)
            db["instagram_credentials"].delete(username=username)
            db["instagram_credentials"].insert(data, ["username"])
        return True
    return False

def get_api(username, password):
    api = API()
    api.login(username=username, password=password)
    return api

def get_main_api():
    db = dataset.connect()
    main_accounts = db["instagram_credentials"].find(is_main_account=True)
    if len(main_accounts) == 0:
        return None
    if len(main_accounts) > 0:
        pass  # TODO: add warning
    main_account = main_accounts[0]
    return get_api(main_account["username"], main_account["password"])

def get_all_instagram_credentials():
    db = dataset.connect()
    credentials = db["instagram_credentials"]
    if len(credentials) == 0:
        return False
    return credentials

def get_apis():
    creds = get_all_instagram_credentials()
    return cycle([get_api(cred["username"], cred["password"]) for cred in creds])