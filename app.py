from datetime import date, timedelta
import web

urls = (
    '/(.*)', 'Page',
    '/admin/(*)', 'Admin',
    '/ajax/(*)', 'Ajax',
)

class Admin(object):
    def GET(self, url):
        pass #return web.storage(header='foo', author='foo', pub_date='foo', content='admin')
        
    def POST(self):
        pass
        
class Ajax(object):
    pass
        
class Page(object):
    def GET(self, url=''):
        return base_template(load_page(url))
        
def base_template(page):
    return render.base(
        render.header(site_globals), 
        render.footer(), 
        page, 
        site_globals)
    
def load_post(url):
    rows= db.select('objects', where = 'url=$url', vars=locals()).list()
    p = len(rows) and rows[0]
    if p:
        return render.post(p, None)
        
def load_page(url):
    ''' will return the matched url or None '''
    return url == '' and  load_frontier() \
        or load_post(url)
    
    
def load_frontier():
    # date and time of the first back day
    dt = (date.today() - timedelta(days= 7)).timetuple()
    since = str(dt[0]) + '-' + str(dt[1]) + '-' + str(dt[2])
    rows = db.select('objects', where = 'pub_date >= $since', vars=locals()).list()
    args = web.storage()
    sections = set((row.section for row in rows))
    for section in sections:
        args[section] = [row for row in rows if row.section == section]

    return render.home(web.storage(args))

web.webapi.internalerror = web.debugerror
web.webapi.notfound = lambda: "page not found"

db = web.database(dbn='sqlite', db='db/weblishr.db')
site_globals = web.storage(site_name='Weblishr', title='Weblishr: green publisher')

render = web.template.render('templates/')

if __name__== "__main__":
    web.application(urls, globals()).run()
    