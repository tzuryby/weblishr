#!/usr/bin/env python
from __future__ import generators

"""web.py: makes web apps (http://webpy.org)"""
__version__ = "0.3"
__revision__ = "$Rev$"
__author__ = "Aaron Swartz <me@aaronsw.com>"
__license__ = "public domain"
__contributors__ = "see http://webpy.org/changes"

# todo:
#   - some sort of accounts system

import utils, db, net, wsgi, http, webapi, httpserver, debugerror
import template, form

import session

from utils import *
from db import *
from net import *
from wsgi import *
from http import *
from webapi import *
from httpserver import *
from debugerror import *
from application import *
try:
    import webopenid as openid
except ImportError:
    pass # requires openid module

def main():
    import doctest
    
    doctest.testmod(utils)
    doctest.testmod(db)
    doctest.testmod(net)
    doctest.testmod(wsgi)
    doctest.testmod(http)
    doctest.testmod(webapi)
    
    template.test()
    
    import sys
    urls = ('/web.py', 'source')
    class source:
        def GET(self):
            header('Content-Type', 'text/python')
            return open(sys.argv[0]).read()
    
    if listget(sys.argv, 1) != 'test':
        app = application(urls, locals())
        app.run()

if __name__ == "__main__": main()

