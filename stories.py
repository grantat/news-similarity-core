import requests
import json
import hashlib
import os
import argparse


def load_links(filename):
    with open(filename) as f:
        data = json.load(f)
        return data


def get_story(session, uri):
    """ Get mementos for html using Internet Archive """
    try:

        print(uri)
        r = session.get(uri, verify=False)
        # return entire response
        return r
    except Exception as e:
        print("Failed with error", e)
        return


if __name__ == "__main__":
    # months to download stories from
    months = ["2016_12", "2017_01"]
    parser = argparse.ArgumentParser()
    # parser.add_argument("links_json", type=str,
    #                     help="Links per day JSON file to iterate upon")
    parser.add_argument("--kval", type=str,
                        help="Links per day JSON file to iterate upon")
    args = parser.parse_args()
    session = requests.Session()
    session.headers = headers = {
        'user-agent': 'Web Science and Digital Libraries (@WebSciDL) '
        '<gatki001@odu.edu>'}
    session.max_redirects = 100
    for mo in months:
        print("Month {}".format(mo))
        links_by_day = load_links(
            "data/links_per_day/{}/links_per_day_{}.json".format(mo,
                                                                 args.kval))
        error_file = "data/errors/links_{}.txt".format(mo)
        with open(error_file, 'w') as err_out:
            for day in links_by_day:
                links = links_by_day[day]
                print("Day {}".format(day))
                for uri in links:
                    directory = "./data/stories/if_/{}/{}/".format(mo, day)
                    link_hash = hashlib.md5(uri.encode()).hexdigest()
                    outfile = directory + link_hash + ".html"

                    if not os.path.exists(directory):
                        os.makedirs(directory)

                    if os.path.exists(outfile):
                        continue

                    resp = get_story(session, uri)

                    if not resp:
                        print("Error with response:", resp)
                        print("{}\nError with response: {}".format(
                            uri, resp), file=err_out)
                        continue

                    if resp.status_code == 200:
                        with open(outfile, "w") as out:
                            out.write(resp.text)
                    else:
                        print(resp.history)
                        print("ERR::{} response code".format(resp.status_code))
                        print("{}\nError with response code: {}".format(
                            uri, resp.status_code), file=err_out)

        if os.path.getsize(error_file) == 0:
            os.remove(error_file)
