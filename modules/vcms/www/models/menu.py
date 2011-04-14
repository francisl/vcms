# -*- coding: utf-8 -*-
# Application: Vimba - CMS
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francis Lavoie on 30-05-2010.

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

#from treebeard.ns_tree import NS_Node
from treebeard.mp_tree import MP_Node
from vcms.www.managers.menu import CMSMenuManager, MainMenuManager
from vcms.www.managers import QuickLinksManager
from site_language.models import Language
from vcms.www.fields import StatusField


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
   
        
import mptt
class CMSMenu(models.Model):
    DROPDOWN_MENU = 0
    SIMPLE_MENU = 1
    MENU_STYLE = ((DROPDOWN_MENU, _('Dropdown')),
              (SIMPLE_MENU, _('Single line')))
    menu_name = models.CharField(max_length=120, help_text="Name that appear in the menu. Maximum 80 characters", blank=True, null=True)
    slug = models.SlugField(max_length=150, help_text=_("Used for hyperlinks, no spaces or special characters."), blank=True, null=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    display = models.BooleanField(default=True, help_text="Display in menu - Only work for page that are set as published")
    default = models.BooleanField(default=False)
    language = models.ForeignKey(Language)
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    objects = CMSMenuManager()
    
    class Meta:
        app_label = 'www'
        verbose_name = 'Menu - Master'
        verbose_name_plural = 'Menu - Master'
        unique_together = ('parent', 'slug')
        ordering = ['tree_id', 'lft']
        
    def __unicode__(self):
        if self.menu_name == None or self.menu_name == '':
            try:
                self.menu_name = self.content_object.get_name()
            except:
                self.menu_name = "Database relation error"
        return self.menu_name

    def get_name(self):
        if self.__unicode__():
            return self.__unicode__()
        return self.content_object.get_name()
        
    def get_slug(self):
        return self.get_absolute_url()
        
    def get_tab_name(self):
        prefix = "+-- " * self.level
        return prefix + self.__unicode__()
    
    def get_absolute_url(self):
        if self.parent:
            return '/%s/%s/' % (self.parent.slug, self.slug)
        return '/%s/' % self.slug
    
    def get_page_status(self):
        return self.content_object.status
    
    def get_root_menu(self):
        return self.parent

    def get_children(self):
        return CMSMenu.objects.get_children(self)

    name = property(get_name)
    status = property(get_page_status)

    def get_controller(self):
        if hasattr(self.content_object, 'get_controller'):
            return self.content_object.get_controller()
        return None
    
mptt.register(CMSMenu, order_insertion_by=['object_id'])


class MenuLocalLink(models.Model):
    """ MenuLocalLink is to link static page dynamicaly into the menu """
    name = models.CharField(max_length=100, unique=False, help_text=_('Max 100 characters.'))
    local_link = models.CharField(max_length=200, null=True, blank=True,
                                  help_text="Link on this web site. ex. /www/page/")
    
    class Meta:
        app_label = "www"
        verbose_name = 'Menu - Local Link'
        verbose_name_plural = 'Menu - Local Link'
    
    def __unicode__(self):
        return self.name
    
    def get_name(self):
        return self.__unicode__()
        
    def get_absolute_url(self):
        return self.local_link
        
    def save(self):
        #self.status = StatusField.PUBLISHED
        #self.language = Language.objects.get_default()
        #self.module = "LocalLink"
        try:
            if self.local_link[-1:] == '/' and len(self.local_link) > 1:
                self.local_link = self.local_link[:-1]
        except:
             self.local_link = ''
        #self.slug = self.get_absolute_url()
        super(MenuLocalLink, self).save()


class QuickLinks(models.Model):
    """ Like bookmark, enable to put side links to local webpage
    """
    name = models.CharField(max_length="40", help_text="Max 40 characters")
    image = models.ImageField(upload_to='uploadto/quicklinks', width_field='width', height_field='height')
    width = models.PositiveIntegerField(blank=True)
    height = models.PositiveIntegerField(blank=True)
    local_link = models.CharField(max_length=200, help_text="Link on this web site. ex. /www/page/")
    position = models.IntegerField()

    objects = QuickLinksManager()

    def __unicode__(self):
        return self.name

    def save(self):
        try:
            if self.local_link[-1:] == '/' and len(self.local_link) > 1:
                self.local_link = self.local_link[:-1]
        except:
             self.local_link = ''
        super(QuickLinks, self).save()

    def get_absolute_url(self):
        if self.local_link[0] != "/":
            return self.local_link
        else:
            return self.local_link

    class Meta:
        verbose_name_plural = "Quicklinks"
        ordering = [ 'position' ]
        app_label = "www"
