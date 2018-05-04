from utils import *
from instaparse import *
from random import sample
from collections import Counter

SAMPLE_SIZE = 10

apis = get_apis()

mipt_users = get_parsed_mipt_users()

all_followings = []
mipt_users_sample = sample(mipt_users, SAMPLE_SIZE)
for user in mipt_users_sample:
    followings = next(apis).get_total_followings(user["user_id"])
    if followings:
        all_followings.extend([f["pk"] for f in followings])
    sleep(2)

mipt_users_ids = set([u["user_id"] for u in mipt_users])
value_counts = Counter([uid for uid in all_followings if uid not in mipt_users_ids])
for user_id, count in value_counts.items():
    if count >= SAMPLE_SIZE / 2:
        add_mipt_user(next(apis), user_id=user_id)