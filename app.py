from datetime import date, timedelta
import web

urls = (
    '/edit/(.*)', 'Editor',
    '/(.*)', 'View',
)

web.webapi.internalerror = web.debugerror
notfound = web.webapi.notfound = lambda url: render.notfound(url)
web.template.Template.globals['sorted'] = sorted
db = web.database(dbn='sqlite', db='db/weblishr.db')
site_globals = web.storage(site_name='Weblishr', title='Weblishr: green publisher')

render = web.template.render('templates/')
        
class Editor(object):
    def GET(self, url):
        page =_get_object(url) or notfound(url)
        return base_template(render.edit(page))
        
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
    ''' will return the matched url or None '''
    page = url == '' and  load_frontier() \
        or load_post(url)
    return page or notfound(url)

def _get_object(url):
    rows= db.select('objects', where = 'url=$url', vars=locals()).list()
    o = len(rows) and rows[0]
    return o
    
def load_post(url):
    post =_get_object(url)
    if post:
        return render.post(post)
    
def load_frontier():
    # date and time of the first back day
    dt = (date.today() - timedelta(days= 7)).timetuple()
    since = str(dt[0]) + '-' + str(dt[1]) + '-' + str(dt[2])
    rows = db.select('objects', where = 'pub_date >= $since', vars=locals()).list()
    sections = sorted(set((row.section for row in rows)))
    args = web.storage(
        ((section,[row for row in rows if row.section == section]) for section in sections)
    )
    return render.home(web.storage(args))


if __name__== "__main__":
    web.application(urls, globals()).run()
    