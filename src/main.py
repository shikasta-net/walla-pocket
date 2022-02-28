#! /usr/bin/env python3

import argparse
import feedparser
import json
import pocket

arguments = argparse.ArgumentParser(description='Wallabag to Pocket unread article sync.')
arguments.add_argument('--host', type=str, default='app.wallabag.it', help='The Wallabag hostname')
arguments.add_argument('--user', type=str, help='The Wallabag user')
arguments.add_argument('--secret', type=str, help='The Wallabag user\'s secret')
arguments.add_argument('--pocket-key', type=str, help='The Pocket API key')
arguments.add_argument('--pocket-secret', type=str, help='The Pocket API secret/token')

config = arguments.parse_args()

pocket_connection = pocket.Pocket(
  consumer_key=config.pocket_key,
  access_token=config.pocket_secret
)

def __wallabag_unread_articles():
  wallabag_feed = feedparser.parse(F"https://{config.host}/feed/{config.user}/{config.secret}/unread")
  return { entry.links[0]['href']: entry for entry in reversed(wallabag_feed.entries) }

def __pocket_unread_articles():
  try:
    pocket_feed = pocket_connection.retrieve(state='unread')['list']
  except pocket.PocketException as e:
    print(e.message)
  unread_articles = pocket_feed.values() if pocket_feed else []
  return { entry['given_url'] : entry for entry in unread_articles }

def __remove_articles_from_pocket(pocket_articles):
  for url, entry in pocket_articles.items():
    pocket_connection.delete(entry['item_id'])
  try:
    pocket_connection.commit()
  except pocket.PocketException as e:
    print(e.message)

def __archive_missing_articles(pocket_entries, urls_of_unread_articles):
  for url, entry in pocket_entries.items():
    if url not in urls_of_unread_articles:
      pocket_connection.archive(entry['item_id'])
  try:
    pocket_connection.commit()
  except pocket.PocketException as e:
    print(e.message)

def __add_new_articles(unread_articles, urls_of_unread_articles):
  for url, article in unread_articles.items():
    if url not in urls_of_unread_articles:
      pocket_connection.add(url)

if __name__ == "__main__":
  unread_articles = __wallabag_unread_articles()
  pocket_entries = __pocket_unread_articles()

  __archive_missing_articles(pocket_entries, unread_articles.keys())

  __add_new_articles(unread_articles, pocket_entries.keys())
