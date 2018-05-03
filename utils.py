from instabot import API
import sqlite3
from itertools import cycle

# inits

def init_db():
    conn = sqlite3.connect('phystechtv.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS instagram_users (
          user_id INTEGER PRIMARY KEY,
          username TEXT NOT NULL, fullname TEXT, biography TEXT,
          is_private BOOL NOT NULL, is_business BOOL,
          follower_count INT, following_count INT, media_count INT, usertags_count INT,
          mean_likes FLOAT, mean_comments FLOAT,
          mipt_proven BOOL,
          last_update TIMESTAMP default CURRENT_TIMESTAMP
        );
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS instagram_credentials (
          username TEXT PRIMARY KEY,
          password TEXT NOT NULL,
          is_main_account BOOL default FALSE
        );
    ''')
    conn.commit()

# instagram api and credentials

def add_instagram_credentials(username, password, main=False):
    api = API()
    if api.login(username=username, password=password):
        conn = sqlite3.connect('phystechtv.db')
        c = conn.cursor()
        c.execute('REPLACE INTO instagram_credentials VALUES (?,?,?)',
              [username, password, not not main])
        conn.commit()
        return True
    return False

def get_api(username, password):
    api = API()
    api.login(username=username, password=password)
    return api

def get_main_api():
    conn = sqlite3.connect('phystechtv.db')
    c = conn.cursor()
    c.execute('''SELECT username, password FROM instagram_credentials 
                 WHERE is_main_account = TRUE ''')
    resp = c.fetchall()
    if len(resp) == 0:
        return None
    return get_api(resp[0][0], resp[0][1])

def get_all_instagram_credentials():
    conn = sqlite3.connect('phystechtv.db')
    c = conn.cursor()
    c.execute('''SELECT username, password FROM instagram_credentials''')
    return list(set(c.fetchall()))

def get_apis():
    creds = get_all_instagram_credentials()
    return cycle([get_api(u,p) for u, p in creds])