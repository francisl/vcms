# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: www
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 30-05-2010.
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from vcms.apps.www.fields import StatusField
from vcms.apps.www.models import Language
from vcms.apps.www.models import PageElementPosition
from vcms.apps.www.managers.containers import DashboardElementManager
from vcms.apps.www.managers.page import BasicPageManager
from vcms.apps.www.managers.page import LanguageManager

        
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
    app_slug = models.SlugField(default="", editable=False)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_modified = models.DateTimeField(auto_now=True, editable=False)
    date_published = models.DateTimeField(default=datetime.datetime.min, editable=False)

    objects = BasicPageManager()

    class Meta:
        verbose_name = _("Basic page")
        verbose_name_plural = _("Basic pages")

    def __unicode__(self):
        return self.name

    def get_name(self):
        return self.name

    def save(self):
        # If the status has been changed to published, then set the date_published field so that we don't reset the date of a published page that is being edited
        if self.status == StatusField.PUBLISHED:
            # If the page is being created, set its published date
            if not self.pk:
                self.date_published = datetime.datetime.now()
            # If the Page is being edited, check against the current version in the database and update if it hasn't been previously published
            else:
                model_in_db = Page.objects.get(pk=self.pk)
                if model_in_db.status != StatusField.PUBLISHED:
                    self.date_published = datetime.datetime.now()
        super(BasicPage, self).save()
        # __TODO: Commented out the following line as it doesn't work as of 31-01-2010
        #self.indexer.update()


class Page(BasicPage):
    EMPTY = 0
    TEMPLATES = ((EMPTY, 'Default'),)
    TEMPLATE_FILES = { EMPTY: 'master.html'}
    slug = models.SlugField(max_length=150, unique=True, help_text=_("Used for hyperlinks, no spaces or special characters."))
    description = models.CharField(max_length=250, help_text=_("Short description of the page (helps with search engine optimization.)"))
    keywords = models.CharField(max_length=250, null=True, blank=True, help_text=_("Page keywords (Help for search engine optimization.)"))
    template = models.IntegerField(default=EMPTY, choices=TEMPLATES)

    # menus
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', editable=False)
    level = models.IntegerField(editable=False, default=0)
    tree_position = models.IntegerField(editable=False, default=0)
    display = models.BooleanField(editable=False, default=False)
    default = models.BooleanField(default=False, help_text=_("Check this if you want this page as default home page."))

    # Parameteers
    language = models.ForeignKey(Language)
    # lang = models.IntegerField(max_length=2,choices=settings.LANGUAGES,
    #                       default=settings.DEFAULT_LANGUAGE, db_index=True, editable=False)

    # Controler for the pages
    module = models.CharField(max_length=30, default='', editable=False)
    #objects = PageManager()

    class Meta:
        ordering = ['tree_position', 'name']
        verbose_name_plural = "Menu Administration"
        #unique_together = ("slug", "app_slug")

    def get_absolute_url(self):
        if self.app_slug:
            return "/" + self.app_slug + "/page/" + self.slug
        elif self.slug == '/':
            return ''
        else:
            return "/" + self.slug

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


class SimplePage(Page):
    class Meta:
        verbose_name = "Simple page"
        verbose_name_plural = "Simple pages"

    def save(self):
        self.module = 'Simple'
        self.app_slug = APP_SLUGS
        super(SimplePage, self).save()

#
# DASHBOARD
# Dashboard is an information page layout that display preview and modules
#

class DashboardPage(Page):
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

    def __unicode__(self):
        return self.name


class DashboardPreview(PageElementPosition):
    from vcms.apps.www.models.widget import Content
    page = models.ForeignKey(DashboardPage)
    preview = models.ForeignKey(Content)

    def __unicode__(self):
        return self.preview.name
