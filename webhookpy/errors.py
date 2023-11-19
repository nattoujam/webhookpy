#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : errors.py
# Author            : nattoujam <Public.kyuuanago@gmail.com>
# Date              : 2023 11/19
# Last Modified Date: 2023 11/19
# Last Modified By  : nattoujam <Public.kyuuanago@gmail.com>

def reserved(name: str) -> str:
    """予約語が指定されたとき"""

    return f'{name} reserved'


def duplicate_name(name: str) -> str:
    """nameが重複しているとき"""

    return f'{name} exists'


def not_exists_name(name: str) -> str:
    """nameが存在しないとき"""

    return f'{name} not exists'


def config_empty() -> str:
    """configファイルが存在しないとき"""

    return 'config not exists'


def default_not_set() -> str:
    """defaultが指定されていないとき"""

    return 'does not set default'
