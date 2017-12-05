import requests
import hashlib
import json
import os
# import csv
# from datetime import datetime
# from urllib.parse import urlparse


def get_mementos(day, uri):
    """ Get mementos for html using Internet Archive """
    try:
        headers = {
            'user-agent': 'Web Science and Digital Libraries (@WebSciDL) '
            '<gatki001@odu.edu>'}

        print("Request:", uri)
        r = requests.get(uri, headers=headers)
        # return entire response
        return r
    except Exception as e:
        print("Failed with error", e)
        return


def makedir_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_news_mementos():
    """
    Get html for websites listed in textfile.
    """
    with open('data/news-websites.txt') as f:

        for news_site in f:
            saved_mementos = {}
            news_site = news_site.rstrip()
            site_hash = hashlib.md5(news_site.encode()).hexdigest()
            saved_mementos.setdefault(site_hash, {})
            makedir_if_not_exists("data/mementos/" + site_hash)
            # memento_pairs = []
            # November 1 - 30
            if os.path.isfile("data/mementos/{}/mementos.json".
                              format(site_hash)):
                print("{} already has mementos. Delete folder to download "
                      "mementos again".format(site_hash))
                continue

            for day in list(range(1, 31)):
                day = "%02d" % (day,)
                uri = "http://web.archive.org/web/201611{}010000if_/{}".format(
                    day, news_site)
                resp = get_mementos(day, uri)

                # map request URI, response URI, and memento datetime
                saved_mementos[site_hash].setdefault(
                    day, {"URI-R": uri, "URI-M": resp.url,
                          "Memento-Datetime": resp.headers["Memento-Datetime"]
                          })
                print("Response:", resp.url)
                with open("data/mementos/{}/{}.html".
                          format(site_hash, day), 'w') as out:
                    out.write(resp.text)

            with open("data/mementos/{}/mementos.json".format(site_hash), 'w')\
                    as memento_index:
                json.dump(saved_mementos, memento_index)


if __name__ == "__main__":
    get_news_mementos()
