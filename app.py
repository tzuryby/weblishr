#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from datetime import date, timedelta
import web
from simplejson import dumps as dump_json
from config import site_globals, client_params
from data import WebDBProvider

site_globals.ctx = web.ctx

urls = (
    '/ajax/(.*)', 'Ajax',
    '/archive', 'Archive',
    '/login', 'Login',
    '/logout', 'Logout',
    '/(edit|add)/(.*)', 'Editor',
    '/(.*)', 'View',
)

web.webapi.internalerror = web.debugerror
web.template.Template.globals['sorted'] = sorted
db_provider = None

if site_globals.db_env == 'webpy.db':
    db_provider = WebDBProvider()
elif site_globals.db_env == 'gae.datastore':
    db_provider = GAEDataStoreProvider()

notfound = web.webapi.notfound = lambda url: render.notfound(url)
render = web.template.render('templates/')
app = web.application(urls, globals())

if web.config.get('_session') is None:
    session = web.session.Session(
        app, web.session.DiskStore('sessions'), 
        {'user': None, 'previous_url': '/'}
    )
    web.config._session = session
else:
    session = web.config._session

def start():
    app.run()

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
            
        elif fn == 'add':
            data['pub_date'] = str(date.today())
            db_provider.add_object(**data)
            
        web.seeother('/' + url)
        
class View(object):
    def GET(self, url=''):
        return base_template(load_page(url))

class Login(object):
    def GET(object):
        return base_template(render.login())
        
    def POST(self):
        input = web.input()
        session.get('user') = valid_login(input.username, input.password)
        if session.get('user'):
            redirect_previous()
        else:
            web.seeother('/login')
class Logout(object):
    def GET(self):
        session.kill()
        web.redirect('/')
    
def valid_login(username, password):
    return site_globals.username == username and site_globals.password == password

def redirect_previous():
    url = session.previous_url
    web.redirect(url)
    session.previous_url = None
    
def base_template(page):
    edit_path = None
    if session.get('user'):
        edit_path = web.ctx.path
        edit_path = not (edit_path.startswith('/edit') or 
            edit_path.startswith('/add')) and edit_path[1:]
            
    register_script = 'window.client_params = %s;' % dump_json(client_params)
    
    return render.base(
        render.header(site_globals, session.get('user'), edit_path), 
        render.footer(), 
        page, 
        site_globals,
        register_script)
    
def edit_template(page):
    edit_path = None
    if session.get('user'):
        edit_path = web.ctx.path
        edit_path = not (edit_path.startswith('/edit') or 
            edit_path.startswith('/add')) and edit_path[1:]
    return render.editor(
        render.header(site_globals, session.get('user'), edit_path), 
        render.footer(), 
        page, 
        site_globals,
        'window.client_params = %s;' % dump_json(client_params))
        
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