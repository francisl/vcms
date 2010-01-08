# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie

import Image, os, datetime
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.storage import default_storage, FileSystemStorage
from vcms.apps.www.managers import PageManager, BannerManager, DashboardElementManager, LanguageManager


# -- variable
PRODUCT_IMAGES = "uploadto/prod_images"
PRODUCT_VIDEOS = "uploadto/prod_videos"
APP_SLUGS = "www"

class Language(models.Model):
    language = models.CharField(max_length=50, help_text=_('Max 50 characters.'))
    language_code = models.CharField(max_length=2, primary_key=True, help_text=_('e.g. fr = French or en = english'))
    
    objects = LanguageManager()
    
    def __unicode__(self):
        return self.language
    
# -- Pages
# -- -----
class PageElementPosition(models.Model):
    #PREVIEW
    LEFT = 'left'
    RIGHT = 'right'
    FLOAT_TYPE = ((LEFT, 'Left'), (RIGHT, 'Right'),)
    TOP = 1
    MIDDLE = 2
    BOTTOM = 3
    PRIORITY = ((TOP,'Top'),(MIDDLE,'Middle'),(BOTTOM,'Bottom'),)
    preview_position = models.CharField(max_length=10, choices=FLOAT_TYPE)
    preview_display_priority = models.IntegerField(choices=PRIORITY)
    
    class Meta:
        abstract = True

def _delete_page(page2delete):
    """ Move submenu up one level """
    pages = Page.objects.filter(parent=page2delete.id)
    #print("menus : %s" % menus)
    if pages:
        for page in pages:
            if page.level != 0: # root = 0, no less
                # put menu one level up
                page.level = page.level - 1
                page.parent = page2delete.parent
            page.save()
            # check if menu has children, a level up them too
            _delete_page(page)

class Page(models.Model):
    DRAFT = 0
    PUBLISHED = 1
    STATUSES = (
        (DRAFT, _('Draft')),
        (PUBLISHED, _('Published')),
    )
    name = models.CharField(max_length=100, unique=True, help_text=_('Max 40 characters.'))
    slug = models.SlugField(max_length=150, unique=True, help_text="used for link, no space or special caracter")
    description = models.CharField(max_length=250, help_text="Page short description (Help for search engine optimisation)")
    keywords = models.CharField(max_length=250, null=True, blank=True, help_text="Page keywords (Help for search engine optimisation)")
    app_slug = models.SlugField(default=APP_SLUGS, editable=False)
    status = models.IntegerField(choices=STATUSES, default=DRAFT)
    date_created = models.DateTimeField(default=datetime.datetime.today(), editable=False)
    date_modified = models.DateTimeField(auto_now=True, editable=False)

    # menus
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', editable=False)
    level = models.IntegerField(editable=False, default=0)
    tree_position = models.IntegerField(editable=False, default=0)
    display = models.BooleanField(editable=False, default=False)
    default = models.BooleanField(default=False, help_text="Check this if you want this page as default home page")
    
    # Parameteers
    language = models.ForeignKey(Language)
    # lang = models.IntegerField(max_length=2,choices=settings.LANGUAGES, 
    #                       default=settings.DEFAULT_LANGUAGE, db_index=True, editable=False)

    # Controler for the pages
    module = models.CharField(max_length=30, default='Simple', editable=False)
    objects = PageManager()

    class Meta:
        verbose_name_plural = "Menu Administration"
        ordering = ['tree_position','name']

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        if self.app_slug:
            return "/" + self.app_slug + "/page/" + self.slug
        else:
            return "/" + self.slug

    def get_name(self):
        return self.name

    def save(self):
        if self.default:
            Page.objects.reset_Default()
        super(Page, self).save()
        self.indexer.update()

    def delete(self):
        if self.default:
            Page.objects.deleted_Default()
        _delete_page(self)
        super(Page, self).delete()
        self.indexer.update()


class SimplePage(Page):
    class Meta:
        verbose_name_plural = "Pages - Simple"

    def __unicode__(self):
        return self.name

    def save(self):
        self.module = 'Simple'
        super(SimplePage, self).save()


# -- CONTENT
# ----------
class Content(models.Model):
    #CONTENT
    name = models.CharField(max_length="40", help_text="Max 40 characters")
    excerpt = models.TextField(verbose_name="Preview")
    content = models.TextField()
    published = models.BooleanField(default=False)
    display = models.BooleanField(default=True, choices=((True, 'Show'),(False, 'Hide')))
    position = models.IntegerField(default=5, help_text="Priority to display. 0=top, 9=bottom")
    
    #INFORMATION
    date = models.DateField(auto_now=True, editable=True)
    author = models.ForeignKey(User, editable=False, null=True, blank=True)
    page = models.ForeignKey(SimplePage)
    
    class Meta:
        verbose_name_plural = "Page content"
        ordering = ['position', 'date']
    
    def __unicode__(self):
        return self.name
        
    def get_absolute_url(self):
        self.page.get_absolute_url()

class Banner(models.Model):
    FILE_PATH = "static/uploadto/banners"
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to=FILE_PATH)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(max_length=200, null=True, blank=True)
    page = models.ManyToManyField(Page, null=True, blank=True)
    
    objects = BannerManager()
    
    def __unicode__(self):
        return self.name    

# DASHBOARD
# -- ------
# Dashboard is an information page layout that display preview and modules

class DashboardPage(Page):
    EMPTY = 0
    NEWS = 1
    CONTACT = 2
    TEMPLATES = ((EMPTY, 'Clean'),
                        #(NEWS, 'News'),
                        (CONTACT, 'Contact Form'),)
    template = models.IntegerField(default=EMPTY, choices=TEMPLATES)
    
    class Meta:
        verbose_name_plural = "Pages - Dashboard"
        
    def __unicode__(self):
        return self.name
    
    def save(self):
        self.module = 'Dashboard'
        super(DashboardPage, self).save()

class DashboardElement(PageElementPosition):
    name = models.CharField(max_length=36)
    page = models.ForeignKey(DashboardPage)
    text = models.TextField()
    published = models.BooleanField()
    link = models.URLField(verify_exists=True, null=True, blank=True)

    objects = DashboardElementManager()
    
    def __unicode__(self):
        return self.name

class DashboardPreview(PageElementPosition):
    page = models.ForeignKey(DashboardPage)
    preview = models.ForeignKey(Content)
    
    def __unicode__(self):
        return self.preview.name


"""
TODO : remake djapian code to haystack code
import djapian
class PageIndexer(djapian.Indexer):
    fields=["text"]
    tags=[
        ("name",  "name" ),
        ("description",   "description"),
        ("keywords",    "keywords"  )
         ]
    trigger=lambda indexer, obj: obj.status == Page.PUBLISHED

class ContentIndexer(djapian.Indexer):
    fields=["text"]
    tags=[
        ("name",  "name" ),
        ("content",   "content")
         ]
    trigger=lambda indexer, obj: obj.page.status == Page.PUBLISHED


djapian.add_index(Page, PageIndexer, attach_as="indexer")
djapian.add_index(Content, ContentIndexer, attach_as="indexer")
"""
