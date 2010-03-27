# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 20-03-2010.

from django.db import models
from django.utils.translation import ugettext_lazy as _
from tagging.fields import TagField
from vcms.apps.www.models import Language, Page, PageElementPosition
from vcms.apps.simpleannouncements.models import Announcement


APP_SLUGS = "simplenews"


class News(Announcement):
    class Meta:
        verbose_name_plural = _("News")
        get_latest_by = ['-date_created']
        ordering = ['-date_created']


class NewsPageModule(PageElementPosition):
    from vcms.apps.www.models import DashboardPage as DP
    page = models.ForeignKey(DP)
    tags = TagField()
    title = models.CharField(max_length="60", help_text=_("Max 60 characters"), verbose_name=_("Title"))

    def __unicode__(self):
        return self.page.name
