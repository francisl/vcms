# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie

from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings

from vcms.apps.www.models import *

import sys

class LanguageAdmin(admin.ModelAdmin):
    pass

class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name','module','status','language',)

class ContentInline(admin.StackedInline):
    model = Content
    extra = 1

class SimplePageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ContentInline]

class DashboardElementInline(admin.StackedInline):
    model = DashboardElement
    extra = 1

class DashboardPreviewInline(admin.TabularInline):
    model = DashboardPreview
    extra = 2

DASHBOARD_MODULES = [DashboardElementInline,DashboardPreviewInline]
# now scan to cms apps module to see if something what what to register to dahsboard
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
        print("modules exception : %s" % module)



class DashboardPageAdmin(admin.ModelAdmin):
    inlines = DASHBOARD_MODULES

# -- CONTENTS
# -----------
class BannerAdmin(admin.ModelAdmin):
    filter_horizontal = ('page',)


#admin.site.register(Language, LanguageAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(SimplePage, SimplePageAdmin)

# CONTENTS
#admin.site.register(Content, ContentAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(DashboardPage, DashboardPageAdmin)