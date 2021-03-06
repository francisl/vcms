# -*- coding: utf-8 -*-
# Application: Vimba - CMS
# Module: www
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 30-05-2010.
import datetime, inspect, sys

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.db.models import signals
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

from site_language.models import Language

from vcms.www.models.menu import CMSMenu
from vcms.www.managers.page import BasicPageManager
from vcms.www.managers.containers import DashboardElementManager
from vcms.www.fields import StatusField

APP_SLUGS = 'www'

def _delete_page(page2delete):
    """ Move submenu up one level """
    pages = Page.objects.filter(parent=page2delete.id)
    if pages:
        for page in pages:
            if page.level != 0: # root = 0, no less
                # put menu one level up
                page.level = page.level - 1
                page.parent = page2delete.parent
            page.save()
            # check if menu has children, a level up them too
            _delete_page(page)

        
class BasicPage(models.Model):
    """ A page is a placeholder accessible by the user that represents a section content
        Like a news page, a forum page with multiple sub-section, a contact page ...
        A page can have multiple sub-section define in the application urls

        -- Link
        The CMS generate links to make these placeholder accessible in menus
        it uses the follow pattern : /{APP_SLUGS}/page/{page_slug}/
        ex: A basic Page model will be accessible at : /www/page/examplepage
            A news page model will be accessible at : /news/page/newspage

        -- Language
        Page can be classified by language - NOTE not yet working
        # TODO : add multi-language fonctionnality
    """
    _content_type = None
    name = models.CharField(max_length=100, unique=False, help_text=_('Max 100 characters.'))
    status = models.PositiveIntegerField(choices=StatusField.STATUSES, default=StatusField.DRAFT)
    slug = models.SlugField(max_length=150, unique=True, help_text=_("Used for hyperlinks, no spaces or special characters."))
    app_slug = models.SlugField(default="", editable=False, null=True, blank=True)
    module = models.CharField(max_length=30, default='', editable=False)
    description = models.CharField(max_length=250, help_text=_("Short description of the page (helps with search engine optimization.)"))
    keywords = models.CharField(max_length=250, null=True, blank=True, help_text=_("Page keywords (Help for search engine optimization.)"))
    
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_modified = models.DateTimeField(auto_now=True, editable=False)
    date_published = models.DateTimeField(default=datetime.datetime.min, editable=False)
    language = models.ForeignKey(Language)
    
    menu = generic.GenericRelation(CMSMenu)
    
    objects = BasicPageManager()

    display_title = models.BooleanField(default=True)

    containers = (('content', _('Content'))
                    ,('content_absolute', _('Content Absolute'))
                    ,('side_navigation', _('Side Navigation'))
                    ,('page_absolute', _('Page Absolute'))
                    ,('content_col1', _('Content Column 1 - MainPage only'))
                    ,('content_col2', _('Content Column 2 - MainPage only'))
                    )
    containers_type = { 'content': 'relative'
                        ,'content_absolute': 'absolute'
                        ,'side_navigation': 'relative'
                        ,'page_absolute': 'absolute'
                        ,'content_col1': 'relative'
                        ,'content_col2': 'relative' 
    }

    class Meta:
        verbose_name = _("Page - Basic page (do not edit)")
        verbose_name_plural = _("Page - Basic pages (do not edit)")
        app_label = 'www'

    def __unicode__(self):
        return self.name

    def get_type(self):
        """
            Returns the class of the current page.
            Used as a workaround to Django's ORM inheritance vs OOP's inheritance.
        """
        # Get all the classes in the current module
        for name, obj in inspect.getmembers(sys.modules[__name__]):
            # Discard everything but classes and classes that inherit from BasicPage
            if inspect.isclass(obj) and BasicPage in obj.__bases__:
                # If there are instances for the current page, the instance is of
                # the current page's type
                if obj.objects.filter(pk=self.pk).exists():
                    return obj
        return BasicPage

    def get_name(self):
        return self.__unicode__()

    def get_absolute_url(self):
        page = self.get_type().objects.get(id=self.id)
        menus = page.menu.all()
        if menus:
            return menus[0].get_absolute_url()
        return None

    url = property(get_absolute_url)
    
    def _add_to_main_menu(self, root):
        root.add_child(menu_name=self.name, content_object=self)

    def get_containers():
        raise NotImplementedError()

    @staticmethod
    def get_page_containers():
        raise NotImplementedError()
    
    #@staticmethod
    #def get_menu(self):
    #    try:
    ###        return self.menu.all()[0]
    #    except:
    #        return []
        
    def save(self, *args, **kwargs):
        if not self.app_slug:
            self.app_slug='www'
        super(BasicPage, self).save()

        from django.contrib.contenttypes.models import ContentType
        this_content_type = ContentType.objects.get_for_model(self.__class__)        
        if not CMSMenu.objects.has_menu_for_page(self):
            menu = CMSMenu(display=False, language=self.language
                           ,slug=self.slug
                           ,content_type=this_content_type, object_id=self.id)
            menu.save()

        super(BasicPage, self).save(*args, **kwargs)

class MainPage(BasicPage):
    class Meta:
        app_label = 'www'
        verbose_name = "Page - Main page"
        verbose_name_plural = "Page - Main pages"

    def save(self):
        self.module = 'main_page'
        super(MainPage, self).save()

    def get_menu(self):
        try:
            return self.menu.all()[0]
        except:
            return []
        
    def get_absolute_url(self):
        return self.basicpage_ptr.get_absolute_url()
    
    def get_controller(self):
        from vcms.www.views.html import MainPage
        return MainPage

class SimplePage(BasicPage):
    class Meta:
        verbose_name = "Page - Simple page"
        verbose_name_plural = "Page - Simple pages"
        app_label = 'www'

    def save(self):
        self.module = 'simple_page'
        super(SimplePage, self).save()

    def get_menu(self):
        try:
            return self.menu.all()[0]
        except:
            return []
        
    def get_controller(self):
        from vcms.www.views.html import simple_page
        return simple_page

    def get_absolute_url(self):
        return self.basicpage_ptr.get_absolute_url()
     
# -----
# Menu

class MenuSeparator(BasicPage):
    external_link = models.URLField(max_length=200, null=True, blank=True)
    def save(self):
        self.slug = self.get_absolute_url()
        self.status = StatusField.PUBLISHED
        self.language = Language.objects.get_default()
        self.module = "Separator"
        super(MenuSeparator, self).save()

    class Meta:
        app_label = "www"
        verbose_name = 'Menu - Separator'
        verbose_name_plural = 'Menu - Separator'

    def get_absolute_url(self):
        return "/" + self.external_link
