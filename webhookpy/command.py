#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : command.py
# Author            : nattoujam <Public.kyuuanago@gmail.com>
# Date              : 2023 11/13
# Last Modified Date: 2023 11/19
# Last Modified By  : nattoujam <Public.kyuuanago@gmail.com>

from pathlib import Path

import click

from . import errors
from . import slack_webhook as wh
from .config import Config

CONFIG_FILE = 'config.yml'
CONFIG_PATH = Path(click.get_app_dir('webhookpy')).joinpath(CONFIG_FILE)

FAILED = 1


@click.group()
def webhook():
    pass


@webhook.command(short_help='add hook setting')
@click.argument('name', type=click.STRING)
@click.argument('url', type=click.STRING)
@click.argument('channel', type=click.STRING)
@click.argument('bot_name', type=click.STRING)
@click.option('--app', '-a', default='slack', show_default=True, type=click.Choice(['slack']), help='target application')
@click.option('--default', '-d', 'set_default', default=False, is_flag=True, help='set default')
def add(name: str, url: str, channel: str, bot_name: str, app: str, set_default: bool):
    """add hook setting.

    \b
    NAME: hook setting name.
    URL: webhook url generated by an application.
    CHANNEL: channel name to post.
    BOT_NAME: sender name to post.
    """

    if name in Config.reserved_words():
        click.echo(errors.reserved(name), err=True)
        exit(FAILED)

    config = Config.load(CONFIG_PATH)
    if config.empty():
        config.add(name, url, channel, bot_name, app) \
              .set_default(name) \
              .dump(CONFIG_PATH)
    else:
        if name in config:
            click.echo(errors.duplicate_name(name), err=True)
            exit(FAILED)

        if set_default:
            config.add(name, url, channel, bot_name, app) \
                  .set_default(name) \
                  .dump(CONFIG_PATH)
        else:
            config.add(name, url, channel, bot_name, app) \
                  .dump(CONFIG_PATH)


@webhook.command(short_help='set default hook setting')
@click.argument('name', type=click.STRING)
def setdefault(name: str):
    """default hook setting. use post command without --name option.

    NAME: hook setting name to default.
    """

    config = Config.load(CONFIG_PATH)
    if config.empty():
        click.echo(errors.config_empty(), err=True)
        exit(FAILED)

    if name not in config:
        click.echo(errors.not_exists_name(name), err=True)
        exit(FAILED)

    config.set_default(name) \
          .dump(CONFIG_PATH)


@webhook.command(short_help='remove hook setting')
@click.argument('name', type=click.STRING)
def remove(name: str):
    """remove hook setting.

    NAME: hook setting name to remove.
    """

    config = Config.load(CONFIG_PATH)
    if config.empty():
        click.echo(errors.config_empty(), err=True)
        exit(FAILED)

    if name not in config:
        click.echo(errors.not_exists_name(name), err=True)
        exit(FAILED)

    config.remove(name) \
          .dump(CONFIG_PATH)


@webhook.command(short_help='show all hook settings')
def list():
    """show all hook settings."""

    config = Config.load(CONFIG_PATH)
    if config.empty():
        click.echo(errors.config_empty(), err=True)
        exit(FAILED)

    click.echo(f'*{config.default}')
    for hook in config.hooks:
        click.echo(f'{hook.name}.application = {hook.app}')
        click.echo(f'{hook.name}.url = {hook.url}')
        click.echo(f'{hook.name}.channel = {hook.channel}')
        click.echo(f'{hook.name}.bot_name = {hook.bot_name}')

    config.dump(CONFIG_PATH)


@webhook.command(short_help='post message')
@click.argument('message', type=click.STRING)
@click.option('--name', '-n', 'name', type=click.STRING, help='using hook name')
def post(message: str, name: str = None):
    """
    \b
    post message via webhook.
    if '--name' option is omitted, the default setting is used.

    NAME: hook setting to use.
    """

    config = Config.load(CONFIG_PATH)

    if config.empty():
        click.echo(errors.config_empty(), err=True)
        exit(FAILED)

    if name is None:
        if config.default is None:
            click.echo(errors.default_not_set(), err=True)
            exit(FAILED)
        else:
            name = config.default

    hook = config.hook(name)
    if hook is None:
        click.echo(errors.not_exists_name(name), err=True)
        exit(FAILED)
    else:
        wh.post(hook.url, hook.channel, hook.bot_name, message)
