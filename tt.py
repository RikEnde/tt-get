#!/usr/bin/env python

import urllib2
import sys
from BeautifulSoup import BeautifulSoup, Tag, NavigableString

DEBUG=False

if DEBUG:
    def colored(txt, fg, bg):
        return "[%s][%s]%s[RS]" % (fg, bg, txt)
else:
    from termcolor import colored


def main(html):
    data = urllib2.urlopen(html).read()
    content = get_content(data)
    print unescape(content)


def get_content(html):
    soup = BeautifulSoup(html)

    content = soup.find('pre', attrs={'id': 'content'})
    print content
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
    return tag['class'].split(' ') if 'class' in dict(tag.attrs) else None

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
            print type(tag)
    return ''.join(lines)


def unescape(text):
    return unicode(BeautifulSoup(text, convertEntities=["xml", "html"]))


if __name__ == '__main__':
    page = "http://teletekst-data.nos.nl/webtekst"

    if len(sys.argv) > 1:
        page += "?p=%s" % sys.argv[1].replace('/', '-')

    main(page)
