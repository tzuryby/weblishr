from datetime import date, timedelta
import web
#from simplejson import dumps as dump_json
from config import site_globals

urls = (
    #'/ajax/(.*)', 'Ajax',
    '/archive/(.*)', 'Archive',
    '/(edit|add)/(.*)', 'Editor',
    '/(.*)', 'View',
)

web.webapi.internalerror = web.debugerror
web.template.Template.globals['sorted'] = sorted
db = web.database(dbn='sqlite', db='db/weblishr.db')
notfound = web.webapi.notfound = lambda url: render.notfound(url)
render = web.template.render('templates/')
        
class Editor(object):
    def GET(self, fn, url):
        page =_get_object(url) or notfound(url)
        return base_template(render.edit(url, page))
        
    def POST(self, fn, url):
        data = web.input()
        #del data['_content']
        web.debug(data)
        if fn == 'edit':
            data['where'] = 'url=$url'
            data['vars'] = locals()
            db.update('objects', **data)
        elif fn == 'add':
            data['pub_date'] = str(date.today())
            db.insert('objects', **data)
            
        web.seeother('/' + url)
        
class View(object):
    def GET(self, url=''):
        return base_template(load_page(url))
        
def base_template(page):
    return render.base(
        render.header(site_globals), 
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
    web.application(urls, globals()).run()
    