# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie

import sys

from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings

from treebeard import admin as treeadmin

from vcms.www.models import *
from vcms.www.models.page import *
from vcms.www.models.containers import *
from vcms.www.models.menu import *

#class MainMenuAdmin(treeadmin.TreeAdmin):
#    pass
#admin.site.register(MainMenu, MainMenuAdmin)

class CMSMenuAdmin(admin.ModelAdmin):
    list_display = ('get_tab_name', 'get_slug', 'language','id', 'parent', 'lft', 'rght', 'tree_id')
admin.site.register(CMSMenu, CMSMenuAdmin)

class MenuSeparatorAdmin(admin.ModelAdmin):
    fieldsets = (( 'Separator',
                   { 'fields': ('name','external_link') }
                   ),
                 )
admin.site.register(MenuSeparator, MenuSeparatorAdmin)

class MenuLocalLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'local_link', 'id')
    fieldsets = (( 'Separator',
                   { 'fields': ('name','local_link') }
                   ),
                 )
admin.site.register(MenuLocalLink, MenuLocalLinkAdmin)

class QuickLinksAdmin(admin.ModelAdmin):
    list_display = ('name', 'local_link', 'position')
    
admin.site.register(QuickLinks, QuickLinksAdmin)


class BasicPageAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    #prepopulated_fields = {"slug": ("name",)}
    #list_display = ('name','module','status','language',)
#admin.site.register(BasicPage, BasicPageAdmin)

class MainPageAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    
admin.site.register(MainPage, MainPageAdmin)

class SimplePageAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'url', 'id')
admin.site.register(SimplePage, SimplePageAdmin)


class ContentInline(admin.StackedInline):
    model = Content
    extra = 1

class ContainerWidgetsAdmin(admin.ModelAdmin):
    list_display = ('widget', 'page', 'container', 'widget_type', 'status')
    list_filter = ('page',)
admin.site.register(ContainerWidgets, ContainerWidgetsAdmin)

class TextWidgetAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
admin.site.register(TextWidget, TextWidgetAdmin)


# -- BANNER
# -----------

class BannerImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image_thumbnail', 'displayed_in_banner')
    #filter_horizontal = ('banner',)
admin.site.register(BannerImage, BannerImageAdmin)
    
class BannerAdmin(admin.ModelAdmin):
    filter_horizontal = ('page',)
admin.site.register(Banner, BannerAdmin)
