# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francis Lavoie on 30-05-2010.

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from treebeard.ns_tree import NS_Node
#from vcms.www.models.page import BasicPage
from vcms.www.managers.menu import MainMenuManager

class MainMenu(NS_Node):
    menu_name = models.CharField(max_length=50, help_text="Maximum 50 characters")
    display = models.BooleanField(default=True, help_text="Display in menu")
    default = models.BooleanField(default=False)
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    objects = MainMenuManager()
    
    class Meta:
        app_label = 'www'

    def __unicode__(self):
        to_print = """
            id         : %s
            menu_name  : %s
            lft        : %s
            rgt        : %s
            tree_id    : %s
            depth      : %s
            display    : %s
            default    : %s
        """ % (self.id, self.menu_name, self.lft, self.rgt, self.tree_id, self.depth, self.display, self.default)
        
        return self.menu_name
    
    """
    def save(self):
        
        if self.default == True:
            self.set_root(self)
            
        try:
            root_node = PageMenu.get_root(self)
            root_node.add_child(self)
        except:
            PageMenu.add_root()
            #root_node = PageMenu.get_root(self)
        
        print("root node = %s" % root_node)
        
        #PageMenu.objects.set_as_generic_node(self)
       
        
        super(PageMenu, self).save()
        """

class DummyPageMenu(NS_Node):
    name = models.CharField(max_length=100)
    
    class Meta:
        app_label = 'www'
        
        