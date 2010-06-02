# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie

import sys

from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings

from vcms.apps.www.models import *
from vcms.apps.www.models.page import *
#from vcms.apps.www.models.menu import PageMenu

class LanguageAdmin(admin.ModelAdmin):
    pass

class MainMenuAdmin(admin.ModelAdmin):
    pass
admin.site.register(MainMenu, MainMenuAdmin)

class MenuSeparatorAdmin(admin.ModelAdmin):
    fieldsets = (( 'Separator',
                   { 'fields': ('name','external_link') }
                   ),
                 )
admin.site.register(MenuSeparator, MenuSeparatorAdmin)

class MenuLocalLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    fieldsets = (( 'Separator',
                   { 'fields': ('name','local_link') }
                   ),
                 )
admin.site.register(MenuLocalLink, MenuLocalLinkAdmin)

class QuickLinksAdmin(admin.ModelAdmin):
    list_display = ('name', 'local_link', 'position')
    
admin.site.register(QuickLinks, QuickLinksAdmin)


class BasicPageAdmin(admin.ModelAdmin):
    pass
    #prepopulated_fields = {"slug": ("name",)}
    #list_display = ('name','module','status','language',)
admin.site.register(BasicPage, BasicPageAdmin)

class MainPageAdmin(admin.ModelAdmin):
    pass
    #prepopulated_fields = {"slug": ("name",)}
    #list_display = ('name','module','status','language',)
admin.site.register(MainPage, MainPageAdmin)

class ContentInline(admin.StackedInline):
    model = Content
    extra = 1
    
class SimplePageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ContentInline]
admin.site.register(SimplePage, SimplePageAdmin)

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
