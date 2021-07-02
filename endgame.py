from db_part import *
from visual_part import *
from manual_start import *
import argparse
import sys


class splitAction(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        dick = {}
        for i in values:
            buff = i.split("=")
            if len(buff) == 2:
                dick[buff[0]] = buff[1]
            else:
                sys.stderr.write("Usage [key=value]\n")
        setattr(namespace, self.dest, dick)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--gui", help="launch GUI", action="store_true")
    parser.add_argument("--history", help="show/clear history", type=str, choices=["show", "clear"])
    parser.add_argument("--method", help="select the HTTP request method", type=str,
                        choices=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'], default='GET')
    parser.add_argument("--endpoint", help="specify the endpoint URL", type=str)
    parser.add_argument("--params", help="specify query parameters", nargs='*', action=splitAction)
    parser.add_argument("--header", help="specify request headers with argument", nargs='*', action=splitAction)
    parser.add_argument("--body", help="specify request body with argument", nargs='*', action=splitAction)
    parser.add_argument("--auth", help="specify username and password", type=str, nargs=2)
    parser.add_argument("--yaml", help="specify type of view", action="store_true")

    args = parser.parse_args()
    myDb = workWithDb("endgameDatabase", "root", "root")
    if args.gui:
        visual_start(db=myDb)
    elif args.history:
        if args.history == 'show':
            myDb.history_show()
        elif args.history == 'clear':
            myDb.history_clear()
    else:
        manual_start(db=myDb, url=args.endpoint, method=args.method, params=args.params,
                     headers=args.header, auth=args.auth, body=args.body, trig=args.yaml)

