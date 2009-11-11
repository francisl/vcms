# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie

from django.conf.urls.defaults import *
from django.conf import settings
from vimba_cms.apps.news.feeds import LatestEntriesFeed
from django.contrib import syndication

feeds = { "entries" : LatestEntriesFeed }

urlpatterns = patterns('vimba_cms.apps.news.views',
    # Example:
    (r'^(\d+)/$', 'NewsSingle'),
    (r'^page/(?P<page>[-\w]+)/$', 'Generic'),
    #(r'^preview/$', 'Preview'),
    (r'^preview/(?P<category>[-\w]+)/$', 'Preview'),
    (r'^(?P<page>[-\w]+)/$', 'Generic'),
    (r'^(?P<year>\d{4})/$', 'Generic'),
    (r'^feeds/?P<url>.*/$', 'syndication.views.feed', { 'feed_dict': feeds }),
    #(r'^$', 'Generic'),
)
