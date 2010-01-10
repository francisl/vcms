# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie

from django.conf.urls.defaults import *
from django.conf import settings
from vcms.apps.news.feeds import LatestNewsFeed, CategoryFeed


feeds = { "news" : LatestNewsFeed,
          "categories" : CategoryFeed }

urlpatterns = patterns('vcms.apps.news.views',
    # Example:
    (r'^(\d+)/$', 'NewsSingle'),
    (r'^page/(?P<page>[-\w]+)/$', 'Generic'),
    (r'^(?P<year>\d{4})/$', 'Generic'),
    #(r'^preview/$', 'Preview'),
    (r'^preview/(?P<category>[-\w]+)/$', 'Preview'),
    (r'^(?P<page>[-\w]+)/$', 'Generic'),
    (r'^(?P<year>\d{4})/$', 'Generic'),
    (r'^all/$', 'Generic'),
    #(r'^$', 'Generic'),
)

urlpatterns += patterns('',
                       (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', { 'feed_dict': feeds }),
                       )
