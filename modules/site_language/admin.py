# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie

from django.contrib import admin
from site_language.models import Language

class LanguageAdmin(admin.ModelAdmin):
    pass
admin.site.register(Language, LanguageAdmin)
