#! /usr/bin/env python3

import argparse
import feedparser

arguments = argparse.ArgumentParser(description='Wallabag to Pocket unread article sync.')
arguments.add_argument('--host', type=str, default='app.wallabag.it', help='The Wallabag hostname')
arguments.add_argument('--user', type=str, help='The Wallabag user')
arguments.add_argument('--secret', type=str, help='The Wallabag user\'s secret')

config = arguments.parse_args()

wallabag_feed = feedparser.parse(F"https://{config.host}/feed/{config.user}/{config.secret}/unread")
