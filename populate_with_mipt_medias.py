from tqdm import tqdm

from utils import *
from instaget import *

apis = get_apis()

mipt_users = extract_mipt_users()

random.shuffle(mipt_users)
for user_id in tqdm(mipt_users):
    if download_user_medias(next(apis), user_id=user_id):
        sleep(60)