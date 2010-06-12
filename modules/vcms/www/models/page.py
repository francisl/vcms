# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: www
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 30-05-2010.
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.db.models import signals

from treebeard.ns_tree import NS_Node

from vcms.www.fields import StatusField
from vcms.www.models.menu import MainMenu
from vcms.www.managers.page import BasicPageManager
from vcms.www.managers.page import LanguageManager

class Language(models.Model):
    language = models.CharField(max_length=50, help_text=_('Max 50 characters.'))
    language_code = models.CharField(max_length=2, primary_key=True, help_text=_('e.g. fr = French or en = english'))

    objects = LanguageManager()

    class Meta:
        app_label = "www"
        
    def __unicode__(self):
        return self.language
    
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
    name = models.CharField(max_length=100, unique=True, help_text=_('Max 100 characters.'))
    status = StatusField()
    slug = models.SlugField(max_length=150, unique=True, help_text=_("Used for hyperlinks, no spaces or special characters."))
    app_slug = models.SlugField(default="", editable=False, null=True, blank=True)
    module = models.CharField(max_length=30, default='', editable=False)
    description = models.CharField(max_length=250, help_text=_("Short description of the page (helps with search engine optimization.)"))
    keywords = models.CharField(max_length=250, null=True, blank=True, help_text=_("Page keywords (Help for search engine optimization.)"))
    
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_modified = models.DateTimeField(auto_now=True, editable=False)
    date_published = models.DateTimeField(default=datetime.datetime.min, editable=False)
    language = models.ForeignKey(Language)
    
    menu = generic.GenericRelation(MainMenu)
    
    objects = BasicPageManager()

    # Generic FK to the container, used as an inheritance workaround
    #widget_type = models.ForeignKey(ContentType)
    #widget_id = models.PositiveIntegerField()
    #widget = generic.GenericForeignKey('widget_type', 'widget_id')
    

    class Meta:
        verbose_name = _("Basic page")
        verbose_name_plural = _("Basic pages")
        app_label = 'www'

    def __unicode__(self):
        return self.name

    def get_name(self):
        return self.name

    def get_absolute_url(self):
        return "/www/page/" + self.slug

    def _add_to_main_menu(self, root):
        root.add_child(menu_name=self.name, content_object=self)

    @staticmethod
    def get_containers():
        raise NotImplementedError()
        
    def save(self):
        self.app_slug='www'
        from vcms.www.models.menu import MainMenu as PageMenu
        first_root = MainMenu.get_first_root_node()
        root = None
        
        if type(first_root) != type(None):
            if first_root.menu_name == str(self.language).lower():
                root = first_root
                del first_root
            else:
                for sibling in root.get_siblings():
                    if sibling.menu_name == str(self.language).lower():
                        root = sibling
                        break
        
        super(BasicPage, self).save()
        
        if root == None:
            # root menu not found
            root = MainMenu.add_root(menu_name=str(self.language))
            self._add_to_main_menu(root)
        else:
            # root already exist
            # check if already insert in menu
            exist = False
            for child in root.get_children():
                if child.menu_name == self.name:
                    exist = True
                    break
            if not exist:
                self._add_to_main_menu(root)
            
                            
        # __TODO: Commented out the following line as it doesn't work as of 31-01-2010
        #self.indexer.update()


class Page(BasicPage):
    EMPTY = 0
    TEMPLATES = ((EMPTY, 'Default'),)
    TEMPLATE_FILES = { EMPTY: 'master.html'}
    template = models.IntegerField(default=EMPTY, choices=TEMPLATES)

    # menus
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', editable=False)
    level = models.IntegerField(editable=False, default=0)
    tree_position = models.IntegerField(editable=False, default=0)
    display = models.BooleanField(editable=False, default=False)

    # Parameteers
    
    # lang = models.IntegerField(max_length=2,choices=settings.LANGUAGES,
    #                       default=settings.DEFAULT_LANGUAGE, db_index=True, editable=False)

    # Controler for the pages
    #objects = PageManager()

    class Meta:
        ordering = ['tree_position', 'name']
        verbose_name_plural = "Menu Administration"
        #unique_together = ("slug", "app_slug")
        app_label = "www"
        

    def get_absolute_url(self):
        if self.app_slug:
            return "/" + self.app_slug + "/page/" + self.slug
        elif self.slug == '/':
            return ''
        else:
            return "/" + self.slug

    def __unicode__(self):
        return self.name
    
    def save(self):
        if self.default:
            Page.objects.reset_Default()
        super(Page, self).save()

    def delete(self):
        if self.default:
            Page.objects.deleted_Default()
        _delete_page(self)
        super(Page, self).delete()
        # __TODO: Commented out the following line as it doesn't work as of 31-01-2010
        #self.indexer.update()


