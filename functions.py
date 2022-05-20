import base64
import json
import pickle

from sql import SqlDatabase
import concurrent.futures
import requests
from pyunsplash import PyUnsplash


sqldb = SqlDatabase()
print(sqldb.config)


def is_image_selected(photo_url, style):
    print("Calling Prediction ...")
    req = sqldb.config['filter_host'] + ':' + sqldb.config['filter_port'] + '/filter_image?style=' + style + '&image=' + photo_url
    r = requests.post(req)
    d = json.loads(r.text)
    return d['result']


def search_image_fn(search_string, style):
    pu = PyUnsplash(api_key=sqldb.config["unsplash_access_key"])
    photos = pu.photos(type_='random', count=10, featured=True, query=search_string)
    photo_urls = list()
    for photo in photos.entries:
        photo_urls.append(photo.link_download)
    result = list()
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_photo_urls = dict()
        for photo_url in photo_urls:
            future_to_photo_urls[executor.submit(is_image_selected, photo_url, style)] = photo_url
        for future in concurrent.futures.as_completed(future_to_photo_urls):
            photo_url = future_to_photo_urls[future]
            try:
                res = future.result()
                if res == "1":
                    result.append(photo_url)
            except Exception as exc:
                print(exc)
    return result
