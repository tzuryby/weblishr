#!/usr/bin/env python
# -*- coding: UTF-8 -
import web
from google.appengine.ext import db
from google.appengine.ext import webapp

class Settings(db.Model):
  category_num = db.IntegerProperty()
  category_name = db.StringProperty()
  item_key = db.StringProperty()
  title = db.StringProperty()
  value = db.TextProperty()
  validator = db.StringProperty()
  evaluator = db.StringProperty()
  

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
        results = Objects.all()
        sections = set(o.section for o in results)
        # get last N rows per section
        for section in sections:
            args[section] = [row for row in results if row.section == section]
                
        return args
        
    def update_object(self, **data):
        web.debug(data)
        Objects(**data).put()
        
    def get_archive(self, num_of_rows=0):
        sql = "ORDER BY pub_date DESC"
        if num_of_rows:
            sql += " LIMIT %d" % num_of_rows
            
        return Objects.gql(sql)
        
    def delete_object(self, url):
        query = Objects.gql("WHERE url='%s'" % url)
        res = query.fetch(1)
        db.delete(res)
        
    def load_settings(self):
        '''load the setting from the datastore'''
        fetch = lambda: Settings.all() #("ORDER BY category_num, category_name, title")
        result = fetch()
        
        if not result.count():
            f = open('static/css/screen.css')
            style_info = ''.join(line for line in f)
            f.close()

            Settings(category_num=2, category_name='Client Settings', item_key='init_wym_editor', title = 'Init WYMEditor', value = '').put()
            Settings(category_num=2, category_name='Client Settings', item_key='lang', title = 'Language', value = 'en').put()
            Settings(category_num=2, category_name='Client Settings', item_key='css', title = 'Site CSS', value = style_info).put()

            Settings(category_num=1, category_name='Global Settings', item_key='site_name', title = 'Site\'s Name', value = 'Weblishr').put()
            Settings(category_num=1, category_name='Global Settings', item_key='title', title = 'Site\'s Title', value = 'weblishr - easy publisher').put()
            Settings(category_num=1, category_name='Global Settings', item_key='url', title = 'Site\'s URL', value = 'http://weblishr.com/').put()
            Settings(category_num=1, category_name='Global Settings', item_key='posts_per_section', title = 'Posts Per Section', value = '7', evaluator='int(%d)').put()
            Settings(category_num=1, category_name='Global Settings', item_key='admins', title = 'Admins', value = 'tzury.by@gmail.com afro.systems@gmail.com', evaluator='"%s".split(" ")').put()
            
            result = fetch()
        
        return result
        
        
    def get_settings(self):
        '''returns the settings as storage'''
        settings = self.load_settings()
        data = web.storage(site_globals=web.storage(), 
            client_params=web.storage())
        for item in settings:
            if item.category_name == 'Global Settings':
                data.site_globals[item.item_key] = item.value
            elif item.category_name == 'Client Settings':
                data.client_params[item.item_key] = item.value
                
        return data
        
    def save_settings(self, data):
        for k,v in data.iteritems():
            item = Settings.gql("WHERE item_key='" + k + "'").fetch(1)[0]
            item.value = v
            db.put(item)