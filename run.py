from utils import *
from instaparse import *

init_db()

add_instagram_credentials("login", "password", 1)

apis = get_apis()

download_user(next(apis), username="ohld")