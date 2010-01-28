# encoding: utf-8

from __future__ import division

import Image as ImageLib
from vimba_cms_simthetiq.tools import magic # http://www.jsnp.net/code/magic.py
from zope.mimetype import typegetter # http://pypi.python.org/pypi/zope.mimetype/1.2.0
import os
from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete


#from tagging.fields import TagField
from vcms.apps.www.models import Page, Language
from vimba_cms_simthetiq.apps.products.managers import ProductPageManager

# -- variable
PRODUCT_IMAGES = "uploadto/product_images/"
PRODUCT_VIDEOS = "uploadto/product_videos/"
APP_SLUGS = "products"


# -- Validators
# -- ----------------
def validate_video_mime_type(value):
    """
        Validator that raises a ValidationError exception if the MIME type is not
        contained within the list of supported video MIME types as specified in
        the Video model.
    """
    if not value in Video.SUPPORTED_MIME_TYPES:
        from django.core.exceptions import ValidationError
        raise ValidationError("The video file supplied is not supported. Only MOV and flash videos are supported at the moment.")


# -- GENERAL FUNCTION
# -- ----------------
def _save_thumbnail(self, fileName, url="uploadto/misc/", size=(100,40), genthumbnail=True ):
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
    tagname = models.CharField(max_length=30, unique=True, null=False, blank=False)

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
    tags = models.ManyToManyField(MediaTags, blank=True, null=True,)
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
    
    def delete(self):
        """ remove foreign object link
            this prevent cascade deletion of pages when link to image
            this 
        """
        
        for p in self.original_image.all():
            #print("Link original : %s" % p)
            self.original_image.remove(p)
        
        for p in self.productpage_set.all():
            #print("Link normal : %s" % p)
            self.productpage_set.remove(p)
        
        super(Image, self).delete()
        
    def get_absolute_url(self):
        #return str(settings.MEDIA_URL) + str(self.file)
        #return str(settings.MEDIA_ROOT) + str(self.file)
        return self.file

class Video(models.Model):
    # Warning: validate changes in supported MIME types list against the validate_video_mime_type validator
    SUPPORTED_MIME_TYPES = ['application/x-shockwave-flash', 'video/quicktime', 'video/x-flv']

    default_image = "CustomThemes/Simthetiq/images/default/media/video.png"
    name = models.CharField(max_length=150, unique=True)
    #category = models.ForeignKey(Category)
    file = models.FileField(upload_to=PRODUCT_VIDEOS)
    description = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(MediaTags)
    file_size = models.IntegerField(editable=False, blank=True, null=True, default=0)
    mime_type = models.CharField(editable=False, max_length=255) # http://stackoverflow.com/questions/643690/maximum-mimetype-length-when-storing-type-in-db
    thumbnail = models.ImageField(upload_to=PRODUCT_VIDEOS, blank=True, null=True, default=default_image)

    def __unicode__(self):
        return self.name

    def clean(self):
        # Set the video's filesize and its MIME type,
        # then validate its MIME type against the list of supported MIME types
        if self.file:
            self.file_size = self.file.size
            file_data = self.file.read(8192)
            # Try to get the MIME type with magic as Zope doesn't seem to be able to recognize JPEG's magic number
            # and magic fixes that problem but is an old library that may have an outdated MIME types/magic numbers collection
            mimetype = magic.whatis_noguessing(file_data)
            # If magic couldn't determine the MIME type, then try with Zope
            # If smartMimeTypeGuesser can't find the MIME type according to the file's magic number, then it will use the file's extension
            if not mimetype:
                #print 'USING ZOPE'
                mimetype = typegetter.smartMimeTypeGuesser(name=self.file.path, data=file_data)
            #print 'FOUND MIMETYPE: ' + mimetype
            self.mime_type = mimetype
            validate_video_mime_type(self.mime_type)
    
    def delete(self):
        """ remove foreign object link
            this prevent cascade deletion of pages when link to image
            this 
        """
        self.domainpage_set.clear()
        super(Video, self).delete()

class FileFormat(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=4, unique=True)

    def __unicode__(self):
        return self.name

    def delete(self):
        """ remove foreign object link
            this prevent cascade deletion of pages when link to image
            this 
        """
        self.domainpage_set.clear()
        super(FileFormat, self).delete()
        
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
    
    def delete(self):
        """ remove foreign object link
            this prevent cascade deletion of pages when link to image
            this 
        """
        self.category_set.clear()
        super(DomainPage, self).delete()

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
    domain = models.ForeignKey(DomainPage, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Domain - Categories"
        ordering = ["name"]
    
    def __unicode__(self):
        return self.name

    def delete(self):
        """ remove foreign object link
            this prevent cascade deletion of pages when link to image
            this 
        """
        print("clearing product link !")
        print("linked to : %s " % self.productpage_set.all())
        self.productpage_set.clear()
        super(Category, self).delete()

            
class ProductPage(Page):
    #name = models.CharField(max_length=50, unique=True)
    product_description = models.TextField()
    product_id = models.IntegerField()
    polygon = models.IntegerField()
    texture_format = models.CharField(max_length=50)
    texture_resolution = models.CharField(max_length=50)
    #original_image = models.ImageField(upload_to=PRODUCT_IMAGES)
    original_image = models.ForeignKey(Image, related_name="original_image", null=True, blank=True)
    category = models.ForeignKey(Category, null=True, blank=True)
    file_format = models.ManyToManyField(FileFormat)
    similar_products = models.ManyToManyField('self', symmetrical=True, null=True, blank=True)
    images = models.ManyToManyField(Image, null=True, blank=True)
    videos = models.ManyToManyField(Video, null=True, blank=True)
    previous = models.ForeignKey('self', related_name="previous_product", null=True, blank=True)
    next = models.ForeignKey('self', related_name="next_product", null=True, blank=True)
    
    # Set customer manager
    objects = ProductPageManager()
    
    class Meta:
        verbose_name = "Product - Page"
        verbose_name_plural = "Product - Pages"
        ordering = ['category', 'name']
        
    def __unicode__(self):
        return self.name

    def save(self, reorder=True):
        #print("saving product ...")
        self.module  = 'Product'
        self.app_slug = APP_SLUGS
        if reorder:
            """ save one time before, this enable the paginator to find de product in the right order """
            super(ProductPage, self).save()
            """ by default, will reorder the paginator built-in """
            ProductPage.objects.set_product_position(self)

        super(ProductPage, self).save()
        
    def delete(self):
        #print("---------------------")
        #print("deleting %s" % self)
        try:
            if self.previous == self:
                #print("previous == self")
                self.previous = None
        except:
            #print("previous product doesn't exist")
            self.previous = None
            
        try:
            if self.next == self:
                #print("next == self")
                self.next = None
        except:
            #print("next product doesn't exist")
            self.next = None
        #self.save(reorder=False)
        
        # set previous product next and next product previous
        ProductPage.objects.set_previous_next_product(self, self.previous, self.next)

        try:
            #print("self.previous %s" % self.previous)
            #print("self.next %s" % self.next)    

            #remove all next and previous including self
            ProductPage.objects.remove_previous_link(self)
            ProductPage.objects.remove_next_link(self)
            
        except:
            pass
        
        
        self.next = None
        self.previous = None
        #self.save(reorder=False)
        super(ProductPage, self).delete()
        
#def pre_delete_action(sender, instance, **kwargs):
    #print("instance = %s" % instance)
    #print("instance previous = %s" % instance.previous)
    #print("instance next = %s" % instance.next)
    #if instance.mark_for_delete == True:
    #    return True
    
#pre_delete.connect(pre_delete_action, sender=ProductPage, weak=False)
    
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
