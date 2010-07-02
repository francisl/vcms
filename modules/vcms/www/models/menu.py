# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francis Lavoie on 30-05-2010.

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from treebeard.ns_tree import NS_Node
from treebeard.mp_tree import MP_Node
from vcms.www.managers.menu import MainMenuManager

class MainMenu(MP_Node):
    menu_name = models.CharField(max_length=10, help_text="Maximum 50 characters", blank=True, null=True)
    display = models.BooleanField(default=True, help_text="Display in menu")
    default = models.BooleanField(default=False)
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    objects = MainMenuManager()
    
    class Meta:
        app_label = 'www'

    def __unicode__(self):
        if self.menu_name == None or self.menu_name == '':
            self.menu_name = self.content_object.get_name()
        return self.menu_name
    
        