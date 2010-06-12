# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francis Lavoie

from django.db import models

from treebeard.models import Node
#from vcms.www.models.menu import MainMenu


class MainMenuManager(models.Manager):
    #def set_menu_root(self, page):
    #    PageMenu.add_root(page=page)
    
    #def get_menu_root(self):
    #    return PageMenu.get_root()

    def set_as_generic_node(self, node):
        #root = node.get_root()
        #print("root = %s" % root)
        #root.add_child(node)
        pass
        
    def get_root_menu(self):
        return self.get_first_root_node()
    
    def get_default_page(self):
        default_menu = self.filter(default=True)[0]
        return default_menu.content_object

     
    def get_submenu(self):
        from hwm.tree import helper
        """ return navigation tree as a list containing tree node dictionary """
        root = self.get_root_menu() 
        nav = []
        for navgroup in self.all():
            nav.append(helper.create_tree_node(navgroup.name, url=navgroup.get_absolute_url()))
        return nav
    