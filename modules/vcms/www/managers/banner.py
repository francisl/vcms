# -*- coding: utf-8 -*-
# Application: Vimba - CMS
# Module: www
# Copyright (c) 2010 Vimba inc. All rights reserved.

from django.db import models

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
            banners = self.all()
            if banners :
                banner = banners[0]
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
