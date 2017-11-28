#!/usr/env/bin/python3
# -*- coding: utf8 -*-


import json
import re


from os import listdir
from os.path import isfile, join


def dialogs_getter(history):
    dialogs = []
    in_dialog = False
    for message in history:
        if message['out'] == 1 and message['body'].find('Собеседник найден, общайтесь!') > -1:
            in_dialog = True
            dialog = []
        elif in_dialog:
            if message['out'] == 1 and (message['body'].find('Собеседник покинул диалог') > -1 or message['body'].find('Диалог завершен') > -1):
                in_dialog = False
                dialogs.append(dialog)
            else:
                dialog.append({'text': message['body'], 'income': message['out']})

    return dialogs

if __name__ == "__main__":
    histories_path = 'histories'
    dialogs_path = 'divided_dialogs'
    group_ids = [int(re.split('\.', f)[0]) for f in listdir(histories_path) if isfile(join(histories_path, f))]

    for group_id in group_ids:
        print('for group', group_id)
        with open('{}/{}.json'.format(histories_path, group_id), 'r') as f, \
             open('{}/{}.json'.format(dialogs_path, group_id), 'w') as res_f:
            for line in f:
                user_history = json.loads(line[:-1])
                user_id = user_history.keys().__iter__().__next__()

                dialogs = dialogs_getter(user_history[user_id])
                res_f.write(json.dumps({'user_id': user_id, 'dialogs': dialogs}))
                res_f.write('\n')
