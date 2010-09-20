# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: www
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francis

from django.db import models

from site_media.models import Image

class ImageGalleryPageManager(models.Manager):
    def get_default_page(self):
        try:
            return self.all()[0]
        except:
            return None

    def get_seletcted_page_or_default_page(self, page):
        try:
            return self.get(slug=page)
        except:
            return self.get_default_page()

    def get_all_images_for_page(gallery_page):
        categories = self.display_category.all()
        images = Image.models.filter(category__in=categories)
