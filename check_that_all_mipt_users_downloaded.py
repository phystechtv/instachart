from tqdm import tqdm

from utils import *
from instaget import *

apis = get_apis()

mipt_users = extract_mipt_users_info()
for user_info in tqdm(mipt_users[::-1]):
    if not get_user_info(next(apis), user_id=user_info["user_id"]):
        sleep(10)
    sleep(1)