import os

from django.db import models

# CMS
from site_language.models import Language
from site_media.managers import ImageCategoryManager

IMAGE_UPLOAD_TO = "uploadto/imagegallery/images/"

class ImageCategory(models.Model):
    default_name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=150, unique=True)
    
    objects = ImageCategoryManager()
    
    def __unicode__(self):
        return self.default_name
    
    def get_image_quantity(self):
        return len(Image.objects.filter(category=self))

class ImageCategoryTranslation(models.Model):
    name = models.CharField(max_length=150, unique=True)
    category = models.ForeignKey(ImageCategory)
    
    language = models.ForeignKey(Language, default=Language.objects.get_default_code())

# -- --------
class Image(models.Model):
    default_name = models.CharField(max_length=150, unique=True)
    file = models.FileField(upload_to=IMAGE_UPLOAD_TO)
    category = models.ManyToManyField(ImageCategory)
    file_size = models.IntegerField(editable=False, blank=True, null=True, default=0)
    
    def __unicode__(self):
        return self.default_name
    
    def save(self):
        super(Image, self).save()
        self.file_size = int(os.path.getsize(self.file.path))
        super(Image, self).save()
        
    def get_absolute_url(self):
        #return str(settings.MEDIA_URL) + str(self.file)
        #return str(settings.MEDIA_ROOT) + str(self.file)
        return self.file

class ImageDescription(models.Model):
    image = models.ForeignKey(Image)
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)
    language = models.ForeignKey(Language, default=Language.objects.get_default_code())
