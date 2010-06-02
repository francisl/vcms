# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie
from django.conf.urls.defaults import *
from django.conf import settings
import haystack

urlpatterns = patterns('vcms.apps.www.views',
    # Example:
    # (r'^search/$', 'Search'),
    (r'^search/', include('haystack.urls')),
    (r'^page/(?P<page>[-\w]+)/$', 'Generic'),
    (r'^$', 'Generic'),
)
