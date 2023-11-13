#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : slack_webhook.py
# Author            : nattoujam <Public.kyuuanago@gmail.com>
# Date              : 2023 11/13
# Last Modified Date: 2023 11/14
# Last Modified By  : nattoujam <Public.kyuuanago@gmail.com>

import requests
import json


def post(url: str, channel: str, bot_name: str, message: str) -> bool:
    headers = {
        'Content-Type': 'application/json',
    }
    payload = {
        'channel': f'#{channel}',
        'username': bot_name,
        'text': message,
    }
    res = requests.post(url, data=json.dumps(payload), headers=headers)

    if res.status_code == 200:
        print(f'Success!: {res.status_code}')
        return True
    else:
        print(f'Failed: {res.status_code}')
        return False
