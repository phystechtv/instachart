from random import sample
from collections import Counter

from utils import *
from instaget import *

SAMPLE_SIZE = 10
ITERATIONS = 10

apis = get_apis()
init_db()

mipt_users = extract_mipt_users_info()
# if not mipt_users:
#     # for the first launch
#     proven_users = ["ohld", "caffeinum", "mipt_physchem", "mipt.ru", "mipt_bm", "mipt_drec", "cheer_delta",
#                    "belka_fbmf", "alphadance_cheer_mipt", "faki_mipt", "lavash_mipt", "miptculture",
#                    "mipt_profkom", "kvn_mipt", "spektr_mipt", "miptstream_ru", "__hazerblu", "fiztehradio"]
#     _ = [get_user_info(next(apis), username=u) for u in proven_users]
#     mipt_users = [{"user_id": get_user_id(next(apis), username=u)} for u in proven_users]
#     _ = [make_user_mipt(u["user_id"]) for u in mipt_users]

for _ in range(ITERATIONS):
    all_followings = []
    for user in sample(mipt_users, SAMPLE_SIZE):
        _ = get_user_info(next(apis), user_id=user["user_id"])
        followings = get_user_followings(next(apis), user_id=user["user_id"])
        if followings:
            all_followings.extend(followings)
        sleep(5)

    mipt_users_ids = set([u["user_id"] for u in mipt_users])
    value_counts = Counter([uid for uid in all_followings if uid not in mipt_users_ids])
    for user_id, count in value_counts.items():
        if count >= SAMPLE_SIZE / 2:
            _ = get_user_info(next(apis), user_id=user_id)
            _ = make_user_mipt(user_id)

    sleep(60 * 5)