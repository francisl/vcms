from django.db import models

from django.utils.translation import ugettext_lazy as _

# CMS
from vcms.www.models.page import BasicPage
from vcms.image_gallery.managers import ImageGalleryPageManager
from site_media.models import Image
from site_media.models import ImageCategory

APP_SLUGS = "gallery"

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
        self.app_slug = APP_SLUGS
        super(ImageGalleryPage, self).save()
        
    def get_containers(self):
        from vcms.www.models.containers import RelativeContainer
        my_rel_cont = {} 
        for container in RelativeContainer.objects.filter(page=self): 
            my_rel_cont[container.name] = container
        return my_rel_cont

    def get_absolute_url(self):
        return "/%s/%s" % (self.app_slug, self.slug)
        
    def get_menu(self):
        try:
            return self.menu.all()[0]
        except:
            return None

    def get_image_categories(self):
        return self.display_category.all()
    
    def get_all_images(self):
        return Image.objects.filter(category__in=self.display_category.all()).order_by('-date_modified', '-date_created')

    def get_all_images_for_category(self, category):
        if category:
            return Image.objects.filter(category=category).order_by('-date_modified', '-date_created')
        else:
            return []

    def get_controller(self):
        from vcms.image_gallery.views import gallery
        return gallery
    
