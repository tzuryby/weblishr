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
            style_info = css()

            Settings(category_num=2, category_name='Client Settings', item_key='init_wym_editor', title = 'Init WYMEditor', value = '').put()
            Settings(category_num=2, category_name='Client Settings', item_key='lang', title = 'Language', value = 'en').put()
            Settings(category_num=2, category_name='Client Settings', item_key='css', title = 'Site CSS', value = style_info).put()

            Settings(category_num=1, category_name='Global Settings', item_key='site_name', title = 'Site\'s Name', value = 'Weblishr').put()
            Settings(category_num=1, category_name='Global Settings', item_key='title', title = 'Site\'s Title', value = 'weblishr - easy publisher').put()
            Settings(category_num=1, category_name='Global Settings', item_key='url', title = 'Site\'s URL', value = 'http://weblishr.com/').put()
            Settings(category_num=1, category_name='Global Settings', item_key='posts_per_section', title = 'Posts Per Section', value = '7', evaluator='int(%d)').put()
            Settings(category_num=1, category_name='Global Settings', item_key='admins', title = 'Admins', value = 'tzury.by@gmail.com afro.systems@gmail.com', evaluator='"%s".split(" ")').put()
            Settings(category_num=1, category_name='Global Settings', item_key='templates_path', title = 'Templates Path', value = 'templates/').put()
            
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
            
            
def css():
    return '''*{margin:0;padding:0}
html,body{height:100%}
body{background-color:white;font:13.34px helvetica,arial,clean,sans-serif;*font-size:small;text-align:center}
h1,h2,h3,h4,h5,h6{font-size:100%}
h1{margin-bottom:1em}
p{margin:1em 0}
a{color:#00a}
a:hover{color:black}
a:visited{color:#a0a}
table{font-size:inherit;font:100%}
ul.posts{list-style-type:none;margin-bottom:2em}
ul.posts li{line-height:1.75em}
ul.posts span{color:#aaa;font-family:Monaco,"Courier New",monospace;font-size:80%}
.site{font-size:110%;text-align:justify;width:40em;margin:3em auto 2em auto;line-height:1.5em}
.title{color:#a00;font-weight:bold;margin-bottom:2em}
.site .title a{color:#a00;text-decoration:none}
.site .title a:hover{color:black}
.site .title a.extra{color:#aaa;text-decoration:none;margin-left:.5em;margin-right:.5em}
.site .title a.extra:hover{color:black}
.site .meta{color:#aaa}
.site .footer{font-size:80%;color:#666;border-top:4px solid #eee;margin-top:2em;overflow:hidden}
.site .footer .contact{float:left;margin-right:3em}
.site .footer .contact a{color:#8085C1}
.site .footer .rss{margin-top:1.1em;margin-right:-.2em;float:right}
.site .footer .rss img{border:0}
#post{}
#post pre{border:1px solid #ddd;background-color:#eef;padding:0 .4em}
#post code{border:1px solid #ddd;background-color:#eef;font-size:95%;padding:0 .2em}
#post pre code{border:none}
#post pre.terminal{border:1px solid black;background-color:#333;color:white}
#post pre.terminal code{background-color:#333}
#related{margin-top:2em}
#related h2{margin-bottom:1em}
form{padding:8px}
form input[type=text]{width:100%}
form input.w-50{width:50%}
form input.w-25{width:25%}
form textarea{width:100%;height:24em}
.warn{color:#a00}
a.delete{margin-left:24em;color:#a00;text-decoration:none}
a.delete:hover{color:#fff;background-color:#a00;border-bottom:dotted 1px}


ul.tabs-nav{ list-style-image:none; list-style-position:outside; list-style-type:none; }
ul.tabs-nav li{ float:left; margin:0 0 0 1em; border: 1px solid Gray; border-bottom:0px; padding-left: 1em; padding-right: 1em; }
ul.tabs-nav li a { text-decoration:none; }
ul.tabs-nav li.ui-tabs-selected { color: #a00; border: 1px solid #a00; border-bottom:0px;}
ul.tabs-nav li.ui-tabs-selected a { color: #a00; }
.ui-tabs-panel {margin: 4px 0 1em 0; border: 1px solid #a00; padding: 1em}
.ui-tabs-hide { display: none; } '''