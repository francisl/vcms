# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie
from django.conf.urls.defaults import *
from django.conf import settings
import haystack

from vcms.www.views.html import Generic

urlpatterns = patterns('vcms.www.views.html'
    ,(r'^$', Generic)
    ,(r'^search/', include('haystack.urls'))
    ,(r'^page/(?P<page>[-\w]+)/$', 'Generic')
    ,(r'^menu/move/(?P<menuid>[-\w]+)/$', 'testCMSMenuForm')
)

urlpatterns += patterns('vcms.www.views.ajax'
    # AJAX
    ,(r'^ajax/page/list/$', 'get_page_list')
)
