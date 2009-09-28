# encoding: utf-8
from django.conf.urls.defaults import *
from django.conf import settings
import sys
#subdir_path = ""

urlpatterns = patterns('vimba_cms_simthetiq.apps.products.views',
    # TODO - add pagination for product
    (r'page/(?P<page>[-\w]+)/category/(?P<selected_category>(\d+))$', 'Generic'),
    (r'page/(?P<page>[-\w]+)/$', 'Generic'),

    #(r'^(?P<page>(\d+))/(?P<product>[-\w]+)/$', 'ProductByPage'),
    #(r'^preview/(?P<page>[-\w]+)/$', 'Preview'),
    #(r'^$', 'Generic'),
    
    # Uncomment this for admin:
    #    (r'^admin/', include('django.contrib.admin.urls')),
)
