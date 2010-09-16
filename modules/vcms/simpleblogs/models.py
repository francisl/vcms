# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 20-03-2010.

from django.db import models
from django.utils.translation import ugettext_lazy as _
from tagging.fields import TagField
#from vcms.www.models.page import PageElementPosition
from vcms.simpleannouncements.models import AnnouncementPage, AnnouncementPost, AnnouncementPostCategory
from vcms.simpleblogs.managers import BlogPageManager, PublishedBlogPostManager, BlogPostCategoryManager
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
    objects = BlogPostCategoryManager()
    class Meta:
        ordering = ['name']
        verbose_name_plural = _("Blog Posts Categories")
        
class BlogPost(AnnouncementPost):
    display_on_page = models.ForeignKey(BlogPage)
    category = models.ManyToManyField(BlogPostCategory)
    published = PublishedBlogPostManager()
    
    class Meta:
        verbose_name_plural = _("Blog Posts")
        get_latest_by = ['-date_created']
        ordering = ['-date_created']

    def __unicode__(self):
        return self.title

"""
class BlogPageModule(PageElementPosition):
    from vcms.www.models.page import DashboardPage as DP
    page = models.ForeignKey(DP)
    tags = TagField()
    title = models.CharField(max_length="60", help_text=_("Max 60 characters"), verbose_name=_("Title"))
"""
   