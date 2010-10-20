# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: www
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 30-05-2010.

from django.db import models
from vcms.www.fields import StatusField
from django.conf import settings
from django.http import Http404

from site_language.models import Language

class BasicPageManager(models.Manager):
    def get_children(self, parent=None):
        if parent:
            return self.filter(parent=parent).filter(status=StatusField.PUBLISHED).filter(display=True)
        else:
            return None

    def get_default_page(self):
        return self.get_published()[0] #mm.content_object
    
    def get_all_basic(self):
        return self.filter(language=Language.objects.get_default())

    def get_main_published(self):
        return self.filter(status=StatusField.PUBLISHED).filter(level=0)

    def get_published(self):
        return self.filter(status=StatusField.PUBLISHED)

    def drafts(self):
        return self.filter(status=StatusField.DRAFT)

    def get_pages(self, lang='en'):
        lang = Language.objects.get_language(lang)
        return self.get_published().filter(language=lang)
        
    def get_containers(self):
        raise NotImplementedError
        
    def get_page_or_404(self, slug, app_slug):
        page = self.get_pages().filter(slug=slug).filter(app_slug=app_slug)
        if len(page) == 0:
            raise Http404
        return page[0]


class ContentManager(models.Manager):
    def get_contents_for_page(self, page=None):
        if page == None or page == "":
            return []
        else:
            return self.filter(page=page)


class BannerManager(models.Manager):
    def get_random_banner_image(self, banner):
        """ take a list of banners/images and select one randomly """
        import random
        #banner = has_banner = False # set no banners to default to reduce check exception
        #bannerqty = len(banners)
        try:    # only one banner
            randomnumber = random.randrange(0,len(banner))
            if bannerqty == 1:
                banner = banners[0]
                has_banner = True
            elif bannerqty > 1:
                randomnumber = random.randrange(0,bannerqty)
                # print ("random number : %s \nbannerqty = %s") % (randomnumber, bannerqty)
                banner = banners[randomnumber]
                has_banner = True
        finally:
            return banner, has_banner

    def get_random_banner_image_number(self, images):
        """ take size of image array, then give a random number"""
        import random
        if type(images) == type(0):
            images_len = len(images)
            if images_len == 1 :
                return images[0]
            elif images_len > 1 :
                return images[random.randrange(0, images_len-1)]

        return False

    def get_banner(self, page):
        banner = banner_images = banner_style = None
        has_banner = False
        
        if page==None:
            banner = self.all()[0]
        else:
            banners = self.filter(page=page.id)
            if len(banners) >= 1:
                banner = banners[0]
            else:
                banner = None
                
        if banner != None:
            if banner.style == self.model.RANDOM:
                banner_images = banner.get_random_image()
            else:
                banner_images = banner.get_images()
    
            if len(banner_images) >= 1:
                has_banner = True

        return banner, banner_images, has_banner


class BannerImageManager(models.Manager):
    def get_banner_images(self, Banner):
        return self.filter(banner=Banner)

        