#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : command.py
# Author            : nattoujam <Public.kyuuanago@gmail.com>
# Date              : 2023 11/13
# Last Modified Date: 2023 11/14
# Last Modified By  : nattoujam <Public.kyuuanago@gmail.com>

import click
from pathlib import Path
from . import slack_webhook as wh
from .config import Config

CONFIG_DIR = Path('/etc/nattoujam/webhookpy')
CONFIG_USER_DIR = Path.home().joinpath('.config', 'nattoujam', 'webhookpy')
CONFIG_FILE = 'config.yml'
CONFIG_PATH = CONFIG_DIR.joinpath(CONFIG_FILE)
CONFIG_USER_PATH = CONFIG_USER_DIR.joinpath(CONFIG_FILE)


def reserved_error(name: str):
    print(f'{name} reserved')


def duplicate_name_error(name: str):
    print(f'{name} exists')


def not_exists_name_error(name: str):
    print(f'{name} not exists')


def config_empty_error():
    print('config not exists')


def default_not_set_error():
    print('does not set default')


@click.group()
def webhook():
    pass


@webhook.command()
@click.argument('name')
@click.argument('url')
@click.argument('channel')
@click.argument('bot_name')
@click.option('--default', '-d', '_default', default=False, is_flag=True)
def add(name: str, url: str, channel: str, bot_name: str, _default: bool):
    config = Config.load(CONFIG_USER_PATH)
    if name in config.reserved_words:
        reserved_error(name)
        return

    if name in config:
        duplicate_name_error(name)
        return

    if _default:
        config.add(name, url, channel, bot_name) \
              .set_default(name) \
              .dump(CONFIG_USER_PATH)
    else:
        config.add(name, url, channel, bot_name) \
              .dump(CONFIG_USER_PATH)


@webhook.command()
@click.argument('name')
def setdefault(name: str):
    config = Config.load(CONFIG_USER_PATH)
    if config.empty():
        config_empty_error()
        return

    if name not in config:
        not_exists_name_error(name)
        return

    config.set_default(name) \
          .dump(CONFIG_USER_PATH)


@webhook.command()
@click.argument('name')
def remove(name: str):
    config = Config.load(CONFIG_USER_PATH)
    if name not in config:
        not_exists_name_error(name)
        return

    config.remove(name) \
          .dump(CONFIG_USER_PATH)


@webhook.command()
def list():
    config = Config.load(CONFIG_USER_PATH)
    if config.empty():
        config_empty_error()
        return

    print(f'*{config.default}')
    for hook in config.hooks:
        print(f'{hook.name}.url = {hook.url}')
        print(f'{hook.name}.channel = {hook.channel}')
        print(f'{hook.name}.bot_name = {hook.bot_name}')


@webhook.command()
@click.argument('message', nargs=1)
@click.option('--name', '-n', 'name')
def post(message: str, name: str = None):
    config = Config.load(CONFIG_USER_PATH)

    if name is None:
        if config.default is None:
            default_not_set_error()
            return
        else:
            name = config.default

    hook = config.hook(name)
    if hook is None:
        not_exists_name_error(name)
        return
    else:
        wh.post(hook.url, hook.channel, hook.bot_name, message)
