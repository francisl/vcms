# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie
from django.conf.urls.defaults import *

urlpatterns = patterns('vcms.image_gallery.views'
    # Example:
    ,(r'^(?P<page>[-\w]+)/(?P<category>[-\w]+)/(?P<page_number>(\d+))/$', 'gallery')
    ,(r'^(?P<page>[-\w]+)/(?P<page_number>\d+)/$', 'gallery')
    ,(r'^(?P<page>[-\w]+)/(?P<category>[-\w]+)/$', 'gallery')
    ,(r'^(?P<page>[-\w]+)/$', 'gallery')
    ,(r'^$', 'gallery')
)
