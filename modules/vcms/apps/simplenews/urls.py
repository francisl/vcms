# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 20-03-2010.

from django.conf.urls.defaults import *


urlpatterns = patterns('vcms.apps.simplenews.views',
    (r'page-(?P<page>)/$', 'index'), # /news/page-1/
    (r'(?P<news_id>)/$', 'news_unique'), # /news/1/
    (r'category/(?P<category>\w)/$', 'news_category'), # /news/category/Technology/
    (r'category/(?P<category>\w)/page-(?P<page>)/$', 'news_category'), # /news/category/Technology/page-1/
    #(r'category/(?P<category>\w).atom$', 'TODO'), # /news/category/Technology.atom
    #(r'category/(?P<category>\w).rss$', 'TODO'), # /news/category/Technology.rss
    (r'archives/(?P<month>\d{2})-(?P<year>\d{4})/$', 'news_archive'), # /news/archives/12-2010/
    (r'archives/(?P<month>\d{2})-(?P<year>\d{4})/page-(?P<page>)/$', 'news_archive'), # /news/archives/12-2010/page-1/
    #(r'archives/(?P<month>\d{2})-(?P<year>\d{4}).atom$', 'TODO'), # /news/archives/12-2010.atom
    #(r'archives/(?P<month>\d{2})-(?P<year>\d{4}).rss$', 'TODO'), # /news/archives/12-2010.rss
    #(r'recent.atom$', 'TODO'), # /news/recent.atom
    #(r'recent.rss$', 'TODO'), # /news/recent.rss
    (r'$', 'index'), # Catchall index page
)
