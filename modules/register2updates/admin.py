# encoding: utf-8
# copyright Vimba inc. 2010
# programmer : Francis Lavoie

from django.contrib import admin
from register2updates.models import Registered2Updates

class Registered2UpdatesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Registered2Updates, Registered2UpdatesAdmin)
