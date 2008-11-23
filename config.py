import web

__all__ = ['site_globals']

site_globals = web.storage(

    site_name='Weblishr', 
    
    title='Weblishr: green publisher',
    
    author = 'Tzury Bar Yochay',
    
    posts_per_section = 7,
    
    username = 'tzury',
    
    password = 'password', 
    
    db_type = 'webpy.db',
)