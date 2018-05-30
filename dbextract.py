from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import dataset

def extract_user_info(user_id=None, username=None):
    if user_id is None and username is None:
        return False

    if user_id is not None:
        with dataset.connect() as db:
            result = list(db["instagram_users"].find(user_id=user_id))
    else:
        with dataset.connect() as db:
            result = list(db["instagram_users"].find(username=username))

    if len(result) == 0:
        # нет записей в бд
        return False

    if len(result) > 1:
        # что-то странно
        pass

    return result[0]

def extract_user_followers(user_id):
    with dataset.connect() as db:
        followers = list(db["instagram_followships"].find(followee_id=user_id))

    if len(followers) == 0:
        return False

    return [f["follower_id"] for f in followers]


def extract_user_followings(user_id):
    with dataset.connect() as db:
        followees = list(db["instagram_followships"].find(follower_id=user_id))

    if len(followees) == 0:
        return False

    return [f["followee_id"] for f in followees]

def extract_user_medias(user_id):
    with dataset.connect() as db:
        medias = list(db["instagram_medias"].find(author_id=user_id))
    if len(medias) == 0:
        return False

    return medias

def extract_media_info(media_id):
    with dataset.connect() as db:
        media = list(db["instagram_medias"].find(media_id=media_id))
    if len(media) == 0:
        return False

    return media[0]

def extract_posted_medias():
    with dataset.connect() as db:
        medias = list(db["instagram_posted_medias"])
    if len(medias) == 0:
        return False

    return medias

def extract_mipt_users_info():
    with dataset.connect() as db:
        users = list(db.query('''SELECT * FROM instagram_mipt_users INNER JOIN instagram_users
               ON instagram_users.user_id = instagram_mipt_users.user_id WHERE is_private = 0'''))

    if len(users) == 0:
        return False

    return users

def extract_mipt_users():
    with dataset.connect() as db:
        mipt_users = list(db["instagram_mipt_users"])
    if len(mipt_users) == 0:
        return False

    return [u[0] for u in mipt_users]

def extract_scores():
    with dataset.connect() as db:
        scores = list(db.query('''
            SELECT
              likes * comments * likes * comments * mipt_followers_part as score,
              author_username as username, likes, comments, mipt_followers_part, caption, link, last_update, media_id
            FROM mipt_ratings
            ORDER BY score DESC
        '''))
    for i, score in enumerate(scores):
        for float_column in ["likes", "comments", "score", "mipt_followers_part"]:
            scores[i][float_column] = float(scores[i][float_column])
        scores[i]["last_update"] = str(scores[i]["last_update"])
        scores[i]["place"] = i + 1
    return scores

def extract_users_with_old_media_updates():
    with dataset.connect() as db:
        users = list(db.query('''
            select distinct author_id as user_id, instagram_medias.last_update
            from instagram_medias 
            left join instagram_users on instagram_users.user_id = instagram_medias.author_id
            where author_id in (select user_id from instagram.instagram_mipt_users)
            AND is_private is FALSE 
            ORDER BY last_update
        '''))
    return [u["user_id"] for u in users]