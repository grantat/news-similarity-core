from urllib.parse import urlparse
import os
import re


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


def makedir_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
