# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 20-03-2010.

from django.contrib import admin
from vcms.apps.simplenews.models import News, NewsCategory, NewsPageModule


class NewsCategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(NewsCategory, NewsCategoryAdmin)


class NewsAdmin(admin.ModelAdmin):
    def queryset(self, request):
        return News.objects.get_news_for_user(request.user)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        has_class_permission = super(NewsAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj and obj not in News.objects.get_news_for_user(request.user):
            return False
        return True
admin.site.register(News, NewsAdmin)


class NewsPageModuleAdmin(admin.ModelAdmin):
    pass
admin.site.register(NewsPageModule, NewsPageModuleAdmin)
