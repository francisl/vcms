# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francis Lavoie on 30-05-2010.

from django.db import models
from django.utils.translation import ugettext_lazy as _

from treebeard.ns_tree import NS_Node
from vcms.apps.www.models.page import BasicPage
from vcms.apps.www.managers.menu import PageMenuManager

class PageMenu(NS_Node):
    page = models.OneToOneField(BasicPage)
    display = models.BooleanField(default=True)
    default = models.BooleanField(default=False)
    
    objects = PageMenuManager()
    
    class Meta:
        app_label = 'www'

    def __unicode__(self):
        to_print = """
            id         : %s
            page       : %s
            lft        : %s
            rgt        : %s
            tree_id    : %s
            depth      : %s
            display    : %s
            default    : %s
        """ % (self.id, self.page, self.lft, self.rgt, self.tree_id, self.depth, self.display, self.default)
        
        return to_print
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
    display = models.BooleanField(default=True)
    default = models.BooleanField(default=False)
    
    objects = PageMenuManager()
    
    class Meta:
        app_label = 'www'
        
        