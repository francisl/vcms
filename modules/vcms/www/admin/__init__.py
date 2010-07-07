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

class LanguageAdmin(admin.ModelAdmin):
    pass
admin.site.register(Language, LanguageAdmin)

class MainMenuAdmin(treeadmin.TreeAdmin):
    pass
admin.site.register(MainMenu, MainMenuAdmin)

class CMSMenuAdmin(admin.ModelAdmin):
    list_display = ('get_tab_name', 'get_slug', 'language','id', 'parent', 'lft', 'rght', 'tree_id')
    #filter_horizontal = ('language',)
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
admin.site.register(BasicPage, BasicPageAdmin)

class MainPageAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    
admin.site.register(MainPage, MainPageAdmin)

class SimplePageAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'id')
admin.site.register(SimplePage, SimplePageAdmin)


class ContentInline(admin.StackedInline):
    model = Content
    extra = 1
    
#class SimplePageAdmin(admin.ModelAdmin):
#    prepopulated_fields = {"slug": ("name",)}
#    inlines = [ContentInline]
#admin.site.register(SimplePage, SimplePageAdmin)


## ################
## CONTAINERS
#class BasicContainerAdmin(admin.ModelAdmin):
#    pass
#admin.site.register(BasicContainer, BasicContainerAdmin)

class GridContainerAdmin(admin.ModelAdmin):
    pass
admin.site.register(GridContainer, GridContainerAdmin)

class TableContainerAdmin(admin.ModelAdmin):
    pass
admin.site.register(TableContainer, TableContainerAdmin)

class RelativeContainerAdmin(admin.ModelAdmin):
    list_display = ['page', 'name']
    #filter_horizontal = ('page',)
admin.site.register(RelativeContainer, RelativeContainerAdmin)


## ################
## WIDGETS
class WidgetWrapperAdmin(admin.ModelAdmin):
    pass
admin.site.register(WidgetWrapper, WidgetWrapperAdmin)

class GridWidgetWrapperAdmin(admin.ModelAdmin):
    pass
admin.site.register(GridWidgetWrapper, GridWidgetWrapperAdmin)

class TableWidgetWrapperAdmin(admin.ModelAdmin):
    pass
admin.site.register(TableWidgetWrapper, TableWidgetWrapperAdmin)

class RelativeWidgetWrapperAdmin(admin.ModelAdmin):
    pass
admin.site.register(RelativeWidgetWrapper, RelativeWidgetWrapperAdmin)

class WidgetAdmin(admin.ModelAdmin):
    pass
admin.site.register(Widget, WidgetAdmin)

class TextWidgetAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
admin.site.register(TextWidget, TextWidgetAdmin)

class PageLinksWidgetLinkInline(admin.StackedInline):
    model = PageLinksWidgetLink
    extra = 1

class PageLinksWidgetAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    inlines = [PageLinksWidgetLinkInline]
admin.site.register(PageLinksWidget, PageLinksWidgetAdmin)


"""
NEED TO BE REDONE
class DashboardElementInline(admin.StackedInline):
    model = DashboardElement
    extra = 1

class DashboardPreviewInline(admin.TabularInline):
    model = DashboardPreview
    extra = 2

DASHBOARD_MODULES = [DashboardElementInline,DashboardPreviewInline]
# now scan to cms apps module to see if something wants to register to dahsboard
for module in settings.PAGE_MODULES:
    try:
        # loading requirements first
        __import__(module['models'], globals(), locals(), [module["model"]])
        # loading module into dashboard list
        mod = __import__(module["admin"], globals(), locals(), [module["model"]])
        inline_mod = getattr(mod,module["inline"]) 
        DASHBOARD_MODULES.append(inline_mod)

    except:
        pass
        #print("modules exception : %s" % module)

class DashboardPageAdmin(admin.ModelAdmin):
    inlines = DASHBOARD_MODULES
admin.site.register(DashboardPage, DashboardPageAdmin)
"""

# -- BANNER
# -----------
class BannerImageAdmin(admin.ModelAdmin):
    filter_horizontal = ('banner',)
admin.site.register(BannerImage, BannerImageAdmin)
    
class BannerAdmin(admin.ModelAdmin):
    filter_horizontal = ('page',)
admin.site.register(Banner, BannerAdmin)
