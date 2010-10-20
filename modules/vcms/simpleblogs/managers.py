# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleBlogs
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francis Lavoie

from django.db import models
from vcms.simpleannouncements.managers import PublishedAnnouncementPostManager

class BlogPageManager(models.Manager):
    def get_blog_page_from_string(self, page_name):
        return self.get(slug=page_name)


class PublishedBlogPostManager(models.Manager):
    def get_count_in_category(self, category):
        return len(self.filter(category__in=category))
        
    def get_all_for_page(self, page, category=None):
        """ Returns the latest Announcement instances.
        """
        if category:
            return self.filter(display_on_page=page).filter(category__slug__contains=category).order_by("-date_published")
        return self.filter(display_on_page=page).order_by("-date_published")

class BlogPostCategoryManager(models.Manager):
    
    def get_count_in_category(self, category):
        return len(self.get(slug=category.slug).blogpost_set.all())

    def get_non_empty_categories_for_page(self, page, counts=False):
        categories_len= {}
        if counts:
            for category in self.all():
                categories_len[category.name] = {'model': category
                                            ,'count' : self.get_count_in_category(category)
                                            }
        else:
            categories_len[category.name] = {'model': category }
        
        return categories_len
        