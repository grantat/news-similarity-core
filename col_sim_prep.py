import json
from urllib.parse import urlparse
import csv
import os
import re
from util import makedir_if_not_exists
from calendar import monthrange


def format_link(link):
    """ Regex parse web archive link and add 'if_' after datetime """
    p = re.compile('(\/web\/[0-9]+\/)')
    for m in p.finditer(link):
        to_rep = link[m.start():m.end()][:-1] + "if_/"
        new_str = link[:m.start()] + to_rep + link[m.end():]
        # only need first occurrence
        return new_str
    # return original if already formatted
    return link


def is_absolute(url):
    """ Check if URI is absolute """
    return bool(urlparse(url).netloc)


def k10_stories(parsed_links_file, year, month):
    links_per_day = {}
    with open(parsed_links_file) as f:
        data = json.load(f)
        # Number of days in the month
        num_days = monthrange(int(year), int(month))[1]
        for n in range(1, num_days + 1):
            links = set()
            num = format(n, '02d')
            for i in data:
                # exclude wsj
                if i == "https://www.wsj.com/":
                    continue

                if data[i][num]["hero_link"]:
                    hero_link = data[i][num]["hero_link"]
                    if not is_absolute(hero_link):
                        hero_link = "http://web.archive.org" + hero_link
                    links.add(format_link(hero_link))

                for h in data[i][num]["headlines"]:
                    # if not absolute add web archive domain
                    if not is_absolute(h["link"]):
                        h["link"] = "http://web.archive.org" + h["link"]
                    links.add(format_link(h["link"]))

            links_per_day.setdefault(num, list(links))
            print("Day {} has {} links".format(num, len(links)))

    return links_per_day


def k1_stories(parsed_links_file, year, month):
    """ Format group the first story of each news outlet per day """
    links_per_day = {}
    with open(parsed_links_file) as f:
        data = json.load(f)
        # Number of days in the month
        num_days = monthrange(int(year), int(month))[1]
        for n in range(1, num_days + 1):
            links = set()
            num = format(n, '02d')
            for i in data:
                # exclude wsj
                if i == "https://www.wsj.com/":
                    continue

                if data[i][num]["hero_link"]:
                    hero_link = data[i][num]["hero_link"]
                    if not is_absolute(hero_link):
                        hero_link = "http://web.archive.org" + hero_link
                    links.add(format_link(hero_link))
                    continue

                for h in data[i][num]["headlines"]:
                    # if not absolute add web archive domain
                    if not is_absolute(h["link"]):
                        h["link"] = "http://web.archive.org" + h["link"]
                    links.add(format_link(h["link"]))
                    break

            links_per_day.setdefault(num, list(links))
            print("Day {} has {} links".format(num, len(links)))

    return links_per_day


def k3_stories(parsed_links_file, year, month):
    """ Format group the first 3 stories of each news outlet per day """
    links_per_day = {}
    with open(parsed_links_file) as f:
        data = json.load(f)
        # Number of days in the month
        num_days = monthrange(int(year), int(month))[1]
        for n in range(1, num_days + 1):
            links = set()
            num = format(n, '02d')
            for i in data:
                # exclude wsj
                temp = set()
                if i == "https://www.wsj.com/":
                    continue

                if data[i][num]["hero_link"]:
                    hero_link = data[i][num]["hero_link"]
                    if not is_absolute(hero_link):
                        hero_link = "http://web.archive.org" + hero_link
                    temp.add(format_link(hero_link))

                for h in data[i][num]["headlines"]:
                    if len(temp) == 3:
                        break
                    # if not absolute add web archive domain
                    if not is_absolute(h["link"]):
                        h["link"] = "http://web.archive.org" + h["link"]
                    temp.add(format_link(h["link"]))

                # print(i, len(temp))
                links.update(temp)

            links_per_day.setdefault(num, list(links))
            print("Day {} has {} links".format(num, len(links)))

    return links_per_day


def col_sim_sum(months=["2016_11"]):
    """ Make Col-sim summary CSV of the specified month directories """
    col_sim_dir = "data/col_sim/"
    with open(col_sim_dir + "col_sim_summary.csv", "w") as out:
        writer = csv.writer(out)
        writer.writerow(["k_val", "date", "cosine", "entity"])
        # go through kval directories
        for k in os.listdir(col_sim_dir):
            k_dir = "{}{}/".format(col_sim_dir, k)
            if not os.path.isdir(k_dir):
                continue
            # month directories
            for mo in os.listdir(k_dir):
                if mo not in months:
                    continue
                # each sim value json
                for filename in os.listdir(k_dir + mo):
                    if not filename.endswith(".json"):
                        continue
                    file_loc = "{}{}/{}".format(k_dir, mo, filename)
                    with open(file_loc) as f:
                        data = json.load(f)
                        num = filename[:-5]
                        date = "{}-{}".format(mo.replace("_", "-"), num)
                        cos = data[num]["col-sim"]["cosine"]
                        ent = data[num]["col-sim"]["entity"]
                        print(num, cos, ent)
                        writer.writerow([k, date, cos, ent])


if __name__ == "__main__":
    # iterate through parsed links and get k = 1, 3, 10 stories
    # formatted by day
    parsed_links_dir = "data/parsed_links/"
    links_per_day_dir = "data/links_per_day/"
    # for filename in os.listdir(parsed_links_dir):
    #     if filename.endswith(".json"):
    #         links_per_day = k1_stories(
    #             parsed_links_dir + filename, filename[:4], filename[5:7])
    #         save_dir = "{}{}/".format(links_per_day_dir, filename[:-5])
    #         makedir_if_not_exists(save_dir)
    #         with open("{}links_per_day_{}.json".format(save_dir,
    #                                                    "k1"), "w") as out:
    #             json.dump(links_per_day, out, indent=4)

    # months/directories we want to summarize
    months = ["2016_11", "2016_12", "2017_01"]
    col_sim_sum(months)
