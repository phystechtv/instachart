from tqdm import tqdm

from utils import *
from instaget import *

apis = get_apis()

mipt_users_id = extract_mipt_users()
for user_id in tqdm(mipt_users_id[::-1]):
    if get_user_info(next(apis), user_id=user_id):
        sleep(1)