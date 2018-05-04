from tqdm import tqdm

from utils import *
from instaparse import *

apis = get_apis()

mipt_users = get_parsed_mipt_users()

random.shuffle(mipt_users)
for user in tqdm(mipt_users):
    download_user_medias(next(apis), user_id=user["user_id"])
    sleep(60)