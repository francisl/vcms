# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleBlogs
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 24-03-2010.

from django.contrib import admin
from vcms.simpleblogs.models import BlogPage, BlogPost, BlogPostCategory, BlogPostWidget


class BlogPageAdmin(admin.ModelAdmin):
    pass
admin.site.register(BlogPage, BlogPageAdmin)

class BlogPostAdmin(admin.ModelAdmin):
    pass
admin.site.register(BlogPost, BlogPostAdmin)

class BlogPostCategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(BlogPostCategory, BlogPostCategoryAdmin)

class BlogPostWidgetAdmin(admin.ModelAdmin):
    pass
admin.site.register(BlogPostWidget, BlogPostWidgetAdmin)
