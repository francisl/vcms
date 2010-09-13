# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie

import sys

from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings

from site_media.models import *

class ImageCategoryTranslationInline(admin.StackedInline):
    model = ImageCategoryTranslation
    extra = 1

class ImageCategoryAdmin(admin.ModelAdmin):
    inlines = [ImageCategoryTranslationInline]
admin.site.register(ImageCategory, ImageCategoryAdmin)


class ImageDescriptionInline(admin.StackedInline):
    model = ImageDescription
    extra = 1

class ImageAdmin(admin.ModelAdmin):
    inlines = [ImageDescriptionInline]
admin.site.register(Image, ImageAdmin)

