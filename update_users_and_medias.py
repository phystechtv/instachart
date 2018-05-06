from tqdm import tqdm

from utils import *
from instaget import *

apis = get_apis()

mipt_users = extract_mipt_users_info()

random.shuffle(mipt_users)
for user_info in tqdm(mipt_users):
    if not download_user_info(next(apis), user_id=user_info["user_id"]):
        sleep(120)
    if not download_user_medias(next(apis), user_id=user_info["user_id"]):
        sleep(120)
    sleep(60)