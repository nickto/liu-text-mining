#!/usr/bin/env python
"""
Usage: scrape-hashtags.py.

Scrapes Twitter hashtags related to #machinelearning.
"""

from lxml import html
import urllib.request
VISITED_MAX = 30


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


def unvisited_remain(hashtags):
    """Check if there are any unisited hashtags."""
    for key, value in hashtags.items():
        if not value["visited"]:
            return True
    return False


def count_visited(hashtags):
    """Count visited hashtags."""
    counter = 0
    for key, value in hashtags.items():
        if key[0] == "#" and value["visited"]:
            counter += 1
    print(counter)
    return counter


def scrape_from_entry_point(url, hashtags={}):
    """Scrape hashtags from an entry point specified as URL."""
    initial_hashtags = get_related_searches(url)

    for hashtag, url in initial_hashtags.items():
        new_hashtags = get_related_searches(url)
        add_new_hashtags(hashtags, new_hashtags)

    while unvisited_remain(hashtags) and count_visited(hashtags) < VISITED_MAX:
        hashtags = visit_unvisited(hashtags)

    return hashtags


# Start with #machinelearning hashtag
url = u"https://twitter.com/hashtag/bayesianinference?src=rela"
hashtags = scrape_from_entry_point(url)

for key, value in hashtags.items():
    if value["hashtag"][0] == "#":
        print(value["hashtag"] + "\t" + str(value["visited"]))
