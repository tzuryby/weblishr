#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from datetime import datetime, date, timedelta
import time
import web
from simplejson import dumps as dump_json
from config import site_globals, client_params


site_globals.ctx = web.ctx

urls = (
    '/ajax/(.*)', 'Ajax',
    '/archive', 'Archive',
    '/feed/(.*)', 'Feed',
    '/login', 'Login',
    '/logout', 'Logout',
    '/(edit|add)/(.*)', 'Editor',
    '/(.*)', 'View',
)

web.webapi.internalerror = web.debugerror
web.template.Template.globals['sorted'] = sorted

db_provider = None

if site_globals.env == 'webpy':
    from data import WebDBProvider
    db_provider = WebDBProvider()
elif site_globals.env == 'gae':
    from data import GAEDataStoreProvider
    db_provider = GAEDataStoreProvider()

notfound = web.webapi.notfound = lambda url: render.notfound(url)
render = web.template.render('templates/')
app = web.application(urls, globals())

web.config._session = web.storage(user=None, previous_url = None)
session = (lambda: web.config._session)()
'''
if web.config.get('_session') is None:
    session = web.session.Session(
        app, web.session.DiskStore('sessions'), 
        {'user': None, 'previous_url': '/'}
    )
    web.config._session = session
else:
    session = web.config._session
'''
def start():    
    if site_globals.env == 'webpy':
        app.run()
    elif site_globals.env == 'gae':
        app.cgirun()
        
def check_permission(fn, *args, **kwargs):
    def proxy(*args, **kwargs):
        if session.get('user'):
            return fn(*args, **kwargs)
        else:
            session.previous_url = web.ctx.path
            web.seeother('/login')
            
    return proxy

class Archive(object):
    def GET(self):
        rows = db_provider.get_archive()
        return base_template(render.archive(rows))
        
class Ajax(object):
    def GET(self, url):
        web.header("Content-Type","X-JSON")
        return dump_json(get_object(url))
        
class Feed(object):
    #datetime.datetime.today().strftime('%a, %d %h %Y %H:%M:%S GMT')
    def GET(self, fmt):
        items = channel = []
        if fmt == 'rss2':
            return self.rss2()
            
    def rss2(self):
        channel = web.storage(title=site_globals.site_name, 
            link = site_globals.url , 
            description = site_globals.title )
            
        items = []
        sections = db_provider.get_frontier()
        for section in sections:
            for item in sections[section]:
                # title, link, description, pubDate, guid
                items.append ( web.storage(
                    title=item.title, 
                    link = site_globals.url + item.url, 
                    pubDate = item.pub_date, 
                    guid = site_globals.url + item.url, 
                    category = item.section,
                    description=item.content))
        web.header("Content-Type","application-xml")
        return render.rss2(channel, items)

def format_gmt(dt):
    return datetime(*time.strptime(dt, "%Y-%m-%d %H:%M:%S")[0:5]).strftime('%a, %d %h %Y %H:%M:%S GMT')

web.template.Template.globals['format_gmt'] = format_gmt

class Editor(object):
    @check_permission
    def GET(self, fn, url):
        page =get_object(url) or notfound(url)
        return edit_template(render.edit(url, page))
        
    @check_permission
    def POST(self, fn, url):
        data = web.input()
        if fn == 'edit':
            data['where'] = 'url=$url'
            data['vars'] = locals()
            db_provider.update_object(**data)
            return web.seeother('/' + url)
            
        elif fn == 'add':
            data['pub_date'] = str(datetime.today())
            db_provider.add_object(**data)
            return web.seeother('/' + data.url)
            
class View(object):
    def GET(self, url=''):
        return base_template(load_page(url))

class Login(object):
    def GET(object):
        return base_template(render.login())
        
    def POST(self):
        input = web.input()
        session.user = valid_login(input.username, input.password)
        if session.get('user'):
            redirect_previous()
        else:
            return web.seeother('/login')
            
class Logout(object):
    def GET(self):
        session.kill()
        return web.redirect('/')
    
def valid_login(username, password):
    return site_globals.username == username and site_globals.password == password

def redirect_previous():
    web.redirect(session.previous_url)
    session.previous_url = None
    
def base_template(page):
    edit_path = None
    if session.get('user'):
        edit_path = web.ctx.path
        edit_path = not (edit_path.startswith('/edit') or 
            edit_path.startswith('/add')) and edit_path[1:]
            
    script = 'window.client_params = %s;' % dump_json(client_params)
    header = render.header(site_globals, session.get('user'), edit_path)
    
    return render.base( header, render.footer(), page, site_globals, script)
    
def edit_template(page):
    edit_path = None
    if session.get('user'):
        edit_path = web.ctx.path # the requested URL
        # do not show edit or add links in 'edit' or 'add' mode
        edit_mode = not edit_path.startswith('/edit') \
                    and not edit_path.startswith('/add') # and edit_path[1:]
    
    header = render.header(site_globals, session.get('user'), edit_mode)
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
    return render.home(web.storage(args))


if __name__== "__main__":
    start()
