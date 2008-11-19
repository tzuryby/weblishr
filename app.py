import web

render = web.template.render('templates/')

urls = (
    '/admin(*)', 'admin_processor',
    '/(*)', 'site_processor'
)

class admin_processor:
    def GET(self, url='/admin'):
        print 'Hello'
        
    def POST(self):
        pass
        
class site_processor:
    def GET(self, url='/'):
        print render.imagePage("Enter Your Value")
        
    def POST(self):
        i = web.input()
        web.debug(i)
        web.seeother('/r')
        
        
web.webapi.internalerror = web.debugerror
if __name__== "__main__":
    web.run(urls, globals(), web.reloader)
