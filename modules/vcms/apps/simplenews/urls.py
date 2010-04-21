# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 20-03-2010.

from django.conf.urls.defaults import *


urlpatterns = patterns('vcms.apps.simplenews.views',
    (r'^simplenews/(?P<category_slug>.+)/page-(?P<page>\d+)/$', 'list_news'), # /news/finances/page-1/
    url(r'^simplenews/page-(?P<page>\d+)/$', 'list_news', { "category_slug": None }), # /news/page-1/
    (r'^simplenews/(?P<category_slug>.+)/(?P<news_slug>.+)/$', 'single_news'), # /news/finances/year-of-the-linux-desktop/
    (r'^simplenews/(?P<category_slug>.+)/category/(?P<category>.+)/$', 'news_category'), # /news/finances/category/Technology/
    url(r'^simplenews/category/(?P<category>.)/$', 'news_category', { "category_slug": None }), # /news/category/Technology/
    (r'^simplenews/(?P<category_slug>.+)/category/(?P<category>.+)/page-(?P<page>\d+)/$', 'news_category'), # /news/finances/category/Technology/page-1/
    url(r'^simplenews/category/(?P<category>.)/page-(?P<page>\d+)/$', 'news_category', { "category_slug": None }), # /news/category/Technology/page-1/
    #(r'^simplenews/(?P<category_slug>.+)/category/(?P<category>.+).atom$', 'TODO'), # /news/finances/category/Technology.atom
    #url(r'^simplenews/category/(?P<category>.+).atom$', 'TODO', { "category_slug": None }), # /news/category/Technology.atom
    #(r'^simplenews/(?P<category_slug>.+)/category/(?P<category>.+).rss$', 'TODO'), # /news/finances/category/Technology.rss
    #url(r'^simplenews/category/(?P<category>.+).rss$', 'TODO', { "category_slug": None }), # /news/category/Technology.rss
    (r'^simplenews/(?P<category_slug>.+)/archives/(?P<month>\d{2})-(?P<year>\d{4})/$', 'news_archives'), # /news/finances/archives/12-2010/
    url(r'^simplenews/archives/(?P<month>\d{2})-(?P<year>\d{4})/$', 'news_archives', { "category_slug": None }), # /news/archives/12-2010/
    (r'^simplenews/(?P<category_slug>.+)/archives/(?P<month>\d{2})-(?P<year>\d{4})/page-(?P<page>\d+)/$', 'news_archives'), # /news/finances/archives/12-2010/page-1/
    url(r'^simplenews/archives/(?P<month>\d{2})-(?P<year>\d{4})/page-(?P<page>\d+)/$', 'news_archives', { "category_slug": None }), # /news/archives/12-2010/page-1/
    #(r'^simplenews/(?P<category_slug>.+)/archives/(?P<month>\d{2})-(?P<year>\d{4}).atom$', 'TODO'), # /news/finances/archives/12-2010.atom
    #url(r'^simplenews/archives/(?P<month>\d{2})-(?P<year>\d{4}).atom$', 'TODO', { "category_slug": None }), # /news/archives/12-2010.atom
    #(r'^simplenews/(?P<category_slug>.+)/archives/(?P<month>\d{2})-(?P<year>\d{4}).rss$', 'TODO'), # /news/finances/archives/12-2010.rss
    #url(r'^simplenews/archives/(?P<month>\d{2})-(?P<year>\d{4}).rss$', 'TODO', { "category_slug": None }), # /news/archives/12-2010.rss
    #url(r'^simplenews/recent.atom$', 'TODO', { "category_slug": None }), # /news/recent.atom
    #(r'^simplenews/(?P<category_slug>.+)/recent.atom$', 'TODO'), # /news/finances/recent.atom
    #url(r'^simplenews/recent.rss$', 'TODO', { "category_slug": None }), # /news/recent.rss
    #(r'^simplenews/(?P<category_slug>.+)/recent.rss$', 'TODO'), # /news/finances/recent.rss
    (r'^simplenews/(?P<category_slug>.+)/', 'list_news'), # Catchall index page for a category
    url(r'^simplenews/', 'list_news', { "category_slug": None }), # Catchall index page
)
