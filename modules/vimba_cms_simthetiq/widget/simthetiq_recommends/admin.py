# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie

import sys

from django.contrib import admin

from vimba_cms_simthetiq.widget.simthetiq_recommends.models import *

class PageLinkInline(admin.StackedInline):
    model = PageLink
    extra = 1

class PageLinksWidgetAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    inlines = [PageLinkInline]
admin.site.register(PageLinksWidget, PageLinksWidgetAdmin)
