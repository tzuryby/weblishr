from datetime import date, timedelta
import web
from simplejson import dumps as dump_json
from config import site_globals


site_globals.ctx = web.ctx

urls = (
    '/ajax/(.*)', 'Ajax',
    '/archive/(.*)', 'Archive',
    '/login', 'Login',
    '/logout', 'Logout',
    '/(edit|add)/(.*)', 'Editor',
    '/(.*)', 'View',
)

web.webapi.internalerror = web.debugerror
web.template.Template.globals['sorted'] = sorted
db = web.database(dbn='sqlite', db='db/weblishr.db')

web.config.db_type = 'webpy.db'

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
        if session.user:
            return fn(*args, **kwargs)
        else:
            session.previous_url = web.ctx.path
            web.seeother('/login')
            
    return proxy
    
class Ajax(object):
    def GET(self, url):
        web.header("Content-Type","X-JSON")
        return dump_json(_get_object(url))
        
class Editor(object):
    
    @check_permission
    def GET(self, fn, url):
        page =_get_object(url) or notfound(url)
        return edit_template(render.edit(url, page))
        
    @check_permission
    def POST(self, fn, url):
        data = web.input()
        if fn == 'edit':
            data['where'] = 'url=$url'
            data['vars'] = locals()
            fn = db.update
        elif fn == 'add':
            data['pub_date'] = str(date.today())
            fn = db.insert
            
        fn('objects', **data)
        web.seeother('/' + url)
        
class View(object):
    def GET(self, url=''):
        return base_template(load_page(url))

class Login(object):
    def GET(object):
        return base_template(render.login())
        
    def POST(self):
        input = web.input()
        session.user = valid_login(input.username, input.password)
        if session.user:
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
    if session.user:
        edit_path = web.ctx.path
        edit_path = not (edit_path.startswith('/edit') or 
            edit_path.startswith('/add')) and edit_path[1:]
    return render.base(
        render.header(site_globals, session.user, edit_path), 
        render.footer(), 
        page, 
        site_globals)
    
def edit_template(page):
    edit_path = None
    if session.user:
        edit_path = web.ctx.path
        edit_path = not (edit_path.startswith('/edit') or 
            edit_path.startswith('/add')) and edit_path[1:]
    return render.editor(
        render.header(site_globals, session.user, edit_path), 
        render.footer(), 
        page, 
        site_globals)
        
def load_page(url):
    '''homepage OR matched url OR not-found'''
    return (url == '' and load_frontier() or load_post(url)) or notfound(url)

def _get_object(url):
    '''first (and only) row OR 0'''
    rows= db.select('objects', where = 'url=$url', vars=locals()).list()
    return len(rows) and rows[0]
    
def load_post(url):
    post =_get_object(url)
    return post and render.post(post)
    
def load_frontier():
    args = web.storage()
    # get the sections
    sections = db.select('objects', group='section', order='section')
    # get last 7 rows per section
    for section in sections:
        args[section.section] = db.select(
            'objects', where='section="%s"' % section.section, 
            limit= site_globals.posts_per_section)
            
    return render.home(web.storage(args))


if __name__== "__main__":
    start()