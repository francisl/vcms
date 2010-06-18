# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Francis Lavoie

from django.conf.urls.defaults import *

urlpatterns = patterns('register2updates.views'
    ,(r'^updates/$', 'register_2_updates')
)
