# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie

from django.db import models
from django.contrib.sites.managers import CurrentSiteManager


class PageManager(models.Manager):
    def get_Default(self):
        defaultpage = self.filter(default=True)[0]
        #print("RETuRN DEFAULT = %s" % defaultpage)
        return defaultpage

    def reset_Default(self):
        defaultpage = self.filter(default=True)
        for page in defaultpage:
            page.default = False
            page.save()

    def reset_Default(self):
        try:
            defaultpage = self.filter(status=self.model.PUBLISHED)[0]
            defaultpage.default = True
        except:
            pass
                    
    def get_RootMenu(self):
        menu = self.filter(level=0).filter(status=self.model.PUBLISHED).filter(display=True)
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

    def get_AllBasic(self):
        return self.filter(status=self.model.PUBLISHED).filter(module__in=["Basic", 'Dashboard'])

    def get_MainPublished(self):
        return self.filter(status=self.model.PUBLISHED).filter(level=0)

    def get_Published(self):
        return self.filter(status=self.model.PUBLISHED)

    def get_NotDisplay(self, lang='en'):
        return self.filter(status=self.model.PUBLISHED).filter(display=False).filter(language='en')

    def get_PageFirstChild(self, current_page, lang='en'):
        try:
            #print("asdfasdfa = %s" % self.get_SubMenu(current_page)[0])
            return self.get_SubMenu(current_page)[0]
        except:
            #print("NO FCP!!!!!!!")
            return None

    def get_PageChildren(self, parent=None):
        if parent:
            return self.filter(parent=parent).filter(status=self.model.PUBLISHED).filter(display=True)
        else:
            return None

    def drafts(self):
        return self.filter(status=self.model.DRAFT)


class BannerManager(models.Manager):
    def random(self, banners=None):
        import random
        
        banner = has_banner = False # set no banners to default to reduce check exception        
        bannerqty = len(banners)
        try:    # only one banner
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
        
    def banner(self, page):
        banner = has_banner = False
        try:
            banners = self.filter(page=page.id)
            lbanners = len(banners)
            if lbanners >= 2:
                # if only one banner is set
                banner, has_banner = self.random(banners=banners)
                has_banner = True
            elif lbanners == 1:
                # otherwise select a random banners
                banner = banners[0]
                has_banner = True
        except:
            banner, has_banner = False

        return banner, has_banner


class DashboardElementManager(models.Manager):
    def get_PublishedAll(self):
        return self.filter(published=True)

    def get_Published(self, current_page):
        return self.filter(published=True).filter(page=current_page)

class LanguageManager(models.Manager):
    def getDefault(self):
        from settings import LANGUAGE_CODE
        return self.get(language_code=LANGUAGE_CODE[:2])
