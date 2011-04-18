from django.db import models
from django.utils.translation import ugettext_lazy as _

from vcms.www.managers.banner import BannerManager #, BannerImageManager, ContentManager, QuickLinksManager
from vcms.www.managers.banner import BannerImageManager
from vcms.www.models.page import BasicPage

# -- variable
APP_LABEL = "www"

class Banner(models.Model):
    SLIDESHOW = 0
    RANDOM = 1
    DISPLAY_CHOICES = ((SLIDESHOW, _("Slideshow")),(RANDOM, _("Random")))
    name = models.CharField(max_length=90)
    description = models.TextField(blank=True, null=True)
    page = models.ManyToManyField(BasicPage, null=True, blank=True)
    style = models.IntegerField(choices=DISPLAY_CHOICES, default=SLIDESHOW)
    width = models.IntegerField(default=955)
    height = models.IntegerField(default=300)

    objects = BannerManager()
    
    class Meta:
        app_label = APP_LABEL
        
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
            return [rimage]

    def get_size(self):
        return (self.width, self.height)

class BannerImage(models.Model):
    FILE_PATH = "uploadto/banners"
    name = models.CharField(max_length=90)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to=FILE_PATH)
    url = models.URLField(max_length=200, null=True, blank=True)
    banner = models.ManyToManyField(Banner, null=True, blank=True)

    objects = BannerImageManager()

    def image_thumbnail(self):
        banners = self.banner.all()
        if banners:
            banner = banners[0]
            return u'<div><img src="%s" width="%s" height="%s" /></div>' % (self.file.url, banner.width/3, banner.height/3)
    image_thumbnail.short_description = 'Thumbnail'
    image_thumbnail.allow_tags = True

    def displayed_in_banner(self):
        banners_text = '<ul>'
        for banner in self.banner.all():
            banners_text += ('<li>%s</li>' % banner)
        banners_text += '</ul>'
        return banners_text
    displayed_in_banner.short_description = 'Banners'
    displayed_in_banner.allow_tags = True
    
    class Meta:
        app_label = APP_LABEL
        
    def __unicode__(self):
        return self.name

    def save(self):
        super(BannerImage, self).save()

