# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 20-03-2010.

from django.conf.urls.defaults import *
from vcms.simplenews.feeds import NewsRssFeed, NewsCategoryRssFeed
from vcms.simplenews.models import APP_SLUGS


urlpatterns_prefix = r'^%s/' % APP_SLUGS

urlpatterns = patterns('vcms.simplenews.views',
    (r'^(?P<category_slug>.+)/page-(?P<page>\d+)/$', 'list_news'), # ^/finances/page-1/
    url(r'^page-(?P<page>\d+)/$', 'list_news', { "category_slug": None }), # ^/page-1/
    (r'^(?P<category_slug>.+)/(?P<news_slug>.+)/$', 'single_news'), # ^/finances/year-of-the-linux-desktop/
    (r'^(?P<category_slug>.+)/tag/(?P<category>.+)/$', 'news_category'), # ^/finances/tag/Technology/
    url(r'^tag/(?P<category>.)/$', 'news_category', { "category_slug": None }), # ^/tag/Technology/
    (r'^(?P<category_slug>.+)/tag/(?P<category>.+)/page-(?P<page>\d+)/$', 'news_category'), # ^/finances/tag/Technology/page-1/
    url(r'^tag/(?P<category>.)/page-(?P<page>\d+)/$', 'news_category', { "category_slug": None }), # ^/tag/Technology/page-1/
    #(r'^(?P<category_slug>.+)/tag/(?P<category>.+).atom$', 'TODO'), # ^/finances/tag/Technology.atom
    #url(r'^tag/(?P<category>.+).atom$', 'TODO', { "category_slug": None }), # ^/tag/Technology.atom
    #(r'^(?P<category_slug>.+)/tag/(?P<category>.+).rss$', 'TODO'), # ^/finances/tag/Technology.rss
    #url(r'^tag/(?P<category>.+).rss$', 'TODO', { "category_slug": None }), # ^/tag/Technology.rss
    # Archive
    (r'^/archives/(?P<year>\d{4})/$', 'news_archives', { "category_slug": None }), #^/archives/2010/
    (r'^(?P<category_slug>.+)/archives/(?P<year>\d{4})/$', 'news_archives'), # ^/finances/archives/2010/
    (r'^(?P<category_slug>.+)/archives/(?P<month>\d{2})-(?P<year>\d{4})/$', 'news_archives'), # ^/finances/archives/12-2010/
    url(r'^archives/(?P<month>\d{2})-(?P<year>\d{4})/$', 'news_archives', { "category_slug": None }), # ^/archives/12-2010/
    (r'^(?P<category_slug>.+)/archives/(?P<month>\d{2})-(?P<year>\d{4})/page-(?P<page>\d+)/$', 'news_archives'), # ^/finances/archives/12-2010/page-1/
    url(r'^archives/(?P<month>\d{2})-(?P<year>\d{4})/page-(?P<page>\d+)/$', 'news_archives', { "category_slug": None }), # ^/archives/12-2010/page-1/
    #(r'^(?P<category_slug>.+)/archives/(?P<month>\d{2})-(?P<year>\d{4}).atom$', 'TODO'), # ^/finances/archives/12-2010.atom
    #url(r'^archives/(?P<month>\d{2})-(?P<year>\d{4}).atom$', 'TODO', { "category_slug": None }), # ^/archives/12-2010.atom
    #url(r'^recent.atom$', 'TODO', { "category_slug": None }), # ^/recent.atom
    #(r'^(?P<category_slug>.+)/recent.atom$', 'TODO'), # ^/finances/recent.atom
    url(r'^recent.rss$', NewsRssFeed(), name='vcms.simplenews.views.news.recent.rss'), # ^/recent.rss
    url(r'^(?P<month>\d{2})-(?P<year>\d{4}).rss$', NewsRssFeed(), name='vcms.simplenews.views.news.recent.rss'), # ^/01-2010.rss
    url(r'^(?P<year>\d{4}).rss$', NewsRssFeed(), name='vcms.simplenews.views.news.recent.rss'), # ^/2010.rss
    url(r'^(?P<category_slug>.+)/recent.rss$', NewsCategoryRssFeed(), name='vcms.simplenews.views.newscategory.recent.rss'), # ^/finances/recent.rss
    url(r'^(?P<category_slug>.+)/(?P<month>\d{2})-(?P<year>\d{4}).rss$', NewsCategoryRssFeed(), name='vcms.simplenews.views.newscategory.recent.rss'), # ^/finances/01-2010.rss
    url(r'^(?P<category_slug>.+)/(?P<year>\d{4}).rss$', NewsCategoryRssFeed(), name='vcms.simplenews.views.newscategory.recent.rss'), # ^/finances/2010.rss
    (r'^(?P<category_slug>.+)/', 'list_news'), # Catchall index page for a category
    url(r'^', 'list_news', { "category_slug": None }), # Catchall index page
)
