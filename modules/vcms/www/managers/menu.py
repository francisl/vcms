# -*- coding: utf-8 -*-
# Application: Vimba - CMS
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francis Lavoie

from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from treebeard.models import Node

class MainMenuManager(models.Manager):
    def set_as_generic_node(self, node):
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
            pages = self.all()
            if pages:
                return pages[0].content_object
        else:
            return default_menu[0].content_object

    def has_menu_for_page(self, page):
        from django.contrib.contenttypes.models import ContentType
        this_content_type = ContentType.objects.get_for_model(type(page))
        menus = self.filter(content_type=this_content_type, object_id=page.id)
        return True if menus else False

    def get_menu_from_string(self, menu_slug):
        try:
            return self.get(slug=menu_slug)
        except ObjectDoesNotExist:
            return None

class QuickLinksManager(models.Manager):
    def get_quicklinks(self):
        return self.all()
