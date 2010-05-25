# encoding: utf-8
# copyright Vimba inc. 2010
# programmer : Francis Lavoie
from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('vcms.apps.contact.views',
    (r'^page/(?P<page>[-\w]+)/$', 'Contact'),
    (r'^$', 'Contact'),
)
