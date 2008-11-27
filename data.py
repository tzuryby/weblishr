#!/usr/bin/env python
# -*- coding: UTF-8 -
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
        
    def get_archive(self, num_of_rows):
        raise NotImplemented

class WebDBProvider(Provider):
    def __init__(self, db = web.database(dbn='sqlite', db='db/weblishr.db')):
        self.db = db
        
    def get_object(self, url):
        #first (and only) row OR 0
        rows= self.db.select('objects', where = 'url=$url', vars=locals()).list()
        return len(rows) and rows[0]

        
    def get_frontier(self):
        args = web.storage()
        # get the sections
        sections = self.db.select('objects', group='section', order='section')
        # get last N rows per section
        for section in sections:
            args[section.section] = self.db.select( 'objects', 
                where='section=$section.section', 
                limit= site_globals.posts_per_section, 
                order = 'pub_date desc', vars=locals())
                
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
        

'''
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp

class Objects(db.Model):
  url = db.StringProperty()
  type = db.IntegerProperty()
  section = db.StringProperty()
  pub_date = db.DateTimeProperty(auto_now_add=True)
  author = db.StringProperty()
  title = db.StringProperty()
  content = db.StringProperty(multiline=True)

class GAEDataStoreProvider(object):
    def get_object(self, url):
        res = list(db.GqlQuery("SELECT * FROM Objects WHERE url='%s'" % url))
        if len(res):
            return res[0]
        
    def get_frontier(self):
        return db.GqlQuery("SELECT * FROM Objects LIMIT 100")
        
    def add_object(self, **data):
        Objects(**data).put()
        
    def update_object(self, **data):
        Objects(**data).put()
        
    def get_archive(self, num_of_rows=0):
        sql = "SELECT * FROM Objects ORDER BY pub_date DESC"
        if num_of_rows:
            sql += " LIMIT %d" % num_of_rows
            
        return db.GqlQuery(sql)
'''