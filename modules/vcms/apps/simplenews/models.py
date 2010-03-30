# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 20-03-2010.

from django.db import models
from django.contrib.auth.models import Group, User
from django.utils.translation import ugettext_lazy as _
from tagging.fields import TagField
from vcms.apps.www.models import Language, PageElementPosition
from vcms.apps.simpleannouncements.models import Announcement
from vcms.apps.simplenews.managers import NewsManager


APP_SLUGS = "simplenews"


class NewsCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text=_('Max 40 characters.'))
    slug = models.SlugField(max_length=150, unique=True, help_text=_("Used for hyperlinks, no spaces or special characters."))
    description = models.CharField(max_length=250, help_text=_("Short description of the page (helps with search engine optimization.)"))
    authorized_users = models.ManyToManyField(User, related_name="news", blank=True, null=True)
    authorized_groups = models.ManyToManyField(Group, related_name="news", blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_modified = models.DateTimeField(auto_now=True, editable=False)

    # Parameters
    language = models.ForeignKey(Language)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = _("News categories")
        get_latest_by = ['-date_created']
        ordering = ['name']


class News(Announcement):
    category = models.ForeignKey(NewsCategory)

    objects = NewsManager()

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
