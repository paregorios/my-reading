#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
template
"""

import argparse
import chardet
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import feedparser
from getpass import getpass
import json
import html2text
import logging as l
from lxml import etree
import os
import re
import smtplib
import sys
import traceback
sys.path.append('/Users/paregorios/Documents/files/L/libZotero/lib/py/libZotero')
import zotero

SCRIPT_DESC = 'CHANGE ME'

DEFAULT_CREDENTIALS = './creds.json'
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
        tgt.tail = tgtTail
        appendLink(child, fieldValue)
    return child

def sendToTumblr(mailer, subject, link, content, fromAddr, toAddr, ccAddrs=[]):
    msg = MIMEText(content)
    msg['Subject'] = "!mReading: %s" % subject
    msg['From'] = fromAddr
    msg['To'] = toAddr
    if len(ccAddrs) > 0:
        msg['Cc'] = ', '.join(ccAddrs)
    foo = msg.as_string
    print "detecting encoding in msg.as_string"
    print chardet.detect(foo)
    #mailer.sendmail(fromAddr, [toAddr,]+ccAddrs, msg.as_string())


def doCreators(fields, xmlParent):
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
            appendField(xmlParent, creatorType, creatorName, 'p')
        elif len(creators) > 1:
            xmlp = etree.SubElement(xmlParent, 'h3')
            xmlp.text = u'creators:'
            xmllist = etree.SubElement(xmlParent, 'ul')
            for c in creators:
                if 'creatorType' in c:
                    creatorType = c['creatorType']
                else:
                    creatorType = u'creator'
                if 'name' in c:
                    creatorName = c['name']
                elif 'lastName' in c and 'firstName' in c:
                    creatorName = u"%s %s" % (c['firstName'], c['lastName'].title())                                    
                appendField(xmllist, creatorType, creatorName)

def doAbstract(fields, xmlParent):
    if u'abstractNote' in fields:
        abstract = fields[u'abstractNote']
        if len(abstract.strip()) > 0:
            absdiv = etree.SubElement(xmlParent, 'div')
            absdiv.set('class', 'abstract')
            xmlhead = etree.SubElement(absdiv, 'h3')
            xmlhead.text = 'abstract:'
            for line in abstract.strip().split('\n'):
                if len(line.strip()) > 0:
                    xmlp = etree.SubElement(absdiv, 'p')
                    xmlp.text = line.strip()

def main ():

    global args

    if args.verbose:
        l.basicConfig(level=l.DEBUG)
    else:
        l.basicConfig(level=l.WARNING)


    if args.credentials:
        fn = args.credentials
    else:
        fn = DEFAULT_CREDENTIALS
    creds = json.loads(open(fn).read())
    libtype = creds['libraryType']
    libid = creds['libraryID']
    libslug = creds['librarySlug']
    collid = creds['collectionID']
    zapikey = creds['zapiKey']
    useragent = creds['userAgent']
    prev_libversion = creds['prevLibraryVersion']
    feedparser.USER_AGENT = useragent


    headers = {
        'Zotero-API-Version':'2',
        'If-Modified-Since-Version':prev_libversion
    }
    query = 'https://api.zotero.org/%ss/%s/collections/%s/items?order=dateModified&sort=asc&newer=%s' % (libtype, libid, collid, prev_libversion)
    l.debug("query: %s" % query)
    d = feedparser.parse(query, request_headers=headers)
    l.debug("response status: %s" % d.status)
    if d.status == 200:
        print ("entries: %s" % len(d.entries))
        if len(d.entries) > 0:
            zlib = zotero.Library(libtype, libid, libslug, zapikey, userAgent=useragent)
            packages = [] 
            for e in d.entries:
                l.debug("======================================")
                l.debug("title %s" % e.title)
                l.debug("methods:")
                l.debug(dir(e))
                l.debug("keys:")
                for k in e.keys():
                    l.debug ("key %s: %s" % (k, e[k]))
                if e[u'zapi_itemtype'] != u'attachment':
                    itemkey = e.zapi_key
                    xmldiv = etree.Element('div')
                    xmldiv.set('id', itemkey)
                    appendField(xmldiv, 'title', e.title, 'p')
                    i = zlib.fetchItem(itemkey)
                    fields = i.apiObject
                    # print fields
                    if len(fields.keys()) > 0:
                        # url
                        if u'url' in fields:
                            url = fields[u'url']
                            if len(url) > 0:
                                appendField(xmldiv, 'link', url, 'p', 'url')
                        # creators
                        doCreators(fields, xmldiv)
                        # abstract
                        doAbstract(fields, xmldiv)
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
                            u'title',
                            u'abstractNote'
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


                        # last access date

                        # zotero export versions
                        zdiv = etree.SubElement(xmldiv, 'div')
                        zdiv.set('class', 'zotero')
                        xmlhead = etree.SubElement(zdiv, 'h3')
                        xmlhead.text = 'Additional bibliographic information on zotero.org'
                        xmllist = etree.SubElement(zdiv, 'ul')
                        appendField(xmllist, 'online record', e.link, 'li', 'url')
    

                    package = {}
                    package['zapi_key'] = itemkey
                    package['title'] = e.title
                    package['url'] = url
                    htmlpack = etree.tostring(xmldiv, pretty_print=True, encoding='utf-8', method='html')
                    charset = chardet.detect(htmlpack)
                    if charset['encoding'] not in ['ascii', 'utf-8']:
                        print ("%s: encoding of '%s' was '%s'" % (itemkey, 'htmlpack', charset['encoding']))
                        print htmlpack
                    package['html'] = htmlpack
                    h2md = html2text.HTML2Text()
                    h2md.body_width = 0 # disable line wrapping
                    htmlsimple = etree.tostring(xmldiv, pretty_print=True, encoding="ascii", method='html')
                    charset = chardet.detect(htmlpack)
                    if charset['encoding'] != 'ascii':
                        print ("%s: encoding of '%s' was '%s'" % (itemkey, 'htmlsimple', charset['encoding']))
                        print htmlsimple
                    mdpack = h2md.handle(htmlsimple)
                    charset = chardet.detect(mdpack)
                    if charset['encoding'] != 'ascii':
                        print ("%s: encoding of '%s' was '%s'" % (itemkey, 'mdpack', charset['encoding']))
                        print mdpack
                    package['md'] = mdpack
                    packages.append(package)

            ccAddrs = []
            if args.verbose:
                ccAddrs.append(creds['debugCCAddr'])

            mailer = smtplib.SMTP(creds['smtpServer'])
            mailer.starttls()
            mailer.login(creds['smtpUser'],getpass())

            for p in packages:
                if 'md' in p:
                    print ("trying to send %s (%s)" % (p['zapi_key'], p['title']))
                    sendToTumblr(mailer, p['title'], p['url'], p['md'], creds['tumblrFromAddr'], creds['tumblrToAddr'])
            mailer.quit()

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
        parser.add_argument ("-c", "--credentials", type=str, nargs="?")
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
