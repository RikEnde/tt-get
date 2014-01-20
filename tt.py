#!/usr/bin/env python3

import urllib.request as request
import sys
from bs4 import BeautifulSoup, Tag, NavigableString
from termcolor import colored


def main(html):
    data = request.urlopen(html).read()
    content = get_content(data)
    print(unescape(content))


def get_content(html):
    soup = BeautifulSoup(html)

    content = soup.find('pre', attrs={'id': 'content'})
    return handle_line(content)


def print_tag(parent):
    def recursive(tag):
        ret = []
        for t in tag.childGenerator():
            if type(t) == NavigableString:
                ret.append(t)
            elif type(t) == Tag:
                colors = extract_colors(t)
                txt = recursive(t)
                ret.append(apply_colors(colors, txt))
        return ''.join(ret)

    colors = extract_colors(parent)
    txt = recursive(parent)
    return apply_colors(colors, txt)


def extract_colors(tag):
    return tag['class'] if 'class' in dict(tag.attrs) else None

def apply_colors(colors, txt):
    fg = 'white'
    bg = None
    if colors:
        for c in colors:
            if c.startswith('bg-'):
                bg = 'on_' + c[3:]
            else:
                fg = c
    return colored(txt, fg, bg) 


def handle_line(content):
    lines = []
    for tag in content.childGenerator():
        if type(tag) == NavigableString:
            lines.append(tag)
        elif type(tag) == Tag:
            lines.append(print_tag(tag))
        else:
            print(type(tag))
    return ''.join(lines)


def unescape(text):
    return BeautifulSoup(text)


if __name__ == '__main__':
    page = "http://teletekst-data.nos.nl/webtekst"

    if len(sys.argv) > 1:
        page += "?p=%s" % sys.argv[1].replace('/', '-')

    main(page)
