
import web

urls = (
    '/(.*)', 'Page',
    '/admin/(*)', 'Admin',
    '/ajax/(*)', 'Ajax',
)

class Admin(object):
    def GET(self, url):
        print web.storage(header='foo', author='foo', pub_date='foo', content='admin')
        
    def POST(self):
        pass
        
class Ajax(object):
    pass
        
class Page(object):
    def GET(self, url=''):
        p = load_page(url)
        print render.base(None)#(render.page(p))
        #print render.page(p)
        
def load_page(url):
    ''' will return the matched url or None '''
    if url == '':
        return load_frontier()
        
    rows= list(web.select('objects', where = 'url=$url', vars=locals()))
    return len(rows) and rows[0]
    
def load_frontier():
    data = web.storage(title='foo', author='foo', pub_date='foo', content='home page')
    return data
    

web.config.db_parameters = dict(dbn='sqlite', db='db/weblishr.db')
web.webapi.internalerror = web.debugerror
web.webapi.notfound = lambda: "page not found"

render = web.template.render('templates/')

if __name__== "__main__":
    web.run(urls, globals(), web.reloader)
