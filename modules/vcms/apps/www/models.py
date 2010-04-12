# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie

import datetime, Image, os
from django.utils.translation import ugettext_lazy as _
from django.db import models
#from django.contrib import admin
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.storage import default_storage, FileSystemStorage
from vcms.apps.www.managers import PageManager, ContentManager, BannerManager, BannerImageManager, DashboardElementManager, LanguageManager


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

#class MenuGroup(models.Model):
#    name = models.CharField(max_length=100, unique=True, help_text=_('Max 100 characters.'))
 
    
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
    """ A page is a placeholder accessible by the user that represents a section content
        Like a news page, a forum page with multiple sub-section, a contact page ...
        A page can have multiple sub-section define in the application urls
        
        -- Link
        The CMS generate links to make these placeholder accessible in menus
        it uses the follow pattern : /{APP_SLUGS}/page/{page_slug}/
        ex: A basic Page model will be accessible at : /www/page/examplepage
            A news page model will be accessible at : /news/page/newspage
    
        --Menu
        The models keep a ordered tree that represents the structure and ordering
        of the pages. This is used to generate main/sub menu.
        
        -- Language
        Page can be classified by language - NOTE not yet working
        # TODO : add multi-language fonctionnality
         
    """
    DRAFT = 0
    PUBLISHED = 1
    STATUSES = (
        (DRAFT, _('Draft')),
        (PUBLISHED, _('Published')),
    )
    name = models.CharField(max_length=100, unique=True, help_text=_('Max 100 characters.'))
    slug = models.SlugField(max_length=150, unique=True, help_text=_("Used for hyperlinks, no spaces or special characters."))
    description = models.CharField(max_length=250, help_text=_("Short description of the page (helps with search engine optimization.)"))
    keywords = models.CharField(max_length=250, null=True, blank=True, help_text=_("Page keywords (Help for search engine optimization.)"))
    app_slug = models.SlugField(default="", editable=False)
    status = models.IntegerField(choices=STATUSES, default=DRAFT)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_modified = models.DateTimeField(auto_now=True, editable=False)
    date_published = models.DateTimeField(default=datetime.datetime.min, editable=False)

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
    objects = PageManager()

    class Meta:
        ordering = ['tree_position','name']
        verbose_name_plural = "Menu Administration"
        unique_together = ("slug", "app_slug")

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
        # If the status has been changed to published, then set the date_published field so that we don't reset the date of a published page that is being edited
        if self.status == self.PUBLISHED:
            # If the page is being created, set its published date
            if not self.pk:
                self.date_published = datetime.datetime.now()
            # If the Page is being edited, check against the current version in the database and update if it hasn't been previously published
            else:
                model_in_db = Page.objects.get(pk=self.pk)
                if model_in_db.status != self.PUBLISHED:
                    self.date_published = datetime.datetime.now()
        super(Page, self).save()
        # __TODO: Commented out the following line as it doesn't work as of 31-01-2010
        #self.indexer.update()

    def delete(self):
        if self.default:
            Page.objects.deleted_Default()
        _delete_page(self)
        super(Page, self).delete()
        # __TODO: Commented out the following line as it doesn't work as of 31-01-2010
        #self.indexer.update()

class MenuSeparator(Page):  
    def save(self):
        self.slug = self.name
        self.status = self.PUBLISHED
        self.language = Language.objects.getDefault()
        self.module = "Separator"
        super(MenuSeparator, self).save()
        
    def get_absolute_url(self):
        return False
            
    
class SimplePage(Page):
    class Meta:
        verbose_name = "Simple page"
        verbose_name_plural = "Simple pages"

    def __unicode__(self):
        return self.name

    def save(self):
        self.module = 'Simple'
        self.app_slug = APP_SLUGS
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
    page = models.ForeignKey(Page)
    
    objects = ContentManager()
    
    class Meta:
        verbose_name_plural = "Page content"
        ordering = ['position', 'date']
    
    def __unicode__(self):
        return self.name
        
    def get_absolute_url(self):
        self.page.get_absolute_url()

class Banner(models.Model):
    SLIDESHOW = 0
    RANDOM = 1
    DISPLAY_CHOICES = ((SLIDESHOW, _("Slideshow")),(RANDOM, _("Random")))
    name = models.CharField(max_length=90)
    description = models.TextField(blank=True, null=True)
    page = models.ManyToManyField(Page, null=True, blank=True)
    style = models.IntegerField(choices=DISPLAY_CHOICES, default=SLIDESHOW)
    width = models.IntegerField(default=955)
    height = models.IntegerField(default=300)
    
    objects = BannerManager()
    
    def __unicode__(self):
        return self.name
    
    def get_images(self):
        return BannerImage.objects.get_banner_image_for_page(self)

class BannerImage(models.Model):
    FILE_PATH = "uploadto/banners"
    name = models.CharField(max_length=90)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to=FILE_PATH)
    url = models.URLField(max_length=200, null=True, blank=True)
    banner = models.ManyToManyField(Banner)

    objects = BannerImageManager()
    
    def __unicode__(self):
        return self.name
    
    def save(self):
        #from vcms.tools.image import image_resize as ir
        #super(BannerImage, self).save()
        #self.banner = ir.save_resized_image(self, self.file, self.file.path, tuple((955, 300)), False)
        super(BannerImage, self).save()
        
    
# DASHBOARD
# -- ------
# Dashboard is an information page layout that display preview and modules

class DashboardPage(Page):
    EMPTY = 0
    NEWS = 1
    CONTACT = 2
    SIMTHETIQ = 3
    TEMPLATES = ((EMPTY, 'Clean'),
                 (CONTACT, 'Contact Form'),
                 (SIMTHETIQ, 'Simthetiq Home Page'),)
    TEMPLATE_FILES = { EMPTY: 'dashboard.html',
                      SIMTHETIQ: 'simthetiq_dashboard.html',}
    template = models.IntegerField(default=EMPTY, choices=TEMPLATES)
    
    class Meta:
        verbose_name = "Dashboard"
        verbose_name_plural = "Dashboards"
        
    def __unicode__(self):
        return self.name
    
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
