# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleBlogs
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 24-03-2010.

from django.contrib import admin
from vcms.apps.simpleblogs.models import Blog, BlogPageModule


class BlogPageModuleAdmin(admin.ModelAdmin):
    pass
admin.site.register(BlogPageModule, BlogPageModuleAdmin)

class BlogAdmin(admin.ModelAdmin):
    pass
admin.site.register(Blog, BlogAdmin)
