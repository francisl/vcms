# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Francis Lavoie

from django.conf.urls.defaults import *

urlpatterns = patterns('updates_registration.views'
    ,(r'^updates/$', 'updates_registration')
    ,(r'^updates/success/$', 'register_success')
)
