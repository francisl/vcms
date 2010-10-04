# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 21-04-2010.

from datetime import date

from django.db import models

from vcms.www.fields import StatusField
from vcms.www.models.page import STATUS_DRAFT, STATUS_PUBLISHED, STATUSES


class PublishedAnnouncementPostManager(models.Manager):
    def get_latest(self):
        """ Returns the latest Announcement instances.
        """
        return self.order_by("-date_published")

    def get_for_page_by_date(self, page, category=None, year=None, month=1, day=1, post_id=None):
        if post_id:
            return self.filter(date_published__year=int(year)).filter(date_published__month=int(month)).filter(id=post_id)
        return self.filter(date_published__year=int(year)).filter(date_published__month=int(month))
        
    def get_all_for_page(self, page, category=None):
        """ Returns the latest Announcement instances.
        """
        if category:
            return self.filter(display_on_page=page).filter(category__slug__contains=category).order_by("-date_published")
        return self.filter(display_on_page=page).order_by("-date_published")
        
    def get_latest_post_for_page(self, page, qty=1, category=None):
        if category:
            return self.filter(display_on_page=page).filter(category__slug__contains=category.slug).order_by("-date_published")[:qty]
        return self.filter(display_on_page=page).order_by("-date_published")[:qty]
