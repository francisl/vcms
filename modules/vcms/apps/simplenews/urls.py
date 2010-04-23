# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 20-03-2010.

from django.conf.urls.defaults import *
from vcms.apps.simplenews.models import APP_SLUGS

urlpatterns_prefix = r'^%s/' % APP_SLUGS

urlpatterns = patterns('vcms.apps.simplenews.views',
    (r'^(?P<category_slug>.+)/page-(?P<page>\d+)/$', 'list_news'), # /news/finances/page-1/
    url(r'^page-(?P<page>\d+)/$', 'list_news', { "category_slug": None }), # /news/page-1/
    (r'^(?P<category_slug>.+)/(?P<news_slug>.+)/$', 'single_news'), # /news/finances/year-of-the-linux-desktop/
    (r'^(?P<category_slug>.+)/tag/(?P<category>.+)/$', 'news_category'), # /news/finances/tag/Technology/
    url(r'^tag/(?P<category>.)/$', 'news_category', { "category_slug": None }), # /news/tag/Technology/
    (r'^(?P<category_slug>.+)/tag/(?P<category>.+)/page-(?P<page>\d+)/$', 'news_category'), # /news/finances/tag/Technology/page-1/
    url(r'^tag/(?P<category>.)/page-(?P<page>\d+)/$', 'news_category', { "category_slug": None }), # /news/tag/Technology/page-1/
    #(r'^(?P<category_slug>.+)/tag/(?P<category>.+).atom$', 'TODO'), # /news/finances/tag/Technology.atom
    #url(r'^tag/(?P<category>.+).atom$', 'TODO', { "category_slug": None }), # /news/tag/Technology.atom
    #(r'^(?P<category_slug>.+)/tag/(?P<category>.+).rss$', 'TODO'), # /news/finances/tag/Technology.rss
    #url(r'^tag/(?P<category>.+).rss$', 'TODO', { "category_slug": None }), # /news/tag/Technology.rss
    (r'^(?P<category_slug>.+)/archives/(?P<month>\d{2})-(?P<year>\d{4})/$', 'news_archives'), # /news/finances/archives/12-2010/
    url(r'^archives/(?P<month>\d{2})-(?P<year>\d{4})/$', 'news_archives', { "category_slug": None }), # /news/archives/12-2010/
    (r'^(?P<category_slug>.+)/archives/(?P<month>\d{2})-(?P<year>\d{4})/page-(?P<page>\d+)/$', 'news_archives'), # /news/finances/archives/12-2010/page-1/
    url(r'^archives/(?P<month>\d{2})-(?P<year>\d{4})/page-(?P<page>\d+)/$', 'news_archives', { "category_slug": None }), # /news/archives/12-2010/page-1/
    #(r'^(?P<category_slug>.+)/archives/(?P<month>\d{2})-(?P<year>\d{4}).atom$', 'TODO'), # /news/finances/archives/12-2010.atom
    #url(r'^archives/(?P<month>\d{2})-(?P<year>\d{4}).atom$', 'TODO', { "category_slug": None }), # /news/archives/12-2010.atom
    #(r'^(?P<category_slug>.+)/archives/(?P<month>\d{2})-(?P<year>\d{4}).rss$', 'TODO'), # /news/finances/archives/12-2010.rss
    #url(r'^archives/(?P<month>\d{2})-(?P<year>\d{4}).rss$', 'TODO', { "category_slug": None }), # /news/archives/12-2010.rss
    #url(r'^recent.atom$', 'TODO', { "category_slug": None }), # /news/recent.atom
    #(r'^(?P<category_slug>.+)/recent.atom$', 'TODO'), # /news/finances/recent.atom
    #url(r'^recent.rss$', 'TODO', { "category_slug": None }), # /news/recent.rss
    #(r'^(?P<category_slug>.+)/recent.rss$', NewsCategoryRssFeed()), # /news/finances/recent.rss
    (r'^(?P<category_slug>.+)/', 'list_news'), # Catchall index page for a category
    url(r'^', 'list_news', { "category_slug": None }), # Catchall index page
)
