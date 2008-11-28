#!/usr/bin/env python
# -*- coding: UTF-8 -
import web
from google.appengine.ext import db
from google.appengine.ext import webapp

class Objects(db.Model):
  url = db.StringProperty()
  type = db.IntegerProperty()
  section = db.StringProperty()
  pub_date = db.StringProperty()
  author = db.StringProperty()
  title = db.StringProperty()
  content = db.TextProperty() #multiline=True

class GAEDataStoreProvider(object):
    def get_object(self, url):
        res = list(db.GqlQuery("SELECT * FROM Objects WHERE url='%s'" % url))
        if len(res):
            return res[0]
        
    def get_frontier(self):
        args = web.storage()
        # get the sections
        results = db.GqlQuery("SELECT * FROM Objects")
        sections = set(o.section for o in results)
        # get last N rows per section
        for section in sections:
            args[section] = [row for row in results if row.section == section]
                
        return args
        
    def update_object(self, **data):
        web.debug(data)
        Objects(**data).put()
        
    def get_archive(self, num_of_rows=0):
        sql = "SELECT * FROM Objects ORDER BY pub_date DESC"
        if num_of_rows:
            sql += " LIMIT %d" % num_of_rows
            
        return db.GqlQuery(sql)
        
    def delete_object(self, url):
        query = db.GqlQuery("SELECT * FROM Objects WHERE url='%s'" % url)
        res = query.fetch(1)
        db.delete(res)
