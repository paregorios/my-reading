#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A Unicode Dictionary Class, With Special Talents
"""

import collections
from UserDict import UserDict

class UnicodeDict(UserDict):
    """ a dictionary class in which all keys and all textual values are unicode and there are methods for un|encoding """

    # the following replacements are for cleaning up string values
    replacements = [
        (u'\u00A0', u' '),              # non-breaking spaces become normal spaces
    ]


    def __toUnicode(self, data):
        """ helper function to recursively convert data to unicode """
        if isinstance(data, unicode):
            return(data)
        elif isinstance(data, basestring):
            return unicode(data, 'utf-8')
        elif isinstance(data, collections.Mapping):
            return dict(map(self.__toUnicode, data.iteritems()))
        elif isinstance(data, collections.Iterable):
            return type(data)(map(self.__toUnicode, data))
        else:
            return data


    def __fromUnicode(self, data, encoding='utf-8'):
        """ helper function to recursively convert data from unicode to another encoding """
        if isinstance(data, unicode):
            return data.encode(encoding)
        elif isinstance(data, basestring):
            return data.encode(encoding)
        elif isinstance(data, collections.Mapping):
            return dict(map(self.__fromUnicode, data.iteritems()))
        elif isinstance(data, collections.Iterable):
            return type(data)(map(self.__fromUnicode, data))
        else:
            return data


    def __init__(self, cleanValues=True):
    	""" initialize the dictionary and tell it whether or not to clean junk out of value strings on setitem """
        self.cleanValues = cleanValues
        UserDict.__init__(self) 


    def copy(self):
    	""" make a copy of the dictionary """
        if self.__class__ is UserDict:
            return UserDict(self.data)         
        import copy
        return copy.copy(self)  


    def __keytransform(self, key):
    	""" helper method to always use unicode internally for key values """
        cookedKey = key
        try: 
            cookedKey = unicode(cookedKey, 'utf-8')
        except TypeError:
            pass
        return cookedKey


    def __getitem__ (self, key):
    	""" standard dictionary behavior, and you get the unicode value """
        return UserDict.__getitem__(self, self.__keytransform(key))


    def getEncoded (self, key, encoding='utf-8'):
    	""" returns the value corresponding to key, with all textual components in the charset specified by encoding """
        item = self.__getitem__(key)
        item = self.__fromUnicode(item, encoding)
        return item

    
    def __setitem__(self, key, item):
    	""" inserts a key, value pair, converting all textual components to unicode and optionally removing junk from strings """
        if self.cleanValues:
            cleanItem = self.__toUnicode(item)
        else:
            cleanItem = item
        UserDict.__setitem__(self, self.__keytransform(key), cleanItem)

