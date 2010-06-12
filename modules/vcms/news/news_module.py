# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie

from django.contrib import admin
from vcms.news.models import NewsPageModule

class NewsPageModuleInline(admin.StackedInline):
    model = NewsPageModule
    extra = 2

#modules = {"NewsPage" : NewsPageModuleInline }