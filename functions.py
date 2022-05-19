import base64
import json
import pickle
import numpy

from sql import SqlDatabase
import concurrent.futures
import requests


sqldb = SqlDatabase()
print(sqldb.config)


def is_image_selected(image_str_arr, style):
    print("Calling Prediction ...")
    req = sqldb.config['filter_host'] + ':' + sqldb.config['filter_port'] + '/filter_image?style=' + style + '&image=' + image_str_arr
    r = requests.post(req)
    d = json.loads(r.text)
    return d['result']


def search_image_fn(search_string, style):
    image_arrs = list(set([e[0] for e in sqldb.fetch_n_image_arrs(n=10)]))
    result = list()
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_image_str_arr = dict()
        for image_arr in image_arrs:
            image_str_arr = base64.b64encode(pickle.loads(image_arr)).decode("utf-8")
            future_to_image_str_arr[executor.submit(is_image_selected, image_str_arr, style)] = image_str_arr
        for future in concurrent.futures.as_completed(future_to_image_str_arr):
            image_str_arr = future_to_image_str_arr[future]
            try:
                res = future.result()
                if res == "1":
                    result.append(image_str_arr)
            except Exception as exc:
                print(exc)
    return result
