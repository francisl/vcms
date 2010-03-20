# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 20-03-2010.

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from tagging.fields import TagField
from vcms.apps.www.models import Language, PageElementPosition


class Article(models.Model):
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    STATUS_CHOICES = ((LIVE_STATUS, _('Live')), (DRAFT_STATUS, _('Draft')), (HIDDEN_STATUS, _('Hidden')))
    date = models.DateTimeField(auto_now=True, editable=True)
    name = models.CharField(max_length="40", help_text=_("Max 40 characters"), verbose_name=_("Title"))
    excerpt = models.TextField(verbose_name=_("Preview"))
    content = models.TextField()
    language = models.ForeignKey(Language)
    tags = TagField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS, help_text=_("Only Entries with the 'live' status will be publicly displayed."))

    def __unicode__(self):
        return self.name


class News(Article):
    class Meta:
        verbose_name_plural = _("News")
        get_latest_by = ['-date']
        ordering = ['-date']


class NewsPageModule(PageElementPosition):
    from vcms.apps.www.models import DashboardPage as DP
    page = models.ForeignKey(DP)
    tags = TagField()
    title = models.CharField(max_length="60", help_text=_("Max 60 characters"), verbose_name=_("Title"))

    def __unicode__(self):
        return self.page.name
