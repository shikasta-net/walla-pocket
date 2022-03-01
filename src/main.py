#! /usr/bin/env python3

from collections import OrderedDict
import argparse
import feedparser
import json
import pocket
import re

arguments = argparse.ArgumentParser(description='Wallabag to Pocket unread article sync.')
arguments.add_argument('--wallabag-host', type=str, default='app.wallabag.it', help='The Wallabag hostname')
arguments.add_argument('--wallabag-user', type=str, help='The Wallabag user')
arguments.add_argument('--wallabag-secret', type=str, help='The Wallabag user\'s secret')
arguments.add_argument('--pocket-key', type=str, help='The Pocket API key')
arguments.add_argument('--pocket-secret', type=str, help='The Pocket API secret/token')
arguments.add_argument('--purge', action='store_true', help='Completely remove unread items from Pocket.')

config = arguments.parse_args()

pocket_connection = pocket.Pocket(
  consumer_key=config.pocket_key,
  access_token=config.pocket_secret
)

def __wallabag_unread_articles():
  wallabag_feed = feedparser.parse(F"https://{config.wallabag_host}/feed/{config.wallabag_user}/{config.wallabag_secret}/unread")
  articles = OrderedDict()
  for entry in wallabag_feed.entries:
    articles[__standardise_url(entry.links[0]['href'])] = entry
  return articles

def __pocket_unread_articles():
  try:
    pocket_feed = pocket_connection.retrieve(state='unread')['list']
  except pocket.PocketException as e:
    print(e.message)
  unread_articles = pocket_feed.values() if pocket_feed else []
  articles = OrderedDict()
  for entry in unread_articles:
    articles[__standardise_url(entry['given_url'])] = entry
  return articles

def __standardise_url(url):
  return re.sub(r'^https?://(?P<url>.*?)/?$', r'https://\g<url>', url)

def __remove_unread_articles_from_pocket():
  try:
    pocket_feed = pocket_connection.retrieve(state='unread')['list']
    unread_articles = pocket_feed.values() if pocket_feed else []
    for entry in unread_articles:
      pocket_connection.delete(entry['item_id'])
    pocket_connection.commit()
  except pocket.PocketException as e:
    print(e.message)

def __archive_missing_articles(urls_to_archive, pocket_articles):
  for url in urls_to_archive:
    pocket_connection.archive(pocket_articles[url]['item_id'])
  try:
    pocket_connection.commit()
  except pocket.PocketException as e:
    print(e.message)

def __add_new_articles(urls):
  for url in urls:
    pocket_connection.add(url)

if __name__ == "__main__":
  if config.purge:
    print("Removing unread")
    __remove_unread_articles_from_pocket()

  wallabag_articles = __wallabag_unread_articles()
  pocket_articles = __pocket_unread_articles()

  __archive_missing_articles(pocket_articles.keys() - wallabag_articles.keys(), pocket_articles)

  urls_to_add = [url for url in wallabag_articles.keys() if url not in pocket_articles]
  __add_new_articles(reversed(urls_to_add))
