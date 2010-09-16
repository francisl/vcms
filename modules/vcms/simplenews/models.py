# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 20-03-2010.

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from tagging.fields import TagField
from vcms.www.models import PageElementPosition
from vcms.simpleannouncements.models import AnnouncementPage, AnnouncementPost
from vcms.simplenews.managers import NewsManager, NewsCategoryManager


APP_SLUGS = "news"

#class NewsCategory(AnnouncementCategory):
#    objects = NewsCategoryManager()
#    published = PublishedAnnouncementCategoryManager()
#
#    def save(self):
#        self.app_slug = APP_SLUGS
#        self.module = 'SimpleNews'
#        super(NewsCategory, self).save()
#
#    class Meta:
#        verbose_name_plural = _("News categories")


class NewsPage(AnnouncementPage):
    #category = models.ForeignKey(NewsCategory)

    #objects = NewsManager()
    #published = PublishedAnnouncementManager()

    def get_absolute_url(self):
        return reverse("vcms.simplenews.views.single_news", args=[self.slug, self.category.slug])

    class Meta:
        verbose_name_plural = _("News")
        get_latest_by = ['-date_created']
        ordering = ['-date_created']


#
#class NewsPageModule(PageElementPosition):
#    from vcms.www.models.page import DashboardPage as DP
#    page = models.ForeignKey(DP)
#    tags = TagField()
#    title = models.CharField(max_length="60", help_text=_("Max 60 characters"), verbose_name=_("Title"))
#
#    def __unicode__(self):
#        return self.page.name
