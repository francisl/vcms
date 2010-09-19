# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 20-03-2010.

from django.conf.urls.defaults import *
#from vcms.simpleblogs.feeds import NewsRssFeed, NewsCategoryRssFeed
from vcms.simpleblogs.models import APP_SLUGS

urlpatterns_prefix = r'^%s/' % APP_SLUGS

urlpatterns = patterns('vcms.simpleblogs.views'
    #,(r'^(?P<page_slug>[-\w]+)-(?P<page_number>\d+)/(?P<category>[-\w]+)/date/(?P<year>\d{4})/(?P<month>\d{1,2}/(?P<day>\d{2})/)$', 'page_for_date')
    #,(r'^(?P<page_slug>[-\w]+)-(?P<page_number>\d+)/(?P<category>[-\w]+)/date/(?P<year>\d{4})/(?P<month>\d{1,2}/)$', 'page_for_date')
    #,(r'^(?P<page_slug>[-\w]+)-(?P<page_number>\d+)/(?P<category>[-\w]+)/date/(?P<year>\d{4})/$', 'page_for_date')
    ,(r'^(?P<page_slug>[-\w]+)-(?P<page_number>\d+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{2})/$', 'page_for_date')
    ,(r'^(?P<page_slug>[-\w]+)-(?P<page_number>\d+)/(?P<year>\d{4})/(?P<month>\d{1,2})/$', 'page_for_date')
    ,(r'^(?P<page_slug>[-\w]+)-(?P<page_number>\d+)/(?P<year>\d{4})/$', 'page_for_date')
    
    ,(r'^(?P<page_slug>[-\w]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{2})/$', 'page_for_date')
    ,(r'^(?P<page_slug>[-\w]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/$', 'page_for_date')
    ,(r'^(?P<page_slug>[-\w]+)/(?P<year>\d{4})/$', 'page_for_date')
    
    ,(r'^(?P<page_slug>[-\w]+)-(?P<page_number>\d+)/(?P<category>[-\w]+)/$', 'page')
    ,(r'^(?P<page_slug>[-\w]+)/(?P<category>[-\w]+)/$', 'page')
    ,(r'^(?P<page_slug>[-\w]+)-(?P<page_number>\d+)/$', 'page')
    
    ,(r'^(?P<page_slug>[-\w]+)/$', 'page')
    ,(r'^$', 'page')
)
