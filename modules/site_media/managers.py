# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: www
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francis

from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class ImageCategoryManager(models.Manager):
    def get_image_category_from_slug(self, category):
        try:
            return self.get(slug=category)
        except ObjectDoesNotExist:
            return None
            
