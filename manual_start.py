from reqResp import *
import re


def pretty(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent + 1)
        else:
            print('\t' * (indent + 1) + str(value))


def manual_start(db, url=None, method=None, params=None, headers=None, auth=None, body=None, trig=False):
    url_pattern = "^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$"
    if url and re.search(url_pattern, url):
        if method == 'GET':
            data = get_request(db, url, method, params, headers, auth, trig)
        elif method == 'POST':
            data = post_request(db, url, method, params, headers, auth, body, trig)
        elif method == 'PUT':
            data = put_request(db, url, method, params, headers, auth, body, trig)
        elif method == 'PATCH':
            data = patch_request(db, url, method, params, headers, auth, body, trig)
        elif method == 'DELETE':
            data = delete_request(db, url, method, params, headers, auth, body, trig)
        if trig:
            yaml_res = yaml.dump(data)
        else:
            json_result = json.dumps(data, indent=4)
        return data
