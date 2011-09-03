# -*- coding: utf-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 20-03-2010.

from django.conf.urls.defaults import *

from vcms.simpleblogs.feeds import LatestBlogFeed

feeds = { "page" : LatestBlogFeed }

urlpatterns_prefix = ['blogs','news']
urlpatterns = patterns(
    '',
    (r'rss/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', { 'feed_dict': feeds }),
    )

urlpatterns += patterns(''
    ,(r'announcements/comments/', include('django.contrib.comments.urls'))
)

urlpatterns += patterns('vcms.simpleblogs.views'
    ,(r'(?P<page_slug>[-\w]+)-(?P<page_number>\d+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{2})/$', 'page_for_date')
    ,(r'(?P<page_slug>[-\w]+)-(?P<page_number>\d+)/(?P<year>\d{4})/(?P<month>\d{1,2})/$', 'page_for_date')
    ,(r'(?P<page_slug>[-\w]+)-(?P<page_number>\d+)/(?P<year>\d{4})/$', 'page_for_date')
    
    ,(r'(?P<page_slug>[-\w]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{2})/(?P<post_id>\d+)$', 'post')
    ,(r'(?P<page_slug>[-\w]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{2})/$', 'page_for_date')
    ,(r'(?P<page_slug>[-\w]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/$', 'page_for_date')
    ,(r'(?P<page_slug>[-\w]+)/(?P<year>\d{4})/$', 'page_for_date')
    
    ,(r'(?P<page_slug>[-\w]+)-(?P<page_number>\d+)/archives/-(?P<year>\d{4})/$', 'archives')
    ,(r'(?P<page_slug>[-\w]+)/archives/-(?P<year>\d{4})/$', 'archives')
    
    ,(r'(?P<page_slug>[-\w]+)-(?P<page_number>\d+)/(?P<category>[-\w]+)/$', 'page')
    ,(r'(?P<page_slug>[-\w]+)/(?P<category>[-\w]+)/$', 'page')
    ,(r'(?P<page_slug>[-\w]+)-(?P<page_number>\d+)/$', 'page')
    ,(r'(?P<page_slug>[-\w]+)/$', 'page')
    ,(r'^$', 'page')
)
