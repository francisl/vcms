# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleBlogs
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 24-03-2010.

from django.contrib import admin
#from custom_fields.models import CustomField, CustomField2
from vcms.simpleblogs.models import BlogPage, BlogPost, BlogPostCategory, BlogPostWidget, CustomField


class CustomfieldAdmin(admin.StackedInline):
    model = CustomField
    extra = 1
    
class BlogPageAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'status', 'language', 'id')
admin.site.register(BlogPage, BlogPageAdmin)

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_on_page', 'status', 'language')
    inlines = [CustomfieldAdmin]
admin.site.register(BlogPost, BlogPostAdmin)

class BlogPostCategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(BlogPostCategory, BlogPostCategoryAdmin)

class BlogPostWidgetAdmin(admin.ModelAdmin):
    list_display = ('name', 'page', 'display_template', 'id')
admin.site.register(BlogPostWidget, BlogPostWidgetAdmin)

