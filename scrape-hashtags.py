#!/usr/bin/env python
"""
Usage: scrape-hashtags.py.

Scrapes Twitter hashtags related to #machinelearning.
"""

from lxml import html
import urllib.request


def get_related_searches(url):
    """
    Get related hashtags.

    Get related hashtags from a twitter search page and return them as
    dictionariy with hashtag as a key.
    """
    # Load the page and parse it
    html_page = urllib.request.urlopen(url).read().decode(u"utf8")
    tree = html.document_fromstring(html_page)

    # Extract relevant parts of the page
    xquery = u'//a[@class="AdaptiveRelatedSearches-itemAnchor"]'
    related_searches = tree.xpath(xquery)

    # Format them into a list of dictionaries
    hashtags = {}
    for search in related_searches:
        url = "https://twitter.com" + search.get("href")
        hashtag = search.text_content().strip()
        # Only add hashtags, not just searches
        if hashtag[0] == "#":
            hashtags[hashtag] = url

    return hashtags


def add_new_hashtags(old, new):
    """
    Add new hashtags to old hashtags.

    Add new hashtags returned by get_related_searches() to and old dict of
    hashtags.
    """
    for hashtag, url in new.items():
        # Check if it already exists
        if hashtag not in old:
            old[hashtag] = {
                "url": url,
                "hashtag": hashtag,
                "visited": False
            }

    return old


def visit_hashtag(hashtags, key):
    """Visit a hashtag from a list of hashtags by key."""
    new_hashtags = get_related_searches(hashtags[key]["url"])
    add_new_hashtags(hashtags, new_hashtags)

    hashtags[key]["visited"] = True
    return hashtags


def visit_unvisited(hashtags):
    """Visit all unvisited hashtags in the dict."""
    old_hashtags = hashtags.copy()
    for key, value in old_hashtags.items():
        if not value["visited"]:
            hashtags = visit_hashtag(hashtags, key)

    return hashtags


# Start with #machinelearning hashtag
# https://twitter.com/hashtag/machinelearning?src=rela
url = u"https://twitter.com/hashtag/machinelearning?src=rela"
ml_hashtags = get_related_searches(url)

hashtags = {}
for hashtag, url in ml_hashtags.items():
    new_hashtags = get_related_searches(url)
    add_new_hashtags(hashtags, new_hashtags)

hashtags = visit_unvisited(hashtags)
for key, value in hashtags.items():
    print(value["hashtag"])
