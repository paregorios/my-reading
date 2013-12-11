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
import re
import sys
import traceback
sys.path.append('/Users/paregorios/Documents/files/L/libZotero/lib/py/libZotero')
import zotero

SCRIPT_DESC = 'CHANGE ME'

CAMEL_FIELDS = [
    u'itemType',
]

def deCamelize (camel):
    return re.sub('([A-Z]+)', r' \1',camel).lower()

def appendLink (parent, url, textValue=None):
    anchor = etree.SubElement(parent, 'a')
    anchor.set('href', url)
    if textValue is None:
        anchor.text = url
    else:
        anchor.text = textValue
    return anchor

def appendField (parent, fieldKey=None, fieldValue=None, childName='li', fieldType='string'):
    child = etree.SubElement(parent, childName)
    if fieldKey is None or len(fieldKey) == 0:
        tgt = child
        tgtTail = u''
    else:
        fieldName = deCamelize(fieldKey)
        strong = etree.SubElement(child, 'strong')
        strong.text = "%s:" % fieldName
        tgt = strong
        tgtTail = u' '
    if fieldValue is None:
        pass
    elif fieldType == 'string':
        if fieldKey is not None:
            if fieldKey in CAMEL_FIELDS:
                cleanVal = deCamelize(fieldValue)
            else:
                cleanVal = fieldValue
            tgt.tail = tgtTail
            span = etree.SubElement(child, 'span')
            if fieldValue is not None:
                span.set('class', "fieldValue %s" % fieldKey)
            else:
                span.set('class', "fieldValue")
            span.text = cleanVal
        else:
            tgt.tail = u"%s%s" % (tgtTail, fieldValue)
        
    elif fieldType == 'url':
        appendLink(child, fieldValue)
    return child



def main ():

    global args

    if args.verbose:
        l.basicConfig(level=l.DEBUG)
    else:
        l.basicConfig(level=l.WARNING)


    libtype = 'user'
    libid = '465'
    libslug = '<null>'
    zapikey = args.zapikey

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
            zlib = zotero.Library(libtype, libid, libslug, zapikey)
            blogbits = [] 
            for e in d.entries:
                l.debug("======================================")
                l.debug("title %s" % e.title)
                l.debug("methods:")
                l.debug(dir(e))
                l.debug("keys:")
                l.debug(e.keys())
                if e[u'zapi_itemtype'] != u'attachment':
                    xmldiv = etree.Element('div')
                    blogbits.append(xmldiv)
                    itemkey = e.id.split('/')[-1]
                    xmldiv.set('id', itemkey)
                    xmltitle = etree.SubElement(xmldiv, 'h2')
                    xmltitle.text = e.title
                    i = zlib.fetchItem(itemkey)
                    fields = i.apiObject
                    print fields
                    if len(fields.keys()) > 0:
                        # url
                        if u'url' in fields:
                            url = fields[u'url']
                            if len(url) > 0:
                                appendField(xmldiv, None, url, 'p', 'url')
                        # creators
                        if u'creators' in fields:
                            creators = fields[u'creators']
                            if len(creators) == 1:
                                c = creators[0]
                                if 'creatorType' in c:
                                    creatorType = c['creatorType']
                                else:
                                    creatorType = u'creator'
                                if 'name' in c:
                                    creatorName = c['name']
                                elif 'lastName' in c and 'firstName' in c:
                                    creatorName = u"%s %s" % (c['firstName'], c['lastName'].title())
                                appendField(xmldiv, creatorType, creatorName, 'p')
                            elif len(creators) > 1:
                                xmlp = etreeSubElement(xmldiv, 'p')
                                xmlp.text = u'creators'
                                xmllist = etree.SubElement(xmldiv, 'ul')
                                for c in creators:
                                    if 'creatorType' in c:
                                        creatorType = c['creatorType']
                                    else:
                                        creatorType = u'creator'
                                    if 'name' in c:
                                        creatorName = c['name']
                                    elif 'lastName' in c and 'firstName' in c:
                                        creatorName = u"%s %s" % (c['firstName'], c['lastName'].title())                                    
                                    appendField(xmldiv, creatorType, creatorName)


                        # make an ordered list of any other fields
                        xmllist = etree.SubElement(xmldiv, 'ul')
                        skipk = [
                            u'relations',
                            u'collections',
                            u'creators',
                            u'tags',
                            u'url', 
                            u'itemKey',
                            u'itemVersion',
                            u'title'
                        ]
                        keys = sorted(fields.keys())
                        for k in keys:
                            v = fields[k]
                            if v is None:
                                pass
                            else:
                                vt = type(v)
                                if k in skipk:
                                    l.debug ("deliberately skipping zotero content field %s" % k)
                                elif vt is unicode:
                                    if len(v) > 0:
                                        appendField(xmllist, k, v)
                                elif vt is int:
                                    appendField(xmllist, k, u"%s" % v)
                                else:
                                    l.debug ("no handler for %s so skipping zotero content field %s" % (vt, k))

    #                        if len(fields[k]) > 0:
    #                            xmlfield = etree.SubElement(xmllist, 'li')
    #                            xmlstrong = etree.SubElement(xmlfield, 'strong')
    #                            xmlstrong.text = k
    #                            xmlstrong.tail = fields[k]


                    print ("html:\n\n%s" % etree.tostring(xmldiv, pretty_print=True))
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
        parser.add_argument ("zapikey", type=str, action="store")
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
