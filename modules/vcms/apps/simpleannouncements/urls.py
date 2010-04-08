# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 05-04-2010.

from django.conf.urls.defaults import *


urlpatterns = patterns('',
    (r'^announcements/comments/', include('django.contrib.comments.urls')),
)
