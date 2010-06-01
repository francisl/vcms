# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francis Lavoie

from django.db import models

from treebeard.models import Node

class PageMenuManager(models.Manager):
    def set_root(self, menu):
        self.add_root(self, menu)
    
    def get_root(self):
        return self.get_root()
