# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User

from vcms.apps.www.managers import BannerManager#, BannerImageManager, ContentManager, QuickLinksManager
from vcms.apps.www.managers import BannerImageManager
from vcms.apps.www.managers import ContentManager
from vcms.apps.www.managers import QuickLinksManager
from vcms.apps.www.managers.page import LanguageManager




#from vcms.apps.www.fields import StatusField

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

from vcms.apps.www.models.page import Page
from vcms.apps.www.models.page import BasicPage
#from vcms.apps.www.models.page import SimplePage

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

class MenuSeparator(Page):
    external_link = models.URLField(max_length=200, null=True, blank=True)
    def save(self):
        self.slug = self.get_absolute_url()
        self.status = StatusField.PUBLISHED
        self.language = Language.objects.getDefault()
        self.module = "Separator"
        super(MenuSeparator, self).save()

    def get_absolute_url(self):
        return "/" + self.external_link

class MenuLocalLink(Page):
    """ MenuLocalLink is to link static page dynamicaly into the menu
        Let sta
    """
    local_link = models.CharField(max_length=200, null=True, blank=True,
                                  help_text="Link on this web site. ex. /www/page/")
    def save(self):
        self.status = StatusField.PUBLISHED
        self.language = Language.objects.getDefault()
        self.module = "LocalLink"
        try:
            if self.local_link[-1:] == '/' and len(self.local_link) > 1:
                self.local_link = self.local_link[:-1]
        except:
             self.local_link = ''
        self.slug = self.get_absolute_url()
        super(MenuLocalLink, self).save()

class QuickLinks(models.Model):
    """ Like bookmark, enable to put side links to local webpage
    """
    name = models.CharField(max_length="40", help_text="Max 40 characters")
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

# -- CONTENT
# ----------
class Content(models.Model):
    #CONTENT
    name = models.CharField(max_length="40", help_text="Max 40 characters")
    excerpt = models.TextField(verbose_name="Preview")
    content = models.TextField()
    published = models.BooleanField(default=False)

    #position
    POSITION_HELP_TEXT = _("Supported value are 'Default', px, em or %")
    width = models.CharField(max_length="40", default='Default', help_text=POSITION_HELP_TEXT)
    height = models.CharField(max_length="40", default='Default', help_text=POSITION_HELP_TEXT)
    margin_top = models.CharField(max_length="40", default='Default', help_text=POSITION_HELP_TEXT)
    margin_left = models.CharField(max_length="40", default='Default', help_text=POSITION_HELP_TEXT)
    position = models.IntegerField(default=5, help_text="Priority to display. 0=top, 9=bottom")

    #appearance
    TEXT_ONLY = 0
    BOXED = 1
    DARK = 2
    AVAILABLE_STYLES = ((TEXT_ONLY, _('Text only'))
                 ,(BOXED, _('Box'))
                 ,(DARK, _('Bright text on dark background'))
                 )
    style = models.IntegerField(default=TEXT_ONLY, choices=AVAILABLE_STYLES)
    minimized = models.BooleanField(default=False, choices=((True, _('Minimized')),(False, _('Show'))))

    #INFORMATION
    date = models.DateField(auto_now=True, editable=True)
    author = models.ForeignKey(User, editable=False, null=True, blank=True)
    page = models.ForeignKey(Page)

    objects = ContentManager()

    class Meta:
        verbose_name_plural = "Page content"
        ordering = [ 'position', 'date']

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
        return BannerImage.objects.get_banner_images(self)

    def get_random_image(self):
        import random
        images = BannerImage.objects.get_banner_images(self)
        images_len = len(images)
        if images_len == 0 or images_len == 1:
            return images
        else:
            random = random.randrange(0,images_len)
            rimage = images[random]
            print("RIMAGE URL = %s" % rimage.file)
            return [rimage]

    def get_size(self):
        return (self.width, self.height)

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
    trigger=lambda indexer, obj: obj.status == StatusField.PUBLISHED

class ContentIndexer(djapian.Indexer):
    fields=["text"]
    tags=[
        ("name",  "name" ),
        ("content",   "content")
         ]
    trigger=lambda indexer, obj: obj.page.status == StatusField.PUBLISHED


djapian.add_index(Page, PageIndexer, attach_as="indexer")
djapian.add_index(Content, ContentIndexer, attach_as="indexer")
"""
