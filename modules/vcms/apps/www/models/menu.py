# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francis Lavoie on 30-05-2010.

from django.db import models
from django.utils.translation import ugettext_lazy as _

from treebeard.ns_tree import NS_Node

from vcms.apps.www.models.page import BasicPage
    
class PageMenu(NS_Node):
    page = models.OneToOneField(BasicPage)
    display = models.BooleanField(default=True)
   
    def __unicode__(self):
        return 'Category: %s' % self.name    
