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

from vcms.www.models.menu import CMSMenu
from vcms.www.models.language import Language

from vcms.www.managers.page import BasicPageManager

STATUS_DRAFT = 0
STATUS_PUBLISHED = 1
STATUSES = (
    (STATUS_PUBLISHED, _('Draft')),
    (STATUS_PUBLISHED, _('Published')),
)

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
    name = models.CharField(max_length=100, unique=False, help_text=_('Max 100 characters.'))
    
    status = models.PositiveIntegerField(choices=STATUSES, default=STATUSES[STATUS_DRAFT])

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

    # Generic FK to the container, used as an inheritance workaround
    #widget_type = models.ForeignKey(ContentType)
    #widget_id = models.PositiveIntegerField()
    #widget = generic.GenericForeignKey('widget_type', 'widget_id')

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
        if Page.objects.filter(pk=self.pk).exists():
            return Page
        elif MainPage.objects.filter(pk=self.pk).exists():
            return MainPage
        elif SimplePage.objects.filter(pk=self.pk).exists():
            return SimplePage
        else:
            return BasicPage

    def get_name(self):
        return self.__unicode__()

    def get_absolute_url(self):
        return "/%s/%s" % (self.app_slug, self.slug)

    def _add_to_main_menu(self, root):
        root.add_child(menu_name=self.name, content_object=self)

    def get_containers():
        raise NotImplementedError()

    @staticmethod
    def get_page_containers():
        raise NotImplementedError()
    
    @staticmethod
    def get_menu(self):
        raise NotImplementedError()
        
    def save(self):
        if not self.app_slug:
            self.app_slug='www'
        super(BasicPage, self).save()

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
        verbose_name = "Page - Main page"
        verbose_name_plural = "Page - Main pages"

    def save(self):
        self.module = 'MainPage'
        super(BlankPage, self).save()
    
    def get_absolute_url(self):
        return "/www/page/" + self.slug
    
    @staticmethod
    def get_page_containers():
        from vcms.www.models.containers import ContainerDefinition
        from vcms.www.models.containers import GridContainer
        from vcms.www.models.containers import TableContainer
        from vcms.www.models.containers import RelativeContainer
        return { "navigation_container": ContainerDefinition(_("Navigation"), RelativeContainer)
                    ,"main_content": ContainerDefinition(_("Content"), GridContainer) }

    def get_containers(self):
        instance_containers = {}
        for page_container_name, page_container_definition in self.__class__.get_page_containers().items():
            for container in page_container_definition.type.objects.filter(page=self).filter(name=page_container_name):
                instance_containers[page_container_name] = container
        return instance_containers

    def get_menu(self):
        return self.menu.all()[0]

class SimplePage(BasicPage):
    class Meta:
        verbose_name = "Page - Simple page"
        verbose_name_plural = "Page - Simple pages"
        app_label = 'www'

    def save(self):
        self.module = 'SimplePage'
        super(SimplePage, self).save()
    
    def get_absolute_url(self):
        return "/www/page/" + self.slug
    
    def get_containers(self):
        from vcms.www.models.containers import RelativeContainer
        my_rel_cont = {} 
        for container in RelativeContainer.objects.filter(page=self): 
            my_rel_cont[container.name] = container
        return my_rel_cont

    def get_menu(self):
        try:
            return self.menu.all()[0]
        except:
            return None
        
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


