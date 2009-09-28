# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie


from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.admin.views.decorators import staff_member_required

from vimba_cms.apps.news.models import *

class NewsPageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class NewsCategoryAdmin(admin.ModelAdmin):
    pass

class NewsAdmin(admin.ModelAdmin):
    try:
        filter_horizontal = ["product_images", "product_videos"]
    except:
        pass
        # if no product, dont filter
    prepopulated_fields = {"excerpt": ("content",)}

class NewsPageModuleInline(admin.TabularInline):
    model = NewsPageModule
    extra = 2

admin.site.register(NewsPage, NewsPageAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(NewsCategory, NewsCategoryAdmin)

