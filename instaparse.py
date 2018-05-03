import logging
import sqlite3
from statistics import mean

logger = logging.getLogger('instagram_parsing')
logger.setLevel(logging.DEBUG)

def get_user_id(api, username):
    if api.search_username(username):
        user_data = api.last_json["user"]
        user_id = str(user_data["pk"])
        return user_id
    return None

def get_user_medias(api, user_id):
    if api.get_user_feed(user_id):
        return api.last_json["items"]

def download_user(api, username=None, user_id=None):
    if username is None and user_id is None:
        logger.debug("Can't download user: no user_id or username specified")
        return False

    if user_id is None:
        user_id = get_user_id(api, username)

    if user_id is None:  # can't find that user
        return False

    if not api.get_username_info(user_id):
        return False
    user_info = api.last_json["user"]
    user_info_dict = {
        "username": user_info["username"],
        "user_id": user_info["pk"],
        "fullname": user_info["full_name"],
        "biography": user_info["biography"],
        "follower_count": user_info["follower_count"],
        "following_count": user_info["following_count"],
        "usertags_count": user_info["usertags_count"],
        "media_count": user_info["media_count"],
        "is_private": user_info["is_private"],
        "is_business": user_info["is_business"],
    }

    medias = get_user_medias(api, user_id)
    user_info_dict["mean_likes"] = mean([m["like_count"] for m in medias])
    user_info_dict["mean_comments"] = mean([m["comment_count"] for m in medias])

    conn = sqlite3.connect('phystechtv.db')
    c = conn.cursor()

    columns = ', '.join(user_info_dict.keys())
    placeholders = ':' + ', :'.join(user_info_dict.keys())
    c.execute('REPLACE INTO instagram_users (%s) VALUES (%s)' % (columns, placeholders),
              user_info_dict)
    conn.commit()
    return True