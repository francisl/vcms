# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie

from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('vimba_cms.apps.news.views',
    # Example:
    (r'^(\d+)/$', 'NewsSingle'),
    (r'^page/(?P<page>[-\w]+)/$', 'Generic'),
    #(r'^preview/$', 'Preview'),
    (r'^preview/(?P<category>[-\w]+)/$', 'Preview'),
    (r'^(?P<page>[-\w]+)/$', 'Generic'),
    (r'^(?P<year>\d{4})/$', 'Generic'),
    #(r'^$', 'Generic'),
)
