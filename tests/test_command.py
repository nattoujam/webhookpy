#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : test_command.py
# Author            : nattoujam <Public.kyuuanago@gmail.com>
# Date              : 2023 11/19
# Last Modified Date: 2023 11/19
# Last Modified By  : nattoujam <Public.kyuuanago@gmail.com>

from click.testing import CliRunner
from webhookpy import errors
from webhookpy.command import FAILED, webhook
from webhookpy.config import RESERVED_WORDS, Config

TEST_NAME = 'test'
TEST_URL = 'http://example.com/'
TEST_CHANNEL = 'test_channel'
TEST_BOT = 'test_bot'
TEST_CONFIG = {
    'default': TEST_NAME,
    TEST_NAME: {
        'app': 'slack',
        'url': TEST_URL,
        'channel': TEST_CHANNEL,
        'bot_name': TEST_BOT,
    }
}


def get_test_config() -> Config:
    return Config(dict(**TEST_CONFIG))


def describe_add():
    def it_config_file_not_exists(mocker):
        mocker.patch('webhookpy.config.Config.load', return_value=Config({}))

        r = CliRunner().invoke(webhook, args=['add', 'test', 'http://example.com/', 'test_channel', 'test_bot'])

        assert r.exit_code == 0

    def it_append_setting(mocker):
        name = 'test2'
        url = 'http://example.com/2/'
        channel = 'test2_channel'
        bot_name = 'test2_bot'

        mocker.patch('webhookpy.config.Config.load', return_value=get_test_config())
        mocker.patch.object(Config, 'dump')

        r = CliRunner().invoke(webhook, args=['add', name, url, channel, bot_name])

        assert r.exit_code == 0

    def it_set_default(mocker):
        name = 'test2'
        url = 'http://example.com/2/'
        channel = 'test2_channel'
        bot_name = 'test2_bot'

        mocker.patch('webhookpy.config.Config.load', return_value=get_test_config())
        mocker.patch.object(Config, 'dump')

        r = CliRunner().invoke(webhook, args=['add', '-d', name, url, channel, bot_name])

        assert r.exit_code == 0

    def it_set_app(mocker):
        name = 'test2'
        url = 'http://example.com/2/'
        channel = 'test2_channel'
        bot_name = 'test2_bot'

        mocker.patch('webhookpy.config.Config.load', return_value=get_test_config())
        mocker.patch.object(Config, 'dump')

        r = CliRunner().invoke(webhook, args=['add', name, url, channel, bot_name])

        assert r.exit_code == 0

    def it_passing_reserved_name(mocker):
        mocker.patch('webhookpy.config.Config.load', return_value=Config({}))
        mocker.patch.object(Config, 'dump')

        for reserved_name in RESERVED_WORDS:
            r = CliRunner(mix_stderr=False).invoke(
                webhook, args=['add', reserved_name, 'http://example.com/', 'test_channel', 'test_bot'])

            assert r.stderr == errors.reserved(reserved_name) + '\n'
            assert r.exit_code == FAILED

    def it_passing_name_is_exists(mocker):
        duplicate_name = TEST_NAME

        mocker.patch('webhookpy.config.Config.load', return_value=get_test_config())
        mocker.patch.object(Config, 'dump')

        r = CliRunner(mix_stderr=False).invoke(
            webhook, args=['add', duplicate_name, 'http://example.com/', 'test_channel', 'test_bot'])

        assert r.stderr == errors.duplicate_name(duplicate_name) + '\n'
        assert r.exit_code == FAILED


def describe_setdefault():
    def it_success(mocker):
        LOCAL_CONFIG = {
            'default': 'test',
            'test': {
                'app': 'slack',
                'url': 'http://example.com/',
                'channel': 'test_channel',
                'bot_name': 'test bot',
            },
            'test2': {
                'app': 'slack',
                'url': 'http://example.com/',
                'channel': 'test_channel',
                'bot_name': 'test bot',
            }
        }

        mocker.patch('webhookpy.config.Config.load', return_value=Config(LOCAL_CONFIG))
        mocker.patch.object(Config, 'dump')

        r = CliRunner().invoke(webhook, args=['setdefault', 'test2'])

        assert r.exit_code == 0

    def it_config_file_not_exists(mocker):
        mocker.patch('webhookpy.config.Config.load', return_value=Config({}))
        mocker.patch.object(Config, 'dump')

        r = CliRunner(mix_stderr=False).invoke(webhook, args=['setdefault', 'test'])

        assert r.stderr == errors.config_empty() + '\n'
        assert r.exit_code == FAILED

    def it_passing_name_not_exists(mocker):
        not_exists_name = 'test2'

        mocker.patch('webhookpy.config.Config.load', return_value=get_test_config())
        mocker.patch.object(Config, 'dump')

        r = CliRunner(mix_stderr=False).invoke(webhook, args=['setdefault', not_exists_name])

        assert r.stderr == errors.not_exists_name(not_exists_name) + '\n'
        assert r.exit_code == FAILED


