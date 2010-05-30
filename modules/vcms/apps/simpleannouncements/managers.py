# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 21-04-2010.

from django.db import models
from vcms.apps.www.fields import StatusField


class PublishedAnnouncementManager(models.Manager):
    def get_query_set(self):
        """Filters the results to display the published announcements."""
        from vcms.apps.www.models.page import Page
        return super(PublishedAnnouncementManager, self).get_query_set().filter(status=StatusField.PUBLISHED)

    def get_latest(self):
        """
            Returns the latest Announcement instances.
        """
        return self.order_by("-date_published")


class PublishedAnnouncementCategoryManager(models.Manager):
    def get_query_set(self):
        """Filters the results to display the published category announcements."""
        from vcms.apps.www.models.page import Page
        return super(PublishedAnnouncementCategoryManager, self).get_query_set().filter(status=StatusField.PUBLISHED)

    def get_latest(self):
        """
            Returns the latest AnnouncementCategory instances.
        """
        return self.order_by("-date_published")
