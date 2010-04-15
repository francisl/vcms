# encoding: utf-8
from django.conf.urls.defaults import *
from django.conf import settings
import sys
#subdir_path = ""

urlpatterns = patterns('vimba_cms_simthetiq.apps.products.views',
    # TODO - add pagination for product
    #(r'productlist/$', 'productList'),
    (r'page/(?P<page>[-\w]+)/category/(?P<selected_category>(\d+))$', 'Generic'),
    (r'page/(?P<page>[-\w]+)/$', 'Generic'),
    (r'home/$', 'productHome'),

        
    # product
    (r'set_DIS_navigation/$', 'set_navigation_type', {'type':'DIS'}),
    (r'set_compact_navigation/$', 'set_navigation_type', {'type':'compact'}),
    
    # navigation with dis
    #(r'dis/category/(?P<category>[-\w]+)/$', 'set_navigation_type', {'type':'DIS'}),
    
    # navigation in standard
    #(r'standard/category/(?P<category>[-\w]+)/$', 'set_navigation_type', {'type':'DIS'}),
    
    #(r'^(?P<page>(\d+))/(?P<product>[-\w]+)/$', 'ProductByPage'),
    #(r'^preview/(?P<page>[-\w]+)/$', 'Preview'),
    #(r'^$', 'Generic'),
)
