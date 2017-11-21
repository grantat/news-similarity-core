import requests
import hashlib
import json
import os


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
    Get timemaps for websites listed in textfile.
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
            resp = get_timemaps(news_site)
            save_response(news_site, resp, site_hash)

        json.dump(hash_pairs, out)


def count_mementos():
    directory = "data/timemaps/"
    print("For the month of November 2016")
    for filename in os.listdir(directory):
        with open(directory + filename) as f:
            resp = json.load(f)
            counter = 0
            for uri_m in resp:
                datetime = uri_m[1]
                if datetime.startswith("201611"):
                    counter += 1
            print("URI {} has {} mementos".format(
                resp["original_uri"], counter))


if __name__ == "__main__":
    get_news_timemaps()
    # count_mementos()
