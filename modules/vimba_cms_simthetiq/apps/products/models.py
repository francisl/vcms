# encoding: utf-8

from __future__ import division

import Image as ImageLib
import os
from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User

#from tagging.fields import TagField
from vimba_cms.apps.www.models import Page, Language
from vimba_cms_simthetiq.apps.products.managers import ProductPageManager


# -- variable
PRODUCT_IMAGES = "static/uploadto/product_images/"
PRODUCT_VIDEOS = "static/uploadto/product_videos/"
APP_SLUGS = "products"

# -- GENERAL FUNCTION
# -- ----------------
def _save_thumbnail(self, fileName, url="static/uploadto/misc/", size=(100,40), genthumbnail=True ):
    if self.file:
        #filename = fileName
        if genthumbnail:
            fs = FileSystemStorage()
            image = ImageLib.open(str(fileName))

            original_ratio = image.size[0] / image.size[1]
            required_ratio = size[0] / size[1]

            if original_ratio > required_ratio:
                # The image is too large
                correct_width = int(required_ratio / original_ratio * image.size[0])
                # Computing the bounding box
                left = (image.size[0] - correct_width) // 2
                right = left + correct_width
                upper = 0
                lower = image.size[1] - 1   # Pixels are indexed from zero
                bounding_box = (left, upper, right, lower)
                image = image.crop(bounding_box)
            elif original_ratio < required_ratio:
                # The image is too high
                correct_height = int(original_ratio / required_ratio * image.size[1])
                # Computing the bounding box
                left = 0
                right = image.size[0] - 1   # Pixels are indexed from zero
                upper = (image.size[1] - correct_height) // 2
                lower = upper + correct_height
                bounding_box = (left, upper, right, lower)
                image = image.crop(bounding_box)

            image.thumbnail(size)
            filename = self.file.name.split("/")[-1].split('.')
            thumbname = str(filename[0] + "_tn." + str(filename[1]))
            image.save(fs.location + "/" + url + thumbname)
            self.thumbnail = url + thumbname

# -- LICENCES
# -- --------
class Licence(models.Model):
    display_name = models.CharField(max_length=50)
    term = models.TextField()
    language = models.ForeignKey(Language)
    #lang = models.IntegerField(max_length=2,choices=settings.LANGUAGES, 
    #                           default=settings.DEFAULT_LANGUAGE, db_index=True, editable=False)

# -- TAGS
# -------
class MediaTags(models.Model):
    tagname = models.CharField(max_length=30, unique=True)

    class Meta:
        verbose_name_plural = "Product Media Tags"
        
    def __unicode__(self):
        return self.tagname

""" Create a translation table 
    This way, only one tag need to be links in the models instead of 
    tagging each translation 
"""
class MediaTagsTranslation(models.Model):
    tag = models.ForeignKey(MediaTags)
    language = models.ForeignKey(Language)
    tagname = models.CharField(max_length=30)

# -- PRODUCTS
# -- --------
class Image(models.Model):
    name = models.CharField(max_length=150, unique=True)
    file = models.FileField(upload_to=PRODUCT_IMAGES)
    description = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(MediaTags)
    file_size = models.IntegerField(editable=False, blank=True, null=True, default=0)
    thumbnail = models.FileField(upload_to=PRODUCT_IMAGES, blank=True, null=True)
    show_in_gallery = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.name
    
    def save(self):
        super(Image, self).save()
        #tumbnail = _save_thumbnail(self, self.file.path, url=PRODUCT_IMAGES)
        self.file_size = int(os.path.getsize(self.file.path))
        super(Image, self).save()
        

class Video(models.Model):
    name = models.CharField(max_length=150, unique=True)
    #category = models.ForeignKey(Category)
    file = models.FileField(upload_to=PRODUCT_VIDEOS)
    description = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(MediaTags)
    file_size = models.IntegerField(editable=False, blank=True, null=True, default=0)
    thumbnail = models.ImageField(upload_to=PRODUCT_VIDEOS, blank=True, null=True, default="static/img/default/media/video.png")
    
    def __unicode__(self):
        return self.name
    
    def save(self):
        super(Video, self).save()
        #_save_thumbnail(self, url=PRODUCT_VIDEOS, genthumbnail=False)
        self.file_size = int(os.path.getsize(self.file.path))
        super(Video, self).save()

