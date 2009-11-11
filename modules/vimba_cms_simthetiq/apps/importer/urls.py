# encoding: utf-8
from django.conf.urls.defaults import *
from django.conf import settings
import sys
#subdir_path = ""

urlpatterns = patterns('vimba_cms_simthetiq.apps.importer.views',
    # TODO - add pagination for product
    (r'^$', 'dashboard'),
    (r'^log/(?P<logfile>[-\w]+)/$', 'log'),
    #(r'^importfile/(?P<importfile>[-\w]+)/$', 'importDataSource'),

)
