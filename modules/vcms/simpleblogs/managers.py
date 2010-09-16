# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleBlogs
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francis Lavoie

from django.db import models
from vcms.www.models.page import STATUS_DRAFT, STATUS_PUBLISHED, STATUSES


class BlogPageManager(models.Manager):
    def get_blog_page_from_string(self, page_name):
        return self.get(slug=page_name)

class PublishedBlogPostManager(models.Manager):
    def get_all_for_page(self, page, category=None):
        """ Returns the latest Announcement instances.
        """
        if category:
            return self.filter(display_on_page=page).filter(category__slug__contains=category).order_by("-date_published")
        return self.filter(display_on_page=page).order_by("-date_published")

class BlogPostCategoryManager(models.Manager):
    def get_non_empty_categories_for_page(self, page, counts=False):
        from vcms.simpleblogs.models import BlogPage, BlogPost
        blogposts = BlogPost.published.filter(display_on_page=page)
        if counts:
            categories = {}
            for post in blogposts:
                for category in post.category.all():
                    if categories.has_key(category.name):
                        categories[category.name]['count'] += 1
                        categories[category.name]['model'] = category
                    else:
                        categories[category.name] = {}
                        categories[category.name]['count']=1
                        categories[category.name]['model'] = category

        else:
            categories = [category.name for category in post.category.all() for post in blogposts]
        
        return categories
        