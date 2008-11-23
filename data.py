import web
from config import site_globals
'''data layer'''

class Provider(object):
    ''' base class for providers
        there are:
            WebDBProvider   -> webpy db abstraction layer
            GAEProvider     -> Google App Engine Data API
    '''
    def get_object(url):
        raise NotImplemented
        
    def get_frontier(sections_items):
        raise NotImplemented
        
    def add_object(**data):
        raise NotImplemented
        
    def update_object(**data):
        raise NotImplemented
        
class WebDBProvider(Provider):
    def __init__(self, db):
        self.db = db
        
    def get_object(self, url):
        '''first (and only) row OR 0'''
        rows= self.db.select('objects', where = 'url=$url', vars=locals()).list()
        return len(rows) and rows[0]

        
    def get_frontier(self):
        args = web.storage()
        # get the sections
        sections = self.db.select('objects', group='section', order='section')
        # get last N rows per section
        for section in sections:
            args[section.section] = self.db.select(
                'objects', where='section="%s"' % section.section, 
                limit= site_globals.posts_per_section, order = 'pub_date desc')
                
        return args
        
    def add_object(self, **data):
        self.db.insert('objects', **data)
        
    def update_object(self, **data):
        self.db.update('objects', **data)
    