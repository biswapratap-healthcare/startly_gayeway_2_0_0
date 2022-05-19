import json
import pickle

from sql import SqlDatabase
import concurrent.futures
import requests


sqldb = SqlDatabase()


def is_image_selected(image_arr, style):
    numpy_arr = pickle.loads(image_arr)
    r = requests.post(sqldb.config['filter_host'] + ':' +
                      sqldb.config['filter_port'] + '/filter_image?' +
                      'style=' + style +
                      'image=' + image_arr)
    d = json.loads(r.text)
    return d['result']


def search_image_fn(search_string, style):
    image_arrs = list(set([e[0] for e in sqldb.fetch_n_image_arrs(n=10)]))
    result = list()
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_image_arr = {executor.submit(
            is_image_selected, image_arr, style): image_arr for image_arr in image_arrs}
        for future in concurrent.futures.as_completed(future_to_image_arr):
            image_arr = future_to_image_arr[future]
            try:
                res = future.result()
                if res == "1":
                    result.append(image_arr)
            except Exception as exc:
                print(exc)
    return result
