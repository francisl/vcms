# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleBlogs
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francis Lavoie

from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from vcms.simpleannouncements.managers import PublishedAnnouncementPostManager
from vcms.www.fields import StatusField

class BlogPageManager(models.Manager):
    def get_blog_page_from_string(self, page_name):
        page = self.get(slug=page_name)
        if page :
            return page
        raise ObjectDoesNotExist
    
class PublishedBlogPageManager(models.Manager):
    def get_blog_page(self, page_name):
        page = self.get(slug=page_name)
        if page and page.status ==  StatusField.PUBLISHED :
            return page
        return None



class PublishedBlogPostManager(PublishedAnnouncementPostManager):
    pass

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
        