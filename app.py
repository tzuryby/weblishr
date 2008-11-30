#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import datetime
from datetime import date, timedelta
import time
from pprint import pformat

import web

from google.appengine.api import users

from simplejson import dumps as dump_json
from config import site_globals, client_params
from data import GAEDataStoreProvider

db_provider = GAEDataStoreProvider()
site_globals.ctx = web.ctx
web.template.Template.globals['sorted'] = sorted
notfound = web.webapi.notfound = lambda url: render.notfound(url)
render = web.template.render(site_globals.templates_path)

urls = (
    '/sandbox', 'sandbox',
    '/ajax/(.*)', 'Ajax',
    '/archive', 'Archive',
    '/settings', 'Settings',
    '/feed/(.*)', 'Feed',
    '/login', 'Login',
    '/logout', 'Logout',
    '/(edit)/(.*)', 'Editor',
    '/(add)/(.*)', 'Editor',
    '/delete/(.*)', 'Delete',
    '/(.*)', 'View',
)

app = web.application(urls, globals())
logout_url = users.create_logout_url('/')
login_url = users.create_login_url('/')

def check_permission(fn, *args, **kwargs):
    def proxy(*args, **kwargs):
        if is_admin():
            return fn(*args, **kwargs)
        else:
            web.seeother(users.create_login_url(web.ctx.path))
            
    return proxy
    
class Archive(object):
    def GET(self):
        rows = db_provider.get_archive()
        return base_template(render.archive(rows))
        
class Ajax(object):
    def GET(self, url):
        web.header("Content-Type","X-JSON")
        object = get_object(url)
        key_name = object.key().name()
        object = eval(pformat(object._entity))
        object['key_name'] = key_name
        return dump_json(object)
        
class Feed(object):
    def GET(self, fmt):
        items = channel = []
        if fmt == 'rss2':
            return self.rss2()
        
    def rss2(self):
        sections = db_provider.get_frontier()
        from pyrssgen import RSS2, RSSItem
        items = []
        for section in sections:
            for item in sections[section]:
                items.append(
                    RSSItem(title=item.title, 
                        link = site_globals.url + item.url, 
                        pubDate = item.pub_date, 
                        author = item.author,
                        categories = [item.section,],
                        guid = site_globals.url + item.url, 
                        description=item.content))
                        
        rss = RSS2(
            title=site_globals.site_name, 
            link = site_globals.url , 
            description = site_globals.title,
            
            items = items
            
        )
        web.header("Content-Type","application-xml")
        return render.rss2(rss.to_xml())
        
class Editor(object):
    
    @check_permission
    def GET(self, fn, url):
        key_name = None
        if fn == 'add':
            import uuid
            key_name = 'article-' + uuid.uuid4().hex
        return edit_template(render.edit(url, key_name))
        
    @check_permission
    def POST(self, fn, url):
        data = web.input(url=url)
        if fn == 'edit':
            db_provider.update_object(**data)
            return web.seeother('/' + url)
            
        elif fn == 'add':
            data['pub_date'] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            db_provider.update_object(**data)
            return web.seeother('/' + data.url)
            
class Settings(object):
    
    @check_permission
    def GET(self):
        return base_template(render.settings(self.group_settings()))
        
    def group_settings(self):
        settings = [item for item in db_provider.load_settings()]
        web.debug(settings)
        data = web.storage()
        categories = sorted(set((item.category_num, item.category_name) for item in settings))
        web.debug(categories)
        
        for category in categories:
            data[category[1]] = [item for item in settings if item.category_num == category[0]]
        
        web.debug(data)
        return data
        
    @check_permission
    def POST(self):
        db_provider.save_settings(web.input())
        web.seeother('/')
        
class View(object):
    def GET(self, url=''):
        return base_template(load_page(url))
            
class Delete(object):
    @check_permission
    def GET(self, url):
        return base_template(render.delete(url))
                
    @check_permission
    def POST(self, url):
        db_provider.delete_object(url)
        web.seeother('/')
        
class Logout(object):
    def GET(self):
        return web.redirect(logout_url)

class Login(object):
    def GET(self):
        return web.redirect(login_url)

def base_template(page):        
    script = 'window.client_params = %s;' % dump_json(client_params)
    header = render.header(site_globals, is_admin(), view_editor())
    #
    return render.base( header, render.footer(), page, site_globals, script, client_params.css)
    
def edit_template(page):
    header = render.header(site_globals, is_admin(), view_editor())
    footer = render.footer()
    script = 'window.client_params = %s;' % dump_json(client_params)
    
    return render.editor(header, footer, page, site_globals, script)
        
def load_page(url):
    '''homepage OR matched url OR not-found'''
    return (url == '' and load_frontier() or load_post(url)) or notfound(url)

def get_object(url):
    return db_provider.get_object(url)
    
def load_post(url):
    post = get_object(url)
    return post and render.post(post)
    
def load_frontier():
    args = db_provider.get_frontier()
    return render.home(args)
    #return render.home(web.storage(args))

def view_editor():
    if is_admin():
        path = web.ctx.path # the requested URL
        if path.startswith('/edit/') \
            or path.startswith('/add/') \
            or path.startswith('/delete/') \
            or path in urls:
            return False
        else:
            return path[1:]
            
def is_admin(user=users.get_current_user()):
    return user and user.email().lower() in site_globals.admins

class sandbox():
    def GET(self):
        data= dir(users.get_current_user())
        if data:
            for d in data:
                yield str(d) + '\n'
                
            yield str(users.get_current_user().email())
        
def send_mail(_subject, _body):
    from google.appengine.api import mail
    data = web.input()
    _from = site_globals.sender_address
    _to = data.to
    if mail.is_email_valid(user_address):
        mail.send_mail(_from, _to, _subject, _body)
        
def start():    
    app.cgirun()

if __name__== "__main__":  
    start()
