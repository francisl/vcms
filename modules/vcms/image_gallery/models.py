from django.db import models

# CMS
from vcms.www.models import Language
from vcms.www.models.page import BasicPage
from site_media.models import ImageCategory
from vcms.image_gallery.managers import ImageGalleryPageManager
from django.utils.translation import ugettext_lazy as _

from site_media.models import Image

## PAGE
class ImageGalleryPage(BasicPage):
    display_category = models.ManyToManyField(ImageCategory)
    thumbnail_width = models.PositiveIntegerField(default=190, help_text=_("Image width in pixel"))
    thumbnail_height = models.PositiveIntegerField(default=150, help_text=_("Image height in pixel"))
    thumbnail_per_page = models.PositiveIntegerField(default=10, help_text=_("how many image(s) will be display per page"))
    display_image_name = models.BooleanField(default=False)
    
    objects = ImageGalleryPageManager()
    
    class Meta:
        verbose_name = "Page - Image Gallery page"
        verbose_name_plural = "Page - Image Gallery pages"

    def save(self):
        self.module = 'ImageGallery'
        super(ImageGalleryPage, self).save()
        
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

    def get_image_categories(self):
        return self.display_category.all()
    
    def get_all_images(self):
        return Image.objects.filter(category__in=self.display_category.all())

    def get_all_images_for_category(self, category):
        print( "category == %s" % self.display_category.all())
        print("category == %s" % category)
        #if category in self.display_category.all():
        if category:
            return Image.objects.filter(category=category)
        else:
            return self.get_all_images()