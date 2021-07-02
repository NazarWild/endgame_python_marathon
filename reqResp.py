import requests as req
import sys
from time import time
from db_part import *
import json
import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def print_stdout(string):
    sys.stdout.write(f"INFO | {string}.\n")


def print_stderr(err_mess):
    sys.stderr.write(f"ERROR | {err_mess}.\n")


def retData(resp, sec, db, url, method, params=None, headers=None, auth=None, body=None, trig=False):
    req_id = db.insertIntoRequests(url=url, h_method=method, status=resp.status_code,
                                   body=body, params=params, headers=headers)
    print_stdout(f"{resp}")
    if resp.status_code != 200:
        print_stderr("Request failed")
        db.insertIntoResponses(req_id, resp.status_code)
    else:
        print_stdout(f"---Got response 200 OK in {round(sec, 3)} seconds---")
        print_stdout("---Response body---")
        db.insertIntoResponses(req_id, resp.status_code, str(resp.json()))
        if trig:
            yaml_obj = yaml.safe_load(resp.text)
            return yaml_obj
        else:
            json_obj = json.loads(resp.text)
            return json_obj


def get_request(db, url, method, params=None, headers=None, auth=None, body=None, trig=False):
    try:
        time_now = time()
        resp = req.get(url, params=params, headers=headers)
        sec = time() - time_now
        return retData(resp, sec, db, resp.url, method, params, headers, auth, body, trig)
    except Exception as err:
        print_stderr(f"{err}")
        return None


def post_request(db, url, method, params=None, headers=None, auth=None, body=None, trig=False):
    try:
        time_now = time()
        resp = req.post(url, data=body, params=params, headers=headers)
        sec = time() - time_now
        return retData(resp, sec, db, resp.url, method, params, headers, auth, body, trig)
    except Exception as err:
        print_stderr(f"{err}")
        return None


def put_request(db, url, method, params=None, headers=None, auth=None, body=None, trig=False):
    try:
        time_now = time()
        resp = req.put(url, data=body, params=params, headers=headers)
        sec = time() - time_now
        req_id = db.insertIntoRequests(url=resp.url, h_method=method, status=resp.status_code,
                                       body=body, params=params, headers=headers)
        print_stdout(f"{resp}")
        if resp.status_code != 200:
            print_stderr("Request failed")
            db.insertIntoResponses(req_id, resp.status_code)
        else:
            print_stdout(f"---Got response 200 OK in {round(sec, 3)} seconds---")
            print_stdout("---Response body---")
            db.insertIntoResponses(req_id, resp.status_code, str(resp.json()))
            if trig:
                yaml_obj = yaml.safe_load(resp.text)
                yaml_res = yaml.dump(yaml_obj["form"])
                return yaml_res
            else:
                json_obj = json.loads(resp.text)
                json_result = json.dumps(json_obj["form"], indent=4)
                return json_result
    except Exception as err:
        print_stderr(f"{err}")
        return None


def patch_request(db, url, method, params=None, headers=None, auth=None, body=None, trig=False):
    try:
        time_now = time()
        resp = req.patch(url, data=body, params=params, headers=headers)
        sec = time() - time_now
        return retData(resp, sec, db, resp.url, method, params, headers, auth, body, trig)
    except Exception as err:
        print_stderr(f"{err}")
        return None


def delete_request(db, url, method, params=None, headers=None, auth=None, body=None, trig=False):
    try:
        time_now = time()
        resp = req.delete(url, header=headers, data=body, params=params)
        sec = time() - time_now
        return retData(resp, sec, db, resp.url, method, params, headers, auth, body, trig)
    except Exception as err:
        print_stderr(f"{err}")
        return None
