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
    if DEBUG:
        print content
    return print_tag(content)


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
    if colors:
        fg = 'white'
        bg = None
        for c in colors:
            if c.startswith('bg-'):
                bg = 'on_' + c[3:]
            else:
                fg = c
        return colored(txt, fg, bg) 
    else:
        return txt


def unescape(text):
    return unicode(BeautifulSoup(text, convertEntities=["xml", "html"]))


if __name__ == '__main__':
    page = "http://teletekst-data.nos.nl/webtekst"

    if len(sys.argv) > 1:
        page += "?p=%s" % sys.argv[1].replace('/', '-')

    main(page)
