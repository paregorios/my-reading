#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
sometimes you feel like a camel, sometimes you don't
"""
import re

def deCamelize (camel):
    return re.sub('([A-Z]+)', r' \1',camel).lower()
