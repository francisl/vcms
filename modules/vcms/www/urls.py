# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie
from django.conf.urls.defaults import *
from django.conf import settings
import haystack

urlpatterns = patterns('vcms.www.views'
    # Example:
    # (r'^search/$', 'Search'),
    ,(r'^search/', include('haystack.urls'))
    ,(r'^page/(?P<page>[-\w]+)/$', 'Generic')
    ,(r'^menu/move/(?P<menuid>[-\w]+)/$', 'testCMSMenuForm')
        
    # AJAX
    ,(r'^ajax/page/list/$', 'get_page_list')
    ,(r'^ajax/page/add/$', 'add_new_page')
    ,(r'^ajax/page/update/$', 'update_page')
    ,(r'^$', 'Generic')
    ,
)