class FileFormat(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=4, unique=True)

    def __unicode__(self):
        return self.name

class DomainPage(Page):
    content = models.TextField()
    video = models.ForeignKey(Video, null=True, blank=True)
    file_format = models.ManyToManyField(FileFormat)
    
    class Meta:
        verbose_name_plural = "Domain - Pages"
        
    def __unicode__(self):
        return self.name
    
    def save(self):
        self.module  = 'Domain'
        self.app_slug = APP_SLUGS
        super(DomainPage, self).save()
        

class DomainElement(models.Model):
    name = models.CharField(max_length=36)
    page = models.ForeignKey(DomainPage)
    content = models.TextField()
    images = models.ManyToManyField(Image, blank=True)
    videos = models.ManyToManyField(Video, blank=True)
    published = models.BooleanField(default=False)
    display = models.BooleanField(default=True, choices=((True, 'Show'),(False, 'Hide')))
    position = models.IntegerField(default=5, help_text="Priority to display. 0=top, 9=bottom")
    
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['position']

class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField()
    domain = models.ForeignKey(DomainPage)
    
    class Meta:
        verbose_name_plural = "Domain - Categories"
        ordering = ["name"]
    
    def __unicode__(self):
        return self.name


class ProductPage(Page):
    #name = models.CharField(max_length=50, unique=True)
    product_description = models.TextField()
    product_id = models.IntegerField()
    polygon = models.IntegerField()
    texture_format = models.CharField(max_length=50)
    texture_resolution = models.CharField(max_length=50)
    original_image = models.ImageField(upload_to=PRODUCT_IMAGES)
    category = models.ForeignKey(Category)
    file_format = models.ManyToManyField(FileFormat)
    similar_products = models.ManyToManyField('self', symmetrical=True, null=True, blank=True)
    images = models.ManyToManyField(Image, blank=True)
    videos = models.ManyToManyField(Video, blank=True)
    previous = models.ForeignKey('self', related_name="previous_product", null=True, blank=True)
    next = models.ForeignKey('self', related_name="next_product", null=True, blank=True)
    
    # Set customer manager
    objects = ProductPageManager()
    
    class Meta:
        verbose_name_plural = "Product - Pages"
        ordering = ['category', 'name']
        
    def __unicode__(self):
        return self.name

    def save(self, reorder=True):
        self.module  = 'Product'
        self.app_slug = APP_SLUGS
        """ save one time before, this enable the paginator to find de product in the right order """
        super(ProductPage, self).save()

        if reorder:
            """ by default, will reorder the paginator built-in """
            ProductPage.objects.set_product_position(self)

        super(ProductPage, self).save()
        
    def delete(self):
        print("delete is getting called")
        ProductPage.objects.remove_product_position(self)
        super(ProductPage, self).delete()
        
    def pre_delete(self):
        print("pre_delete is getting called")
        ProductPage.objects.remove_product_position(self)
        

# -- CONTENT
# ----------
class ProductContent(models.Model):
    #CONTENT
    title = models.CharField(max_length="60", help_text="Max 60 characters")
    content = models.TextField()
    published = models.BooleanField(default=False)
    position = models.IntegerField(default=5, help_text="Priority to display. 0=top, 9=bottom")
    
    #INFORMATION
    date = models.DateField(auto_now=True, editable=True)
    author = models.ForeignKey(User, editable=False, null=True, blank=True)
    page = models.ForeignKey(ProductPage)

    class Meta:
        verbose_name_plural = "Page Product content"
        ordering = ['position']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        self.page.get_absolute_url()


class GalleryPage(Page):
    class Meta:
        verbose_name_plural = "Gallery - Gallery"
        
    def __unicode__(self):
        return self.name
    
    def save(self):
        self.module  = 'GalleryPage'
        self.app_slug = APP_SLUGS
        super(GalleryPage, self).save()
        
    def get_absolute_url(self):
        return self.app_slug + "/" + self.slug
    
"""
import djapian
class ProductInformationIndexer(djapian.Indexer):
    fields=["text"]
    tags=[
        ("product",  "product.name" ),
        ("description",   "description"),
        ("keywords",    "keywords"  )
         ]

djapian.add_index(ProductInformation, ProductInformationIndexer, attach_as="indexer")

"""