# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francis Lavoie

from django.db import models

from treebeard.models import Node

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
        
    def get_root_menu_if_exist(self):
        if len(self.ancestors) > 0 :
            return self.ancestors[0]
        return None

    def get_root_menu(self):
        return self.get_first_root_node()
    
    def get_default_page(self):
        default_menu = self.filter(default=True)[0]
        return default_menu.content_object

    def get_submenu(self):
        from hwm.tree import helper
        """ return navigation tree as a list containing tree node dictionary 
            ex:
                >>> from vcms.www.models import menu
                >>> mm = menu.MainMenu
                >>> mm.objects.get_children_for_object_id(3)
        """
        root = self.get_root_menu() 
        nav = []
        for navgroup in self.all():
            nav.append(helper.create_tree_node(navgroup.name, url=navgroup.get_absolute_url()))
        return nav
    
    def get_children_for_object_id(self, obj_id):
        node = self.filter(content_object=obj_id)[0]
        return node.get_children()

class CMSMenuManager(models.Manager):
    def get_roots(self, language):
        return self.filter(level=0).filter(language=language).filter(display=True)
        
    def get_displayable_children(self, parent):
        #parent.get_children()
        return parent.get_children().filter(display=True)
        
    def get_default_page(self):
        default_menu = self.filter(default=True)
        if default_menu.count() == 0 or default_menu == None:
            return self.all()[0].content_object
        else:
            return default_menu[0].content_object


class QuickLinksManager(models.Manager):
    def get_quicklinks(self):
        return self.all()
