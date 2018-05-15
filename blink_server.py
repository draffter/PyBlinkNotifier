#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _thread
import asyncio
import json
import time

from mattermostdriver import Driver

from blink import Blink
from config import Config
from http_server import Server


class BlinkServer(object):

    def __init__(self):
        self.config = Config()
        self.not_read_channels = []
        self.blink = Blink()
        self.mattermost_driver = Driver({
            'url': self.config.get_string('MATTERMOST', 'url'),
            'login_id': self.config.get_string('MATTERMOST', 'login_id'),
            'password': self.config.get_string('MATTERMOST', 'password'),
            'verify': self.config.get_bool('MATTERMOST', 'verify'),
            'scheme': self.config.get_string('MATTERMOST', 'scheme'),
            'port': self.config.get_int('MATTERMOST', 'port'),
            'debug': self.config.get_bool('MATTERMOST', 'debug')
        })
        self.server = None
        self.start()

    def start_wbe_server(self, thread_name):
        self.server = Server(self.blink)

    @asyncio.coroutine
    def socket_handler(self, message):
        print(message)
        self.handle_message(json.loads(message))

    def handle_message(self, json_message):
        if 'event' not in json_message:
            return

        if json_message['event'] == "posted":
            self.parse_post(json.loads(json_message['data']['post']))
        elif json_message['event'] == "channel_viewed":
            self.mark_chanel_as_read(json_message['data']['channel_id'])

    def parse_post(self, post_data):
        try:
            self.not_read_channels.index(post_data['channel_id'])
        except ValueError:
            self.not_read_channels.append(post_data['channel_id'])
        self.blink.start_unread_blink()

    def mark_chanel_as_read(self, channel_id):
        try:
            index = self.not_read_channels.index(channel_id)
            del self.not_read_channels[index]
            if len(self.not_read_channels) == 0:
                self.blink.stop_unread_blinking()
        except ValueError:
            pass

    def start(self):
        _thread.start_new_thread(self.start_wbe_server, ('webserver',))
        # todo: polaczenie z gitlabem - nowy MR
        self.mattermost_driver.login()
        while True:
            try:
                self.mattermost_driver.init_websocket(self.socket_handler)
            except Exception:
                print('Reconnecting to websocket')
                time.sleep(60)


if __name__ == '__main__':
    BlinkServer()
