# encoding: utf-8
from django.conf.urls.defaults import *
from django.conf import settings
import sys
#subdir_path = ""

urlpatterns = patterns('vimba_cms_simthetiq.apps.products.views',
    # TODO - add pagination for product
    #(r'productlist/$', 'productList'),
    (r'home/$', 'product_list'),
    
    (r'(?P<nav_type>[-\w]+)/(?P<nav_selection>[-\w]+)/list/(?P<paginator_page_number>(\d+))$', 'product_list'),
    (r'(?P<nav_type>[-\w]+)/(?P<nav_selection>[-\w]+)/list/$', 'product_list', {}),
    (r'(?P<nav_type>[-\w]+)/(?P<nav_selection>[-\w]+)/detailed_list/(?P<paginator_page_number>(\d+))$', 'product_detailed_list', {}),
    (r'(?P<nav_type>[-\w]+)/(?P<nav_selection>[-\w]+)/detailed_list/$', 'product_detailed_list', {}),
    (r'(?P<nav_type>[-\w]+)/(?P<nav_selection>[-\w]+)/grid/(?P<paginator_page_number>(\d+))$', 'product_grid', {}),
    (r'(?P<nav_type>[-\w]+)/(?P<nav_selection>[-\w]+)/grid/$', 'product_grid', {}),
    (r'(?P<nav_type>[-\w]+)/', 'product_list'),
    

    #(r'(?P<nav_type>[-\w]+)/slist/(?P<paginator_page_number>(\d+))$', 'product_list', {}),
    #(r'(?P<nav_type>[-\w]+)/slist/$', 'ProductSList', {'slug': 'slist'}),
    #(r'(?P<nav_type>[-\w]+)/list/$', 'ProductList'),
    #(r'(?P<nav_type>[-\w]+)/list/(?P<paginator_page_number>(\d+))$', 'product_detailed_list'),
    #(r'(?P<nav_type>[-\w]+)/grid/$', 'ProductGrid'),
    #(r'(?P<nav_type>[-\w]+)/grid/(?P<paginator_page_number>(\d+))$', 'product_grid'),
    #(r'(?P<nav_type>[-\w]+)/$', 'product_list'),
    
   
    # product
    (r'set_DIS_navigation/$', 'set_navigation_type', {'type':'DIS'}),
    (r'set_compact_navigation/$', 'set_navigation_type', {'type':'compact'}),
    
    # navigation with dis
    #(r'dis/category/(?P<category>[-\w]+)/$', 'set_nav_type', {'type':'DIS'}),
    
    # navigation in standard
    #(r'standard/category/(?P<category>[-\w]+)/$', 'set_nav_type', {'type':'DIS'}),
    
    #(r'^(?P<page>(\d+))/(?P<product>[-\w]+)/$', 'ProductByPage'),
    #(r'^preview/(?P<page>[-\w]+)/$', 'Preview'),
    (r'$', 'product_list', { 'nav_type': 'standard', 'nav_selection': 'all' }),
)
