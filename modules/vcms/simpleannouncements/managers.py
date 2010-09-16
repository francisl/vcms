# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 21-04-2010.

from django.db import models
from vcms.www.fields import StatusField
from vcms.www.models.page import STATUS_DRAFT, STATUS_PUBLISHED, STATUSES

class PublishedAnnouncementPostManager(models.Manager):
    def get_query_set(self):
        """Filters the results to display the published announcements."""
        return self.filter(status=STATUSES[STATUS_PUBLISHED])

    def get_latest(self):
        """
            Returns the latest Announcement instances.
        """
        return self.order_by("-date_published")