class MainPage(BasicPage):
    class Meta:
        app_label = 'www'

    def save(self):
        self.module = 'MainPage'
        super(BlankPage, self).save()
        
    @staticmethod
    def get_containers():
        from vcms.www.models.containers import ContainerDefinition
        from vcms.www.models.containers import GridContainer
        from vcms.www.models.containers import TableContainer
        from vcms.www.models.containers import RelativeContainer
        return { "navigation_container": ContainerDefinition(_("Navigation"), RelativeContainer)
                    ,"main_content": ContainerDefinition(_("Content"), GridContainer) }

def pre_MainPage(instance, **kargs):
    print("!!! entering PRE_SAVE for MainPage")
    print("instance = %s" % instance)
    print("**kargs = %s" % kargs)
    print("**kargs = %s" % kargs['signal'])

#signals.pre_save.connect(pre_MainPage, sender=MainPage)

class BlankPage(BasicPage):
    class Meta:
        verbose_name = "Page - Blank page"
        verbose_name_plural = "Page - Blank pages"
        app_label = 'www'

    def save(self):
        self.module = 'BlankPage'
        super(BlankPage, self).save()
        
    def get_containers(self):
        from vcms.www.models.containers import RelativeContainer
        my_rel_cont = {} 
        for container in RelativeContainer.objects.filter(page=self): 
            my_rel_cont[container.name] = container
        return my_rel_cont
        

class SimplePage(BasicPage):
    class Meta:
        verbose_name = "Page - Simple page"
        verbose_name_plural = "Page - Simple pages"
        app_label = 'www'

    def save(self):
        self.module = 'Simple'
        self.app_slug = APP_SLUGS
        super(SimplePage, self).save()


# -----
# OLD


#
# DASHBOARD
# Dashboard is an information page layout that display preview and modules
#
from vcms.www.managers.containers import DashboardElementManager

class PageElementPosition(models.Model):
    #PREVIEW
    LEFT = 'left'
    RIGHT = 'right'
    FLOAT_TYPE = ((LEFT, _('Left')), (RIGHT, _('Right')),)
    TOP = 1
    MIDDLE = 2
    BOTTOM = 3
    PRIORITY = ((TOP,_('Top')),(MIDDLE,_('Middle')),(BOTTOM,_('Bottom')),)
    preview_position = models.CharField(max_length=10, choices=FLOAT_TYPE)
    preview_display_priority = models.IntegerField(choices=PRIORITY)

    class Meta:
        abstract = True
        app_label = "www"
        
        
class DashboardPage(BasicPage):
    EMPTY = 0
    NEWS = 1
    SIMTHETIQ = 2
    TEMPLATES = ((EMPTY, 'Clean'),
                 (SIMTHETIQ, 'Simthetiq Home Page'),)
    TEMPLATE_FILES = { EMPTY: 'dashboard.html',
                      SIMTHETIQ: 'simthetiq_dashboard.html',}

    class Meta:
        verbose_name = "Dashboard"
        verbose_name_plural = "Dashboards"
        app_label = 'www'

    def save(self):
        self.module = 'Dashboard'
        self.app_slug = APP_SLUGS
        super(DashboardPage, self).save()


class DashboardElement(PageElementPosition):
    """ Text holder that are display in a dashboard element
    """
    name = models.CharField(max_length=36)
    page = models.ForeignKey(DashboardPage)
    text = models.TextField()
    published = models.BooleanField()
    link = models.URLField(verify_exists=True, null=True, blank=True)

    objects = DashboardElementManager()

    class Meta:
        app_label = 'www'
        
    def __unicode__(self):
        return self.name


class DashboardPreview(PageElementPosition):
    from vcms.www.models.old import Content
    page = models.ForeignKey(DashboardPage)
    preview = models.ForeignKey(Content)

    class Meta:
        app_label = 'www'
        
    def __unicode__(self):
        return self.preview.name


