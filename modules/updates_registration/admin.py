# encoding: utf-8
# copyright Vimba inc. 2010
# programmer : Francis Lavoie

from django.contrib import admin
from updates_registration.models import UpdatesRegistration

class UpdatesRegistrationAdmin(admin.ModelAdmin):
    pass

admin.site.register(UpdatesRegistration, UpdatesRegistrationAdmin)
