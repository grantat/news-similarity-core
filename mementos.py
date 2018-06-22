import requests
import hashlib
import json
import os
from calendar import monthrange


months = ["201605", "201606", "201607", "201608", "201609", "201610",
          "201611",
          "201612", "201701", "201702", "201703", "201704", "201705"]


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


def get_news_mementos(mo):
    """
    Get html for websites listed in textfile.
    """
    with open('data/news-websites.txt') as f:

        out_mo = mo[:4] + "_" + mo[4:]
        for news_site in f:
            saved_mementos = {}
            news_site = news_site.rstrip()
            site_hash = hashlib.md5(news_site.encode()).hexdigest()
            saved_mementos.setdefault(site_hash, {})
            makedir_if_not_exists(
                "data/mementos/{}/{}".format(site_hash, out_mo))
            # URI hash, formatted folder name
            summary_file = "data/mementos/{}/{}/mementos.json".format(
                site_hash, out_mo)

            if os.path.isfile(summary_file):
                print("{} already has mementos for {}. Delete folder to"
                      " download mementos again".format(news_site, out_mo))
                continue

            # Iterate through days in the month
            num_days = monthrange(int(mo[:4]), int(mo[4:]))[1]
            for day in list(range(1, num_days + 1)):
                day = "%02d" % (day,)
                outfile = "data/mementos/{}/{}/{}.html".format(
                    site_hash, out_mo, day)
                if os.path.isfile(outfile):
                    continue
                uri = "http://web.archive.org/web/{}{}010000if_/{}".format(
                    mo, day, news_site)
                resp = get_mementos(day, uri)

                # map request URI, response URI, and memento datetime
                saved_mementos[site_hash].setdefault(
                    day, {"URI-R": uri, "URI-M": resp.url,
                          "Memento-Datetime": resp.headers["Memento-Datetime"]
                          })
                print("Response:", resp.url)
                with open(outfile, 'w') as out:
                    out.write(resp.text)
            #
            # WRITE TO UPDATE ALREADY WRITTEN SUMMARY FILE WITH SAV
            #
            if os.path.isfile(summary_file):
                data = {}
                with open(summary_file, 'r') as memento_index:
                    data = json.load(memento_index)
                data[site_hash].update(saved_mementos[site_hash])
                with open(summary_file, 'w') as memento_index:
                    json.dump(data, memento_index)
            else:
                with open(summary_file, 'w') as memento_index:
                    json.dump(saved_mementos, memento_index)


if __name__ == "__main__":
    for mo in months:
        get_news_mementos(mo)
