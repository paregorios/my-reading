#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
template
"""

import argparse
import feedparser
import json
import logging as l
from lxml import etree
import os
import sys
import traceback

SCRIPT_DESC = 'CHANGE ME'

def main ():

    global args

    if args.verbose:
        l.basicConfig(level=l.DEBUG)
    else:
        l.basicConfig(level=l.WARNING)


    feedparser.USER_AGENT = "ParegoricReadingBot/1.0 +http://www.paregorios.org/"
    prev_libversion = '6454'
    headers = {
        'Zotero-API-Version':'2',
        'If-Modified-Since-Version':prev_libversion
    }
    query = 'https://api.zotero.org/users/465/collections/V9VA7HTP/items?order=dateModified&sort=asc&newer=%s' % prev_libversion
    d = feedparser.parse(query, request_headers=headers)
    print("response status: %s" % d.status)
    if d.status == 200:
        print ("entries: %s" % len(d.entries))
        if len(d.entries) > 0:
            root = etree.Element('div')
            for e in d.entries:
                print e.keys()
                ediv = etree.SubElement(root, 'div')
                # ediv.set('id', edata['itemKey'])
                x = etree.SubElement(ediv, 'title')
                x.text = e.title
            print ("html:\n\n%s" % etree.tostring(root, pretty_print=True))
        if 'last-modified-version' in d.headers.keys():
            prev_libversion = d.headers['last-modified-version'].strip()
            print('prev_libversion: %s' % prev_libversion)
    elif d.status == 304:
        print ('Zotero server responded with status code 304: library has not been modified since version %s' % prev_libversion)
        exit(0)
    else:
        l.error('Zotero server returned %s status code' % d.status)
        exit(1)


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description=SCRIPT_DESC, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument ("-v", "--verbose", action="store_true", default=False, help="verbose output")
        args = parser.parse_args()
        main()
        sys.exit(0)
    except KeyboardInterrupt, e: # Ctrl-C
        raise e
    except SystemExit, e: # sys.exit()
        raise e
    except Exception, e:
        print "ERROR, UNEXPECTED EXCEPTION"
        print str(e)
        traceback.print_exc()
        os._exit(1)
