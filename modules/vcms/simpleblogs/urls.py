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
    ,(r'^(?P<blog_page>[-\w]+)-(?P<page_number>\d+)/date/(?P<year>\d{4})/(?P<month>\d{2}/(?P<day>\d{2})/)$', 'blog_page_for_date')
    ,(r'^(?P<blog_page>[-\w]+)-(?P<page_number>\d+)/date/(?P<year>\d{4})/(?P<month>\d{2}/)$', 'blog_page_for_date')
    ,(r'^(?P<blog_page>[-\w]+)-(?P<page_number>\d+)/date/(?P<year>\d{4})/$', 'blog_page_for_date')
    ,(r'^(?P<blog_page>[-\w]+)-(?P<page_number>\d+)/(?P<category>[-\w]+)$', 'blog_page')
    ,(r'^(?P<blog_page>[-\w]+)-(?P<page_number>\d+)/$', 'blog_page')
    ,(r'^(?P<blog_page>[-\w]+)/date/(?P<year>\d{4})/(?P<month>\d{2}/(?P<day>\d{2})/)$', 'blog_page_for_date')
    ,(r'^(?P<blog_page>[-\w]+)/date/(?P<year>\d{4})/(?P<month>\d{2}/)$', 'blog_page_for_date')
    ,(r'^(?P<blog_page>[-\w]+)/date/(?P<year>\d{4})/$', 'blog_page_for_date')

    ,(r'^(?P<blog_page>[-\w]+)/(?P<category>[-\w]+)/$', 'blog_page')
    ,(r'^(?P<blog_page>[-\w]+)/$', 'blog_page')
    ,(r'^$', 'blog_page')
)
