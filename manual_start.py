from reqResp import *
import re


def manual_start(db, url=None, method=None, params=None, headers=None, auth=None, body=None, trig=False):
    url_pattern = "^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$"
    if url and re.search(url_pattern, url):
        # print(f"params = {params}")
        # print(f"headers = {headers}")
        # print(f"body = {body}")
        if method == 'GET':
            data = get_request(db, url, method, params, headers, auth, trig=trig)
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
            print(yaml_res)
        else:
            json_result = json.dumps(data, indent=4)
            print(json_result)
        return data
