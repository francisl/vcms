# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francis Lavoie

from django.db import models

from treebeard.models import Node
#from vcms.apps.www.models.menu import PageMenu


class PageMenuManager(models.Manager):
    #def set_menu_root(self, page):
    #    PageMenu.add_root(page=page)
    
    #def get_menu_root(self):
    #    return PageMenu.get_root()

    def set_as_generic_node(self, node):
        #root = node.get_root()
        #print("root = %s" % root)
        #root.add_child(node)
        pass
        