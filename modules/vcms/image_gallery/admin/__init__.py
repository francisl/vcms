# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie

import sys

from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings

from vcms.www.admin import BasicPageAdmin
from vcms.image_gallery.models import *

class ImageGalleryPageAdmin(BasicPageAdmin):
    pass
admin.site.register(ImageGalleryPage, ImageGalleryPageAdmin)
