import datetime
import logging
import sqlite3
from statistics import mean


def dict_factory(cursor, row):
    # for sqlite export as a dict
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def extract_user_info(user_id=None, username=None):
    conn = sqlite3.connect('phystechtv.db')
    conn.row_factory = dict_factory
    c = conn.cursor()

    if user_id is None and username is None:
        return False

    if user_id is not None:
        c.execute('''SELECT * FROM instagram_users WHERE user_id = ?''', (user_id,))
        result = c.fetchall()
    else:
        c.execute('''SELECT * FROM instagram_users WHERE username = ?''', (username,))
        result = c.fetchall()

    if len(result) == 0:
        # нет записей в бд
        return False

    if len(result) > 1:
        # что-то странно
        pass

    return result[0]


def extract_user_followers(user_id):
    conn = sqlite3.connect('phystechtv.db')
    conn.row_factory = dict_factory
    c = conn.cursor()

    c.execute('SELECT follower_id FROM instagram_followships WHERE followee_id = ?', (user_id,))

    followers = c.fetchall()
    if len(followers) == 0:
        return False

    return [f["follower_id"] for f in followers]


def extract_user_followings(user_id):
    conn = sqlite3.connect('phystechtv.db')
    conn.row_factory = dict_factory
    c = conn.cursor()

    c.execute('SELECT followee_id FROM instagram_followships WHERE follower_id = ?', (user_id,))

    followees = c.fetchall()
    if len(followees) == 0:
        return False

    return [f["followee_id"] for f in followees]

def extract_user_medias(user_id):
    conn = sqlite3.connect('phystechtv.db')
    conn.row_factory = dict_factory
    c = conn.cursor()

    c.execute('SELECT * FROM instagram_medias WHERE author_id = ?', (user_id,))
    medias = c.fetchall()
    if len(medias) == 0:
        return False

    return medias

def extract_mipt_users_info():
    conn = sqlite3.connect('phystechtv.db')
    conn.row_factory = dict_factory
    c = conn.cursor()

    c.execute('''SELECT * FROM instagram_mipt_users INNER JOIN instagram_users  
                 ON instagram_users.user_id = instagram_mipt_users.user_id''')
    users = c.fetchall()
    if len(users) == 0:
        return False

    return users

def extract_mipt_users():
    conn = sqlite3.connect('phystechtv.db')
    c = conn.cursor()

    c.execute('SELECT * FROM instagram_mipt_users')
    mipt_users = c.fetchall()
    if len(mipt_users) == 0:
        return False

    return [u[0] for u in mipt_users]