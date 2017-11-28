#!/usr/bin/env/python3
# -*- coding: utf8 -*-


import json
import psycopg2
import re

from tools import get_api, safe_call

from os import listdir
from os.path import isfile, join

db_config = {
    'host': 'localhost',
    'user': 'smartchat',
    'password': 'pa$$word'
}

conn = psycopg2.connect(**db_config)
cursor = conn.cursor()
query = 'select id, token from scopes;'
cursor.execute(query)
tokens = { gid:token for gid, token in cursor.fetchall()}


if __name__ == "__main__":
    mypath = '/root/sphere_project/user_ids'
    group_ids = [int(re.split('\.', f)[0]) for f in listdir(mypath) if isfile(join(mypath, f))]
    for group_id in group_ids:
        api = get_api(access_token=tokens[group_id], v=5.25)
        print('got api for', group_id)
        with open('/root/sphere_project/user_ids/{}.json'.format(group_id), 'r') as f:
            user_ids = json.load(f)
            print('len(user_ids)', len(user_ids))

            with open('json_histories/{}.json'.format(group_id), 'w') as f_res:
                for i, user_id in enumerate(user_ids):
                    print(i, 'for user', user_id)
                    offset = 0
                    iterate = True
                    user_messages = []
                    while iterate:
                        res = safe_call(api.messages.getHistory, count=200, user_id=user_id, rev=1, offset=offset)
                        len_items = len(res['items'])
                        user_messages += res['items']
                        iterate = len_items > 0
                        offset += 200
                    f_res.write('{"' + str(user_id) + '":')
                    f_res.write(json.dumps(user_messages))
                    f_res.write('}\n')
