#!/usr/bin/env python
"""Download all hashtags."""
import os
import os.path
import json
import gzip
import get_tweets
import logging


def load_database(filename="./out/tweets.json.gz"):
    """Read JSON database and return JSON object."""
    if os.path.isfile(filename):
        json_data = gzip.open(filename).read()
        data = json.loads(json_data)
    else:
        data = {}
    return data


def save_database(data, filename="./out/tweets.json.gz"):
    """Write JSON object to to file."""
    with gzip.open(filename, "wt") as outfile:
        json.dump(data, outfile)


def load_hashtags(filename="hashtags"):
    """Read hashtags."""
    with open(filename, "r") as f:
        hashtags = f.readlines()

    hashtags = [x.strip() for x in hashtags]

    return hashtags


def main():
    """Run queries."""
    # Create logger
    logging.basicConfig(
        filename="get_all_hashtags.log",
        format="%(levelname)s - %(asctime)s - %(message)s",
        level=logging.INFO)
    logger = logging.getLogger()

    counter_added = 0
    counter_skipped = 0

    hashtags = load_hashtags()
    tweets = load_database()

    for query in hashtags:
        t = get_tweets.get_twitter_object()
        query_results = get_tweets.get_tweets_by_hashtags(query, t)

        for tweet in query_results["statuses"]:
            if tweet["id"] not in tweets:
                tweets[tweet["id"]] = tweet
                counter_added += 1
            else:
                counter_skipped += 1

    save_database(tweets)
    logger.info("Added: %d, skipped: %d, total: %d ." % (
                counter_added, counter_skipped, len(tweets)
                ))


if __name__ == "__main__":
    # execute only if run as a script
    main()
