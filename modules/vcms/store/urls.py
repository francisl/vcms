# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: Store
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 13-05-2010.

from django.conf.urls.defaults import *


urlpatterns_prefix = r''

urlpatterns = patterns('',
    (r'^getStatesProvinces/(?P<country_id>\d+)/$', 'vcms.store.views.get_states_provinces'), # ^/getStatesProvinces/39/
    url(r'^login/$', 'vcms.store.views.emaillogin'),
)
