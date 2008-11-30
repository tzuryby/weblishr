#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import web

__all__ = ['site_globals', 'client_params']


from data import GAEDataStoreProvider
settings = GAEDataStoreProvider().get_settings()

site_globals, client_params = settings.site_globals, settings.client_params
