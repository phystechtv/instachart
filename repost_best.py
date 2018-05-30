import os
from utils import *
from instaget import *

HASHTAGS = "#МФТИ#MIPT#ФИЗТЕХ"

DOWNLOADED_MEDIA_FOLDER = "photos/"

if not os.path.exists(DOWNLOADED_MEDIA_FOLDER):
    os.makedirs(DOWNLOADED_MEDIA_FOLDER)

def get_posted_media_ids():
    posted_medias = extract_posted_medias()
    if not posted_medias:
        return []
    return [m["original_media_id"] for m in posted_medias]

def download_img(url, path):
    import requests

    img_data = requests.get(url).content
    with open(path, 'wb') as handler:
        handler.write(img_data)

def main():
    api = get_main_api()

    top_medias = extract_scores()
    top_media = top_medias[0]

    if top_media["media_id"] in get_posted_media_ids():
        print("Media {} was uploaded earlier".format(top_media["media_id"]))
        return False

    media_info = extract_media_info(top_media["media_id"])
    img_path = os.path.join(DOWNLOADED_MEDIA_FOLDER, str(media_info["media_id"]) + ".jpg")
    download_img(media_info["link"], path=img_path)

    text = "Крутое фото от @{}!  {}  -----------------------  {}".format(media_info["author_username"], media_info["caption"], HASHTAGS)

    if api.upload_photo(img_path, text):
        make_media_downloaded(media_id=media_info["media_id"],
                              author_id=media_info["author_id"],
                              caption=text)
        return True


if __name__ == "__main__":
    print(main())

