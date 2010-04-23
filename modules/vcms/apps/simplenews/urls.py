# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 20-03-2010.

from django.conf.urls.defaults import *
from vcms.apps.simplenews.feeds import NewsCategoryRssFeed
from vcms.apps.simplenews.models import APP_SLUGS

urlpatterns_prefix = r'^%s/' % APP_SLUGS

urlpatterns = patterns('vcms.apps.simplenews.views',
    (r'^(?P<category_slug>.+)/page-(?P<page>\d+)/$', 'list_news'), # /simplenews/finances/page-1/
    url(r'^page-(?P<page>\d+)/$', 'list_news', { "category_slug": None }), # /simplenews/page-1/
    (r'^(?P<category_slug>.+)/(?P<news_slug>.+)/$', 'single_news'), # /simplenews/finances/year-of-the-linux-desktop/
    (r'^(?P<category_slug>.+)/tag/(?P<category>.+)/$', 'news_category'), # /simplenews/finances/tag/Technology/
    url(r'^tag/(?P<category>.)/$', 'news_category', { "category_slug": None }), # /simplenews/tag/Technology/
    (r'^(?P<category_slug>.+)/tag/(?P<category>.+)/page-(?P<page>\d+)/$', 'news_category'), # /simplenews/finances/tag/Technology/page-1/
    url(r'^tag/(?P<category>.)/page-(?P<page>\d+)/$', 'news_category', { "category_slug": None }), # /simplenews/tag/Technology/page-1/
    #(r'^(?P<category_slug>.+)/tag/(?P<category>.+).atom$', 'TODO'), # /simplenews/finances/tag/Technology.atom
    #url(r'^tag/(?P<category>.+).atom$', 'TODO', { "category_slug": None }), # /simplenews/tag/Technology.atom
    #(r'^(?P<category_slug>.+)/tag/(?P<category>.+).rss$', 'TODO'), # /simplenews/finances/tag/Technology.rss
    #url(r'^tag/(?P<category>.+).rss$', 'TODO', { "category_slug": None }), # /simplenews/tag/Technology.rss
    (r'^(?P<category_slug>.+)/archives/(?P<month>\d{2})-(?P<year>\d{4})/$', 'news_archives'), # /simplenews/finances/archives/12-2010/
    url(r'^archives/(?P<month>\d{2})-(?P<year>\d{4})/$', 'news_archives', { "category_slug": None }), # /simplenews/archives/12-2010/
    (r'^(?P<category_slug>.+)/archives/(?P<month>\d{2})-(?P<year>\d{4})/page-(?P<page>\d+)/$', 'news_archives'), # /simplenews/finances/archives/12-2010/page-1/
    url(r'^archives/(?P<month>\d{2})-(?P<year>\d{4})/page-(?P<page>\d+)/$', 'news_archives', { "category_slug": None }), # /simplenews/archives/12-2010/page-1/
    #(r'^(?P<category_slug>.+)/archives/(?P<month>\d{2})-(?P<year>\d{4}).atom$', 'TODO'), # /simplenews/finances/archives/12-2010.atom
    #url(r'^archives/(?P<month>\d{2})-(?P<year>\d{4}).atom$', 'TODO', { "category_slug": None }), # /simplenews/archives/12-2010.atom
    #(r'^(?P<category_slug>.+)/archives/(?P<month>\d{2})-(?P<year>\d{4}).rss$', 'TODO'), # /simplenews/finances/archives/12-2010.rss
    #url(r'^archives/(?P<month>\d{2})-(?P<year>\d{4}).rss$', 'TODO', { "category_slug": None }), # /simplenews/archives/12-2010.rss
    #url(r'^recent.atom$', 'TODO', { "category_slug": None }), # /simplenews/recent.atom
    #(r'^(?P<category_slug>.+)/recent.atom$', 'TODO'), # /simplenews/finances/recent.atom
    #url(r'^recent.rss$', 'TODO', { "category_slug": None }), # /simplenews/recent.rss
    (r'^(?P<category_slug>.+).rss$', NewsCategoryRssFeed()), # /simplenews/finances/recent.rss
    (r'^(?P<category_slug>.+)/', 'list_news'), # Catchall index page for a category
    url(r'^', 'list_news', { "category_slug": None }), # Catchall index page
)
