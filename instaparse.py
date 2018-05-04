import datetime
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
    return False

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
        "is_business": user_info["is_business"] if "is_business" in user_info else False,
    }

    if not user_info_dict["is_private"]:
        medias = get_user_medias(api, user_id)
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

def download_user_medias(api, user_id=None, username=None):
    if username is None and user_id is None:
        logger.debug("Can't download user media: no user_id or username specified")
        return False

    if user_id is None:
        user_id = get_user_id(api, username)

    if user_id is None:  # can't find that user
        return False

    medias = get_user_medias(api, user_id)
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
    } for m in medias]

    conn = sqlite3.connect('phystechtv.db')
    c = conn.cursor()
    columns = ', '.join(media_dicts[0].keys())
    placeholders = ':' + ', :'.join(media_dicts[0].keys())
    c.executemany('REPLACE INTO instagram_medias (%s) VALUES (%s)' % (columns, placeholders),
                  media_dicts)

    conn.commit()
    return True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def add_mipt_user(api, username=None, user_id=None):
    if username is None and user_id is None:
        return False
    if not download_user(api, username=username, user_id=user_id):
        return False
    conn = sqlite3.connect('phystechtv.db')
    c = conn.cursor()

    if username is not None:
        c.execute('''
            UPDATE instagram_users
            SET mipt_proven = TRUE
            WHERE username = ?;
        ''', (username,))
        conn.commit()
        return True
    if user_id is not None:
        c.execute('''
            UPDATE instagram_users
            SET mipt_proven = TRUE
            WHERE user_id = ?;
        ''', (user_id,))
        conn.commit()
        return True
    return False

def get_parsed_mipt_users(with_private=False):
    conn = sqlite3.connect('phystechtv.db')
    conn.row_factory = dict_factory
    c = conn.cursor()

    c.execute('''SELECT * FROM instagram_users 
                 WHERE mipt_proven = TRUE''' + " AND is_private != True" * with_private)
    return c.fetchall()
