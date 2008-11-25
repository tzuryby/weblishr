#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import web
from config import site_globals
'''data layer'''

class Provider(object):
    ''' base class for providers
        there are:
            WebDBProvider   -> webpy db abstraction layer
            GAEProvider     -> Google App Engine Data API
    '''
    def get_object(self, url):
        raise NotImplemented
        
    def get_frontier(self, sections_items):
        raise NotImplemented
        
    def add_object(self, **data):
        raise NotImplemented
        
    def update_object(self, **data):
        raise NotImplemented
        
    def get_archive(self, num_or_rows):
        raise NotImplemented
        
class WebDBProvider(Provider):
    def __init__(self, db = web.database(dbn='sqlite', db='db/weblishr.db')):
        self.db = db
        
    def get_object(self, url):
        '''first (and only) row OR 0'''
        rows= self.db.select('objects', where = 'url=$url', vars=locals()).list()
        return len(rows) and rows[0]

        
    def get_frontier(self):
        args = web.storage()
        # get the sections
        sections = self.db.select('objects', group='section', order='section')
        # get last N rows per section
        for section in sections:
            args[section.section] = self.db.select(
                'objects', where='section="%s"' % section.section, 
                limit= site_globals.posts_per_section, order = 'pub_date desc')
                
        return args
        
    def add_object(self, **data):
        self.db.insert('objects', **data)
        
    def update_object(self, **data):
        self.db.update('objects', **data)
        
    def get_archive(self, num_of_rows=0):
        kwargs = dict(order='pub_date desc')
        if num_of_rows:
            kwargs[limit] = num_of_rows
        return self.db.select('objects', **kwargs)
        
        
class GAEDataStoreProvider(object):
    pass
    