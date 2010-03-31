# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 20-03-2010.

from django.conf.urls.defaults import *


urlpatterns = patterns('vcms.apps.simplenews.views',
    (r'^news/(?P<category_slug>\w+)/page-(?P<page>\d+)/$', 'news_index'), # /news/finances/page-1/
    url(r'^news/page-(?P<page>\d+)/$', 'news_index', { "category_slug": None }), # /news/page-1/
    (r'^news/(?P<category_slug>\w+)/(?P<news_slug>)/$', 'news_unique'), # /news/finances/year-of-the-linux-desktop/
    (r'^news/(?P<category_slug>\w+)/category/(?P<category>\w)/$', 'news_category'), # /news/finances/category/Technology/
    url(r'^news/category/(?P<category>\w)/$', 'news_category', { "category_slug": None }), # /news/category/Technology/
    (r'^news/(?P<category_slug>\w+)/category/(?P<category>\w)/page-(?P<page>\d+)/$', 'news_category'), # /news/finances/category/Technology/page-1/
    url(r'^news/category/(?P<category>\w)/page-(?P<page>\d+)/$', 'news_category', { "category_slug": None }), # /news/category/Technology/page-1/
    #(r'^news/(?P<category_slug>\w+)/category/(?P<category>\w).atom$', 'TODO'), # /news/finances/category/Technology.atom
    #url(r'^news/category/(?P<category>\w).atom$', 'TODO', { "category_slug": None }), # /news/category/Technology.atom
    #(r'^news/(?P<category_slug>\w+)/category/(?P<category>\w).rss$', 'TODO'), # /news/finances/category/Technology.rss
    #url(r'^news/category/(?P<category>\w).rss$', 'TODO', { "category_slug": None }), # /news/category/Technology.rss
    (r'^news/(?P<category_slug>\w+)/archives/(?P<month>\d{2})-(?P<year>\d{4})/$', 'news_archives'), # /news/finances/archives/12-2010/
    url(r'^news/archives/(?P<month>\d{2})-(?P<year>\d{4})/$', 'news_archives', { "category_slug": None }), # /news/archives/12-2010/
    (r'^news/(?P<category_slug>\w+)/archives/(?P<month>\d{2})-(?P<year>\d{4})/page-(?P<page>\d+)/$', 'news_archives'), # /news/finances/archives/12-2010/page-1/
    url(r'^news/archives/(?P<month>\d{2})-(?P<year>\d{4})/page-(?P<page>\d+)/$', 'news_archives', { "category_slug": None }), # /news/archives/12-2010/page-1/
    #(r'^news/(?P<category_slug>\w+)/archives/(?P<month>\d{2})-(?P<year>\d{4}).atom$', 'TODO'), # /news/finances/archives/12-2010.atom
    #url(r'^news/archives/(?P<month>\d{2})-(?P<year>\d{4}).atom$', 'TODO', { "category_slug": None }), # /news/archives/12-2010.atom
    #(r'^news/(?P<category_slug>\w+)/archives/(?P<month>\d{2})-(?P<year>\d{4}).rss$', 'TODO'), # /news/finances/archives/12-2010.rss
    #url(r'^news/archives/(?P<month>\d{2})-(?P<year>\d{4}).rss$', 'TODO', { "category_slug": None }), # /news/archives/12-2010.rss
    #url(r'^news/recent.atom$', 'TODO', { "category_slug": None }), # /news/recent.atom
    #(r'^news/(?P<category_slug>\w+)/recent.atom$', 'TODO'), # /news/finances/recent.atom
    #url(r'^news/recent.rss$', 'TODO', { "category_slug": None }), # /news/recent.rss
    #(r'^news/(?P<category_slug>\w+)/recent.rss$', 'TODO'), # /news/finances/recent.rss
    (r'^news/(?P<category_slug>\w+)/', 'news_index'), # Catchall index page for a category
    url(r'^news/', 'news_index', { "category_slug": None }), # Catchall index page
)
