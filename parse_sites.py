import json
import os
import csv
from tns import SiteParser
from urllib.parse import urlparse

months = ["201605", "201606", "201607", "201608", "201609", "201610",
          "201611",
          "201612", "201701", "201702", "201703", "201704", "201705"]


def func_keys(parser, uri):
    """
    Match each URI to a parser for reusability in get_trending
    """

    parsers = {
        "http://abcnews.go.com/": parser.abcnews,
        "https://www.cbsnews.com/": parser.cbsnews,
        "https://www.nbcnews.com/": parser.nbcnews,
        "https://www.washingtonpost.com/": parser.washingtonpost,
        "https://www.npr.org/": parser.npr,
        "http://www.latimes.com/": parser.latimes,
        "https://www.usatoday.com/": parser.usatoday,
        "https://www.wsj.com/": parser.wsj,
        "https://www.nytimes.com/": parser.nytimes,
        "http://www.foxnews.com": parser.foxnews,
        "http://www.chicagotribune.com/": parser.chicagotribune
    }
    # execute on return
    return parsers[uri]()


def get_trending():
    # dirname = "./data/mementos/"
    with open("./data/news-websites-hashes.json") as f:
        site_hashes = json.load(f)
        for mo in months:
            out_mo = mo[:4] + "_" + mo[4:]
            stories = {}
            for site in site_hashes:
                # if site["URI-R"] == "https://www.wsj.com/":
                #     continue
                print(site["hash"], site["URI-R"])
                stories.setdefault(site["URI-R"], {})

                memento_dir = "./data/mementos/{}/{}/".format(
                    site["hash"], out_mo)
                for filename in os.listdir(memento_dir):
                    if not filename.endswith(".html"):
                        continue
                    print(memento_dir + filename)
                    text = open(memento_dir + filename).read()
                    # parser = SiteParser(text, trend_limit=15, left_col_limit=7,
                    #                     center_col_limit=7)
                    parser = SiteParser(text)
                    site_func = func_keys(parser, site["URI-R"])
                    stories[site["URI-R"]].setdefault(filename[:-5], {})
                    stories[site["URI-R"]][filename[:-5]] = site_func
                    # print(json.dumps(site_func, indent=4))
                    print("{} has {} headlines".format(
                        site["URI-R"], len(site_func["headlines"])))
                    if len(site_func["headlines"]) == 0:
                        print(site["URI-R"], "couldn't parse", filename)
            save_stories(stories, out_mo)
        return stories


def save_stories(stories, month):
    with open("./data/parsed_links/{}.json".format(month), "w") as out:
        json.dump(stories, out, indent=4, sort_keys=True)


def export_counts():
    """ Exports headline counts to CSV preprocessed for R """
    dirname = "data/parsed_links/"
    with open("data/parsed_links/headline-counts.csv", 'w') as out:
        writer = csv.writer(out)
        writer.writerow(["uri", "day", "headline_count", "has_hero"])
        for filename in os.listdir(dirname):
            if not filename.endswith(".json"):
                continue

            with open(dirname + filename, 'r') as f:
                stories = json.load(f)
            # dtime = filename[:-5].replace('_', '-') + memento

            for uri in stories:
                for memento in stories[uri]:

                    headline_count = len(stories[uri][memento]["headlines"])
                    netloc = urlparse(uri).netloc
                    # boolean if it found a hero or not
                    has_hero = 0
                    if stories[uri][memento]["hero_link"]:
                        has_hero = 1

                    print("URI {} has {} headlines for day {}".format(
                        uri, headline_count, memento))
                    dtime = filename[:-5].replace('_', '-') + "-" + memento
                    writer.writerow(
                        [netloc, dtime, headline_count, has_hero])


def export_memento_datetimes():
    """ Exports memento datetimes to CSV for R graph """
    with open("./data/news-websites-hashes.json") as f, \
            open("./data/mementos/memento-times.csv", "w") as out:
        site_hashes = json.load(f)
        writer = csv.writer(out)
        writer.writerow(["uri", "request_datetime", "actual_datetime"])

        for mo in months:
            out_mo = mo[:4] + "_" + mo[4:]
            for site in site_hashes:
                print(site["hash"], site["URI-R"])
                memento_dir = "./data/mementos/{}/{}/".format(
                    site["hash"], out_mo)
                netloc = urlparse(site["URI-R"]).netloc
                with open(memento_dir + "mementos.json", "r") as f2:
                    mementos = json.load(f2)
                    # req_time, act_time = get_dates(mementos)
                    for day in mementos[site["hash"]]:
                        req_time = out_mo.replace('_', '-') + \
                            "-" + day + "T01:00:00"
                        writer.writerow(
                            [netloc, req_time,
                             mementos[site["hash"]][day]["Memento-Datetime"]])


def get_dates(mementos):
    req_time = []
    act_time = []
    for k, site in mementos.items():
        for k2, day in site.items():
            # %Y%m%d%H%M%S -> %Y-%m-%dT%H:%M:%S
            req_time.append("2016-11-{}T01:00:00".format(k2))
            act_time.append(day["Memento-Datetime"])
    return req_time, act_time


if __name__ == "__main__":
    stories = get_trending()
    export_counts()
    # export_memento_datetimes()
