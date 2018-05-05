import datetime
import logging
import sqlite3
from statistics import mean

from dbextract import extract_user_info, extract_user_medias

logger = logging.getLogger('instagram_downloading')
logger.setLevel(logging.DEBUG)

def _download_user_medias(api, user_id):
    if api.get_user_feed(user_id):
        return api.last_json["items"]
    return False

def _download_user_id(api, username):
    if api.search_username(username):
        user_data = api.last_json["user"]
        user_id = str(user_data["pk"])
        return user_id
    return False

def get_user_id(api, user_id=None, username=None):
    if user_id is not None:
        return user_id

    if username is not None:
        user_info = extract_user_info(username=username)
        if user_info and "user_id" in user_info:
            return user_info["user_id"]

    if username is not None:
        return _download_user_id(api, username)

    return False

def download_user_info(api, user_id):
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
        "is_business": user_info["is_business"] if "is_business" in user_info else False,
    }

    if not user_info_dict["is_private"]:
        medias = extract_user_medias(user_id)
        if not medias:
            if not download_user_medias(api, user_id):
                return False
            medias = extract_user_medias(user_id)
        if medias:
            user_info_dict["mean_likes"] = mean([m["like_count"] for m in medias if "like_count" in m])
            user_info_dict["mean_comments"] = mean([m["comment_count"] for m in medias if "comment_count" in m])

    conn = sqlite3.connect('phystechtv.db')
    c = conn.cursor()

    columns = ', '.join(user_info_dict.keys())
    placeholders = ':' + ', :'.join(user_info_dict.keys())
    c.execute('REPLACE INTO instagram_users (%s) VALUES (%s)' % (columns, placeholders),
              user_info_dict)
    conn.commit()
    return True

def download_user_medias(api, user_id):
    medias = _download_user_medias(api, user_id)
    if not medias:
        return False
    media_dicts = [{
        "media_id": m["pk"],
        "author_id": m["user"]["pk"],
        "author_username": m["user"]["username"],
        "caption": m["caption"]["text"] if m["caption"] is not None else "",
        "like_count": m["like_count"] if "like_count" in m else 0,
        "comment_count": m["comment_count"] if "comment_count" in m else 0,
        "taken_at": datetime.datetime.fromtimestamp(m["taken_at"]).strftime('%Y-%m-%d'),
        "media_type": m["media_type"],
        "lat": m["lat"] if "lat" in m else None,
        "lng": m["lng"] if "lng" in m else None,
        "link": m["carousel_media"][0]["image_versions2"]["candidates"][0]["url"] if m["media_type"] == 8 else \
                m["image_versions2"]["candidates"][0]["url"] if m["media_type"] == 1 else None,
    } for m in medias]



    conn = sqlite3.connect('phystechtv.db')
    c = conn.cursor()
    columns = ', '.join(media_dicts[0].keys())
    placeholders = ':' + ', :'.join(media_dicts[0].keys())
    c.executemany('REPLACE INTO instagram_medias (%s) VALUES (%s)' % (columns, placeholders),
                  media_dicts)

    conn.commit()
    return True

def download_user_followers(api, user_id):
    followers = api.get_total_followers(user_id)
    if not followers:
        return False

    conn = sqlite3.connect('phystechtv.db')
    c = conn.cursor()
    c.execute('''DELETE FROM instagram_followships WHERE followee_id = ?''', (user_id,))

    c.executemany('''INSERT INTO instagram_followships VALUES (?, ?, CURRENT_TIMESTAMP)''',
                  [(f["pk"], user_id) for f in followers])
    conn.commit()
    return True

def download_user_followings(api, user_id):
    followings = api.get_total_followings(user_id)
    if not followings:
        return False

    conn = sqlite3.connect('phystechtv.db')
    c = conn.cursor()
    c.execute('''DELETE FROM instagram_followships WHERE follower_id = ?''', (user_id,))

    c.executemany('''INSERT INTO instagram_followships VALUES (?, ?, CURRENT_TIMESTAMP)''',
                  [(user_id, f["pk"]) for f in followings])
    conn.commit()
    return True
