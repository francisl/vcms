# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 20-03-2010.

from django.conf.urls.defaults import *


urlpatterns = patterns('vcms.apps.simplenews.views',
    (r'^news/page-(?P<page>)/$', 'news_index'), # /news/page-1/
    (r'^news/(?P<news_slug>)/$', 'news_unique'), # /news/year-of-the-linux-desktop/
    (r'^news/category/(?P<category>\w)/$', 'news_category'), # /news/category/Technology/
    (r'^news/category/(?P<category>\w)/page-(?P<page>)/$', 'news_category'), # /news/category/Technology/page-1/
    #(r'^news/category/(?P<category>\w).atom$', 'TODO'), # /news/category/Technology.atom
    #(r'^news/category/(?P<category>\w).rss$', 'TODO'), # /news/category/Technology.rss
    (r'^news/archives/(?P<month>\d{2})-(?P<year>\d{4})/$', 'news_archives'), # /news/archives/12-2010/
    (r'^news/archives/(?P<month>\d{2})-(?P<year>\d{4})/page-(?P<page>)/$', 'news_archives'), # /news/archives/12-2010/page-1/
    #(r'^news/archives/(?P<month>\d{2})-(?P<year>\d{4}).atom$', 'TODO'), # /news/archives/12-2010.atom
    #(r'^news/archives/(?P<month>\d{2})-(?P<year>\d{4}).rss$', 'TODO'), # /news/archives/12-2010.rss
    #(r'^news/recent.atom$', 'TODO'), # /news/recent.atom
    #(r'^news/recent.rss$', 'TODO'), # /news/recent.rss
    (r'^news/', 'news_index'), # Catchall index page
)