def describe_remove():
    def it_config_file_exists(mocker):
        mocker.patch('webhookpy.config.Config.load', return_value=get_test_config())
        mocker.patch.object(Config, 'dump')

        r = CliRunner().invoke(webhook, args=['remove', 'test'])

        assert r.exit_code == 0

    def it_config_file_not_exists(mocker):
        mocker.patch('webhookpy.config.Config.load', return_value=Config({}))
        mocker.patch.object(Config, 'dump')

        r = CliRunner(mix_stderr=False).invoke(webhook, args=['remove', 'test'])

        assert r.stderr == errors.config_empty() + '\n'
        assert r.exit_code == FAILED

    def it_passing_name_not_exists(mocker):
        not_exists_name = 'test2'

        mocker.patch('webhookpy.config.Config.load', return_value=get_test_config())
        mocker.patch.object(Config, 'dump')

        r = CliRunner(mix_stderr=False).invoke(webhook, args=['remove', not_exists_name])

        assert r.stderr == errors.not_exists_name(not_exists_name) + '\n'
        assert r.exit_code == FAILED


def describe_list():
    def it_config_file_exists(mocker):
        mocker.patch('webhookpy.config.Config.load', return_value=get_test_config())

        r = CliRunner().invoke(webhook, args=['list'])

        print(TEST_CONFIG)
        print(get_test_config().d)

        assert r.exit_code == 0
        assert f'*{TEST_NAME}' in r.output
        assert f'{TEST_NAME}.application = slack' in r.output
        assert f'{TEST_NAME}.url = {TEST_URL}' in r.output
        assert f'{TEST_NAME}.channel = {TEST_CHANNEL}' in r.output
        assert f'{TEST_NAME}.bot_name = {TEST_BOT}' in r.output

    def it_config_file_not_exists(mocker):
        mocker.patch('webhookpy.config.Config.load', return_value=Config({}))
        mocker.patch.object(Config, 'dump')

        r = CliRunner(mix_stderr=False).invoke(webhook, args=['list'])

        assert r.stderr == errors.config_empty() + '\n'
        assert r.exit_code == FAILED


def describe_post():
    def it_success(mocker):
        mocker.patch('webhookpy.config.Config.load', return_value=get_test_config())
        mocker.patch('webhookpy.slack_webhook.post', return_value=True)

        r = CliRunner().invoke(webhook, args=['post', 'message'])

        assert r.exit_code == 0

    def it_config_file_not_exists(mocker):
        mocker.patch('webhookpy.config.Config.load', return_value=Config({}))

        r = CliRunner(mix_stderr=False).invoke(webhook, args=['post', 'message'])

        assert r.stderr == errors.config_empty() + '\n'
        assert r.exit_code == FAILED

    def it_default_name_not_exists(mocker):
        not_exists_name = 'test2'
        LOCAL_CONFIG = {
            'default': not_exists_name,
            'test': {
                'app': 'slack',
                'url': 'http://example.com/',
                'channel': 'test_channel',
                'bot_name': 'test bot',
            },
        }

        mocker.patch('webhookpy.config.Config.load', return_value=Config(LOCAL_CONFIG))

        r = CliRunner(mix_stderr=False).invoke(webhook, args=['post', 'message'])

        assert r.stderr == errors.not_exists_name(not_exists_name) + '\n'
        assert r.exit_code == FAILED

    def it_passing_name_not_exists(mocker):
        not_exists_name = 'test2'

        mocker.patch('webhookpy.config.Config.load', return_value=get_test_config())

        r = CliRunner(mix_stderr=False).invoke(webhook, args=['post', 'message', '-n', 'test2'])

        assert r.stderr == errors.not_exists_name(not_exists_name) + '\n'
        assert r.exit_code == FAILED
