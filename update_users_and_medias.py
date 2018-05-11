from tqdm import tqdm

from utils import *
from instaget import *

apis = get_apis()

mipt_user_ids = extract_users_with_old_media_updates()

for user_id in tqdm(mipt_user_ids):
    if not download_user_medias(next(apis), user_id=user_id):
        sleep(120)
    sleep(60)
    if not download_user_info(next(apis), user_id=user_id):
        sleep(120)
    sleep(60)