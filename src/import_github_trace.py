#!/usr/bin/env python
import argparse
import datetime as dt
import getpass
import json
import sys
import time

try:
    import requests
except ImportError:
    print("""Install requests with the following command:
        python -m pip install requests""", file=sys.stderr)
    exit(-1)

def main():
    parser = argparse.ArgumentParser(description='Import issues and comments from a github repo.')
    parser.add_argument('repo', metavar='REPO',
                        help=f"the repository to query (e.g. pchampin/sophia_rs)")
    parser.add_argument('--out', '-o',
                        help="output file (otherwise, will print to stdout)")
                        # NB: do not use argparse.FileType here,
                        # because we want to allow the same file in -o and -p
    parser.add_argument('--prev', '-p', metavar='PREV',
                        help="previous file (used to retrieved only new items)")
    parser.add_argument('--auth', '-a', metavar='TOKN',
                        help=f"authorization token, to get higher quotas (see https://github.com/settings/tokens)")
    parser.add_argument('--quiet', '-q',
                        action='store_true',
                        help="do not print information messages on stderr")
    args = parser.parse_args()

    global QUIET
    QUIET = args.quiet
    headers = {}
    if args.auth:
        headers['Authorization'] = f"token {args.auth}"
    base = "https://api.github.com/repos/"
    buffer = []
    filter = make_filter(args.prev)
    try:
        get_all_pages(base + args.repo + "/issues?per_page=100&state=all" + filter, headers, buffer)
        get_all_pages(base + args.repo + "/issues/comments?per_page=100" + filter, headers, buffer)
    except MyException as ex:
        eprint(ex)
        exit(-2)
    except KeyboardInterrupt:
        exit(-3)
    if args.out:
        with open(args.out, 'w') as f:
            json.dump(buffer, f, indent='  ')
    else:
        json.dump(buffer, sys.stdout, indent='  ')

QUIET = False
ONE_SEC = dt.timedelta(seconds=1)

def make_filter(filename):
    if filename is None:
        return ""
    try:
        with open(filename) as f:
            data = json.load(f)
        created = [ i.get('created_at') for i in data ]
        updated = [ i.get('updated_at') for i in data ]
        dates = [ i for i in created+updated if i is not None ]
        since = max(dates)
        iso = since[:19]
        tz = since[19:]
        since = dt.datetime.fromisoformat(iso) + ONE_SEC
        since = since.isoformat() + tz
        return f"&since={since}"
    except Exception as ex:
        if not QUIET:
            eprint(f"Error parsing {filename}, no filter applied")
        return ""

def get_all_pages(url, headers, buffer):
    while url is not None:
        if not QUIET:
            eprint(url)
        res = requests.get(url, headers=headers)
        if res.status_code // 100 != 2:
            raise MyException(res)
        try:
            data = res.json()
            if not isinstance(data, list):
                data = None
        except ValueError:
            data = None
        if data is None:
            raise MyException("Response was not JSON:\n" + res.text)
        buffer.extend(data)

        url = res.links.get('next', {}).get('url')

def eprint(*args, **kw):
    if 'file' in kw:
        raise TypeError("'file' is an invalid keyword argument for eprint()")
    kw['file'] = sys.stderr
    print(*args, **kw)

class MyException(Exception):
    def __init__(self, response_or_message):
        if hasattr(response_or_message, 'status_code'):
            res = response_or_message
            super().__init__("{} {}\n{}".format(
                res.status_code,
                res.reason,
                res.text,
            ))
        else:
            super().__init__(response_or_message)

main()
