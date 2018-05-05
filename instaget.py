import datetime
import logging
import sqlite3
from statistics import mean

from dbextract import *
from instadownload import *

def get_user_info(api, user_id=None, username=None):
    user_id = get_user_id(api, user_id=user_id, username=username)
    if not user_id:
        return False

    user_info = extract_user_info(user_id=user_id)
    if not user_info:
        if not download_user_info(api, user_id):
            return False
        user_info = extract_user_info(user_id=user_id)

    return user_info

def get_user_followers(api, user_id=None, username=None):
    user_id = get_user_id(api, user_id=user_id, username=username)
    if not user_id:
        return False

    followers = extract_user_followers(user_id)

    user_info = get_user_info(api, user_id=user_id)
    if not user_info:
        return False

    if not followers or len(followers) < 0.9 * user_info["follower_count"]:
        if not download_user_followers(api, user_id):
            return False
        followers = extract_user_followers(user_id)

    return followers

def get_user_followings(api, user_id=None, username=None):
    user_id = get_user_id(api, user_id=user_id, username=username)
    if not user_id:
        return False

    followings = extract_user_followings(user_id)

    user_info = get_user_info(api, user_id=user_id)
    if not user_info:
        return False

    if not followings or len(followings) < 0.9 * user_info["following_count"]:
        if not download_user_followings(api, user_id):
            return False
        followings = extract_user_followings(user_id)

    return followings

def get_user_medias(api, user_id=None, username=None):
    user_id = get_user_id(api, user_id=user_id, username=username)
    if not user_id:
        return False

    medias = extract_user_medias(user_id)
    if not medias:
        if not download_user_medias(api, user_id):
            return False
        medias = extract_user_medias(user_id)

    return medias

def make_user_mipt(user_id):
    conn = sqlite3.connect('phystechtv.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute('REPLACE INTO instagram_mipt_users VALUES (?)', (user_id,))
    conn.commit()




