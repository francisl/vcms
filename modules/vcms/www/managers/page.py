# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: www
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 30-05-2010.

from django.db import models
from vcms.www.fields import StatusField

class BasicPageManager(models.Manager):
    """
    def get_Default(self):
        try:
            defaultpage = self.filter(default=True)[0]
        except:
            defaultpage = self.all()[0]
        return defaultpage

    def reset_Default(self):
        defaultpage = self.filter(default=True)
        for page in defaultpage:
            page.default = False
            page.save()

    def reset_Default2(self):
        try:
            defaultpage = self.filter(status=StatusField.PUBLISHED)[0]
            defaultpage.default = True
        except:
            pass

    def get_RootMenu(self):
        menu = self.filter(level=0).filter(status=StatusField.PUBLISHED).filter(display=True)
        return menu

    def get_RootSelectedMenu(self, current_page):
        def up1level(page):
            if page.level != 0:
                return up1level(page.parent)
            else:
                return page

        if current_page:
            return up1level(current_page)
        else:
            return None

    def get_SubMenu(self, current_page):
        try:
            #print("currentpage = %s" % current_page)
            root = self.get_RootSelectedMenu(current_page)
            children = self.get_PageChildren(root)
        except:
            children = None

        try:
            selected = children.get(id=current_page.id)
            #print("selected submenu = %s" % selected)
        except:
            selected = None

        #print("SubMenu returning : %s, %s" % (children, selected))
        return children, selected

    def get_NotDisplay(self, lang='en'):
        return self.filter(status=StatusField.PUBLISHED).filter(display=False).filter(language='en')

    def get_PageFirstChild(self, current_page, lang='en'):
        try:
            #print("asdfasdfa = %s" % self.get_SubMenu(current_page)[0])
            return self.get_SubMenu(current_page)[0]
        except:
            #print("NO FCP!!!!!!!")
            return None
    """
    def get_children(self, parent=None):
        if parent:
            return self.filter(parent=parent).filter(status=StatusField.PUBLISHED).filter(display=True)
        else:
            return None


    def get_all_basic(self):
        from vcms.www.models.page import Language
        return self.filter(language=Language.objects.get_default())

    def get_main_published(self):
        return self.filter(status=StatusField.PUBLISHED).filter(level=0)

    def get_published(self):
        return self.filter(status=StatusField.PUBLISHED)


    def drafts(self):
        return self.filter(status=StatusField.DRAFT)

    def get_containers(self):
        raise NotImplementedError


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


class LanguageManager(models.Manager):
    def get_default(self):
        from settings import LANGUAGE_CODE
        return self.get(language_code=LANGUAGE_CODE[:2])


class QuickLinksManager(models.Manager):
    def get_quicklinks(self):
        return self.all()
