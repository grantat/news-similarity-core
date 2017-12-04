import requests
import hashlib
import json
import os
import csv
from datetime import datetime
from urllib.parse import urlparse


def get_timemaps(news_site):
    """ Get timemap JSON using Internet Archive """
    try:
        headers = {
            'user-agent': 'Web Science and Digital Libraries (@WebSciDL) '
            '<gatki001@odu.edu>'}
        r = requests.get(
            "http://web.archive.org/web/timemap/json/" + news_site,
            headers=headers)
        return r.json()
    except Exception as e:
        print("Failed with error", e)
        return []


def save_response(news_site, resp, site_hash):
    """ Save response to file with hash from URI using md5 """
    with open('data/timemaps/' + site_hash + '.json', 'w') as out:
        json.dump(resp, out)


def get_news_timemaps():
    """
    Get timemaps for websites listed in textfile save if not already saved
    Save hash pairs to json
    """
    with open('data/news-websites.txt') as f, \
            open('data/news-websites-hashes.json', 'w') as out:
        hash_pairs = []
        for news_site in f:
            news_site = news_site.rstrip()
            site_hash = hashlib.md5(news_site.encode()).hexdigest()

            pair = {"URI-R": news_site, "hash": site_hash}
            hash_pairs.append(pair)
            print("Requesting:", news_site)
            if os.path.isfile('data/timemaps/' + site_hash + '.json'):
                print('data/timemaps/' + site_hash +
                      '.json Already exists delete to replace.')
                continue
            resp = get_timemaps(news_site)
            save_response(news_site, resp, site_hash)

        json.dump(hash_pairs, out)


def count_mementos():
    """ Helper function to count mementos from timemap in 11/2016 """
    directory = "data/timemaps/"
    print("For the month of November 2016")
    for filename in os.listdir(directory):
        with open(directory + filename) as f:
            resp = json.load(f)
            counter = 0
            for uri_m in resp:
                datetime_val = uri_m[1]
                if datetime_val.startswith("201611"):
                    counter += 1
            print("URI {} has {} mementos".format(
                resp["original_uri"], counter))


def find_hash_match(hash_val, hash_list):
    """ Helper function to find uri-r for a given hash """
    for i in hash_list:
        if i["hash"] == hash_val:
            return i["URI-R"]


def export_counts():
    """ Exports timemap counts to CSV preprocessed for R """
    with open("data/hour-counts.csv", 'w') as out:
        writer = csv.writer(out)
        # hours = list(range(0, 24))
        writer.writerow(["uri", "datetime"])
        for filename in os.listdir("data/timemaps/"):
            if not filename.endswith(".json"):
                continue

            with open("data/timemaps/" + filename) as f, \
                    open('data/news-websites-hashes.json') as f2:
                resp = json.load(f)
                hashes = json.load(f2)
                hash_val = filename[:-5]
                uri = find_hash_match(hash_val, hashes)
                netloc = urlparse(uri).netloc
                counter = 0
                # skip first entry - data headers
                for uri_m in resp[1:]:
                    # skip first item
                    datetime_val = uri_m[1]
                    if datetime_val.startswith("201611"):
                        datetime_val = datetime.strptime(
                            datetime_val, "%Y%m%d%H%M%S").strftime(
                            "%Y-%m-%dT%H:%M:%S")
                        writer.writerow([netloc, datetime_val])
                        counter += 1
                print("URI {} has {} mementos".format(
                    uri, counter))


if __name__ == "__main__":
    get_news_timemaps()
    # count_mementos()
    export_counts()
