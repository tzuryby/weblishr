
import web

urls = (
    '/(.*)', 'Page',
    '/admin/(*)', 'Admin',
    '/ajax/(*)', 'Ajax',
)

class Admin(object):
    def GET(self, url):
        return web.storage(header='foo', author='foo', pub_date='foo', content='admin')
        
    def POST(self):
        pass
        
class Ajax(object):
    pass
        
class Page(object):
    def GET(self, url=''):
        p = load_page(url)
        return base_template(render.post(p, None))
        
def base_template(page):
    return render.base(
        render.header(site_globals), 
        render.footer(), 
        page, 
        site_globals)
    
def load_page(url):
    ''' will return the matched url or None '''
    if url == '':
        return load_frontier()
        
    rows= db.select('objects', where = 'url=$url', vars=locals()).list()
    return len(rows) and rows[0]
    
def load_frontier():
    data = web.storage(title='foo', author='foo', pub_date='foo', content='home page')
    return data

web.webapi.internalerror = web.debugerror
web.webapi.notfound = lambda: "page not found"

db = web.database(dbn='sqlite', db='db/weblishr.db')
site_globals = web.storage(site_name='Weblishr', title='Weblishr: green publisher')

render = web.template.render('templates/')

if __name__== "__main__":
    web.application(urls, globals()).run()
    