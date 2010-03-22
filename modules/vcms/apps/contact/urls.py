# encoding: utf-8
# copyright Vimba inc. 2010
# programmer : Francis Lavoie
from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('vcms.apps.contact.views',
    (r'^(?P<page>[-\w]+)/$', 'Contact'),    
)
