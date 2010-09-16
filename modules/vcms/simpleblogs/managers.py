# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleBlogs
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francis Lavoie

from django.db import models
from vcms.www.models.page import STATUS_DRAFT, STATUS_PUBLISHED, STATUSES

class BlogPageManager(models.Manager):
    def get_blog_page_from_string(self, page_name):
        return self.get(slug=page_name)

class PublishedBlogPostManager(models.Manager):
    def get_all_for_page(self, page):
        """
            Returns the latest Announcement instances.
        """
        return self.filter(display_on_page=page).order_by("-date_published")
