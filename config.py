#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import web

__all__ = ['site_globals']

site_globals = web.storage(

    site_name= 'Weblishr',
    
    title='weblishr - easy publisher',
    
    url = 'http://localhost:8080/',
    
    posts_per_section = 7,
    
    admins = ('afro.systems@gmail.com', 'tzury.by@gmail.com', 'muledriver@gmail.com')
    
)

# these values are stored under window.client_params
client_params = web.storage(
    init_wym_editor = '',
    #init_wym_editor = '<div dir="rtl"><p>הזן טקסט</p></div>',
    
    lang = 'en',

    default_author = 'Tzury Bar Yochay'
)