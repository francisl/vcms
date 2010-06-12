# encoding: utf-8
# copyright Vimba inc. 2010
# programmer : Francis Lavoie

from django.contrib import admin
from vcms.www.admin import ContentInline
from vcontact.models import ContactPage

class ContactPageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ContentInline]
    
admin.site.register(ContactPage, ContactPageAdmin)
