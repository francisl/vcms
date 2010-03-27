# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 20-03-2010.

from django.contrib import admin
from vcms.apps.simplenews.models import News, NewsPageModule


class NewsPageModuleAdmin(admin.ModelAdmin):
    pass
admin.site.register(NewsPageModule, NewsPageModuleAdmin)

class NewsAdmin(admin.ModelAdmin):
    pass
admin.site.register(News, NewsAdmin)
