#!/usr/bin/env python
"""
Download tweets.

Usage:
./get_tweets.py --query="#ai" --output="out/tweets-01.json"
"""

import json
import argparse
from twitter import Twitter, OAuth


def get_twitter_object(oauth_path="oauth.json"):
    """Connect to Twitter."""
    json_data = open(oauth_path).read()
    data = json.loads(json_data)

    # Variables that contains the user credentials to access Twitter API
    ACCESS_TOKEN = data["ACCESS_TOKEN"]
    ACCESS_SECRET = data["ACCESS_SECRET"]
    CONSUMER_KEY = data["CONSUMER_KEY"]
    CONSUMER_SECRET = data["CONSUMER_SECRET"]

    oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

    # Initiate the connection to Twitter
    t = Twitter(auth=oauth, retry=True)

    return t


def get_tweets_by_hashtags(hashtag, t, filepath):
    """Get tweets by hashtag."""
    response = t.search.tweets(q=hashtag)

    with open(filepath, 'w') as outfile:
        json.dump(response, outfile)


def main():
    """Run query."""
    parser = argparse.ArgumentParser()

    parser.add_argument("--query", "-q",
                        help="query to Twitter search",
                        required=True,
                        metavar="QUERY",
                        dest="query")
    parser.add_argument("--output", "-o",
                        help="path to output file",
                        required=True,
                        metavar="PATH",
                        dest="out")

    args = parser.parse_args()

    query = args.query
    out = args.out

    t = get_twitter_object()
    get_tweets_by_hashtags(query, t, out)


if __name__ == "__main__":
    # execute only if run as a script
    main()
