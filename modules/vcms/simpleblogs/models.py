# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 20-03-2010.

from django.db import models
from django.utils.translation import ugettext_lazy as _
from tagging.fields import TagField
from vcms.www.models import PageElementPosition
from vcms.simpleannouncements.models import AnnouncementPage, AnnouncementPost, AnnouncementPostCategory
from vcms.simpleblogs.managers import BlogPageManager, PublishedBlogPostManager
from tagging.models import Tag

APP_SLUGS = "blogs"

class BlogPage(AnnouncementPage):
    objects = BlogPageManager()

    class Meta:
        verbose_name = _("Page - Blog Page")
        verbose_name_plural = _("Page - Blog Pages")
        ordering = ['name']
        
    def save(self):
        self.app_slug = APP_SLUGS
        super(BlogPage, self).save()

class BlogPostCategory(AnnouncementPostCategory):
    class Meta:
        ordering = ['name']

class BlogPost(AnnouncementPost):
    display_on_page = models.ForeignKey(BlogPage)
    category = models.ManyToManyField(BlogPostCategory)
    published = PublishedBlogPostManager()
    
    class Meta:
        verbose_name_plural = _("Blog Posts")
        get_latest_by = ['-date_created']
        ordering = ['-date_created']
  
    @staticmethod
    def get_model_tags(counts=True):
        return Tag.objects.usage_for_model(BlogPost, counts=counts)

    def __unicode__(self):
        return self.title


class BlogPageModule(PageElementPosition):
    from vcms.www.models.page import DashboardPage as DP
    page = models.ForeignKey(DP)
    tags = TagField()
    title = models.CharField(max_length="60", help_text=_("Max 60 characters"), verbose_name=_("Title"))

   