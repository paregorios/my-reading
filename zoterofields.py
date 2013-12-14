#!/usr/bin/env python'
# -*- coding: utf-8 -*-'

defmasks = {
    'bullets' : {
        'str' : "+ **%s:** %s" ,
        'unicode' : "+ **%s:** %s",
        'camel' : "+ **%s:** %s" ,
        'url' : "+ **%s:** [%s](%s)",
        'list' : "+ **%s:**" ,
        'dict' : "+ **%s:**" ,
        'listitem' : "+ %s",
        'dictitem' : "+ **%s:** %s"
        },
    'header' : {
        'str' : "**%s:** %s\n" ,
        'camel' : "**%s:** %s\n" ,    
        'url' : "**%s:** [%s](%s)\n",
        'list' : "**%s:**" ,
        'dict' : "+ **%s:**" ,
        },
    'zotsection' : {
        'str' : "+ **%s:** %s" ,
        'unicode' : "+ **%s:** %s",
        'camel' : "+ **%s:** %s" ,    
        'url' : "+ **%s:** [%s](%s)",
        'list' : "+ **%s:**" ,
        'dict' : "+ **%s:**" ,
        'listitem' : "+ %s",
        'dictitem' : "+ **%s:** %s",
        'mdurl' : "+ **%s:** %s",
    }

}
zfields = {
    'abstractNote':{
        'type':'str',
        'contexts':['header',],
        'caption': 'abstract',
        'mask': '**%s**:\n\n<p style="margin-left: 3em">%s</p>\n',
        'order': 500,
        },
    'accessDate':{
        'type':'str',
        'contexts':['bullets',],
        },
    'archive':{
        'type':'str',
        'contexts':['bullets',],
        },
    'author':{
        # suppress in favor of authors list
        'type':'str',
        'contexts':[],
        },
    'author_detail':{
        # suppress in favor of authors list
        'type':'dict',
        'contexts':[],
        },
    'authors':{
        'type':'list',
        'contexts':['zotsection',],
        'caption': 'authors of the bibliographic record'
        },
    'base':{
        'type':'url',
        'contexts':['bullets',],
        },
    'blogTitle':{
        'type':'str',
        'contexts':['bullets',],
        },
    'charset':{
        'type':'str',
        'contexts':['bullets',],
        },
    'collections':{
        'type':'list',
        'contexts':['zotsection',],
        },
    'content':{
        # suppress
        'type':'list',
        'contexts':[],
        },
    'contentType':{
        'type':'str',
        'contexts':['bullets',],
        },
    'creators':{
        'type':'list',
        'contexts':['header',],
        'order':400,
        'mask':"**%s:**\n"
        },
    'creatorType':{
        'type':'camel',
        'contexts':['header',],
        },
    'date':{
        'type':'str',
        'contexts':['header',],
        'order' : 300,
        },
    'filename':{
        'type':'str',
        'contexts':['bullets',],
        },
    'firstName':{
        'type':'str',
        'contexts':['header',],
        },
    'guidislink':{
        # what is this? suppress for now
        'type':'str',
        'contexts':[],
        },
    'href':{
        # markdown formatted URL for the creator
        'type':'mdurl',
        'contexts':[],
        },
    'id':{
        # uri for the record in zotero
        'type':'url',
        'contexts':[],
        },
    'itemKey':{
        'type':'str',
        'contexts':['zotsection',],
        'caption':'zotero item key for this record'
        },
    'itemType':{
        'type':'camel',
        'contexts':['bullets',],
        },
    'itemVersion':{
        'type':'str',
        'contexts':['zotsection',],
        'caption': 'zotero version number for this record',
        },
    'lastName':{
        'type':'str',
        'contexts':['header',],
        },
    'language':{
        'type':'str',
        'contexts':['bullets',],
        },
    'link':{
        # markdown formatted URL for the bibliographic record in zotero
        'type':'url',
        'contexts':[],
        'caption':'link to the zotero record'
        },
    'linkMode':{
        'type':'str',
        'contexts':['bullets',],
        },
    'links':{
        'type':'list',
        'contexts':['zotsection',],
        'caption':'zotero links to alternate formats of this record'
        },
    'md5':{
        'type':'str',
        'contexts':['zotsection',],
        },
    'mtime':{
        'type':'str',
        'contexts':['bullets',],
        },
    'name':{
        'type':'str',
        'contexts':['header',],
        },
    'parentItem':{
        'type':'str',
        'contexts':['bullets',],
        },
    'publicationTitle':{
        'type':'str',
        'contexts':['bullets',],
        },
    'published':{
        'type':'str',
        'contexts':['zotsection',],
        'caption': 'original publication date of record'
        },
    'published_parsed':{
        'type':'datetime',
        'contexts':[],
        },
    'relations':{
        'type':'str',
        'contexts':['bullets',],
        },
    'reportType':{
        'type':'str',
        'contexts':['bullets',],
        },
    'rights':{
        'type':'str',
        'contexts':['bullets',],
        },
    'runningTime':{
        'type':'str',
        'contexts':['bullets',],
        },
    'section':{
        'type':'str',
        'contexts':['bullets',],
        },
    'shortTitle':{
        'type':'str',
        'contexts':['bullets',],
        },
    'rel':{
        'type':'str',
        'contexts':['zotsection',],
        },
    'tag':{
        'type': 'str',
        'contexts':['zotsection',],
    },
    'tags':{
        'type':'list',
        'contexts':['zotsection',],
        },
    'title':{
        'type':'str',
        'contexts':['header',],
        'order': 100,
        },
    'title_detail':{
        'type':'dict',
        'contexts':[],
        },
    'type':{
        'type':'str',
        'contexts':['bullets',],
        },
    'updated':{
        'type':'str',
        'contexts':['zotsection',],
        'caption': 'last update to the record'
        },
    'updated_parsed':{
        'type':'datetime',
        'contexts':[],
        },
    'url':{
        'type':'url',
        'contexts':['header',],
        'order':200,
        },
    'value':{
        'type':'str',
        'contexts':['bullets',],
        },
    'volume':{
        'type':'str',
        'contexts':['bullets',],
        },
    'websiteTitle':{
        'type':'str',
        'contexts':['bullets',],
        },
    'zapi_creatorsummary':{
        'type':'str',
        'contexts':[],
        },
    'zapi_itemtype':{
        'type':'str',
        'contexts':[],
        },
    'zapi_key':{
        'type':'str',
        'contexts':[],
        },
    'zapi_numchildren':{
        'type':'str',
        'contexts':[],
        },
    'zapi_numtags':{
        'type':'str',
        'contexts':[],
        },
    'zapi_version':{
        'type':'str',
        'contexts':[],
        },
    'zapi_year':{
        'type':'str',
        'contexts':[],
    },
}