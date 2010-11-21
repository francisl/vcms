# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleBlogs
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francis Lavoie

from datetime import date

from django.db import models
from django.core.exceptions import ObjectDoesNotExist

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

class BlogPostCategoryManager(models.Manager):
    def get_category_for_page(self, page, counts=True):
        from vcms.simpleblogs.models import BlogPost
        categories_for_page = {}
        for category in self.all():
            posts = BlogPost.objects.get_all_for_page(page, category=category)
            if posts:    
                categories_for_page[category.name] = {'model': category
                                            ,'count' : posts.count()
                                            }

        return categories_for_page

class PublishedNewsBlogPostManager(models.Manager):
    def get_published(self, queryset=None):
        query = self
        if queryset:
            query = queryset
        return query.filter(status=StatusField.PUBLISHED)
    
    def get_unpublished(self):
        return self.filter(status=StatusField.DRAFT)
    
    def get_category_for_page(self, page):
        query = self.get_for_page(page)
        return query
        
    def get_latest(self, queryset=None):
        query = self
        if queryset:
            query = queryset
        return query.get_published().order_by("-date_published")

    def get_for_page(self, page, queryset=None):
        query = self
        if queryset:
            query = queryset
        query = self.get_published(queryset=query)
        return query.filter(display_on_page=page)
    
    def get_for_page_by_date(self, page, category=None, year=None, month=1, day=1, post_id=None):
        query = self.get_latest()
        query = self.get_for_page(page, queryset=query).filter(date_published__year=int(year)).filter(date_published__month=int(month)) 
        if post_id:
            return query.filter(id=post_id)
        return query 
    
    def get_archive_for_page(self, page, category=None, year=None, month=1, day=1):
        query = self.get_published()
        query = self.get_for_page(page, queryset=query)
        return query.filter(date_published__lt=date(year, month, 1))
            
        
    def get_all_for_page(self, page, category=None):
        query = self.get_latest()
        query = self.get_for_page(page, queryset=query)
        if category:
            query = query.filter(category=category) 
        return query
        
    def get_latest_post_for_page(self, page, qty=1, category=None):
        if category:
            return self.get_latest().filter(display_on_page=page).filter(category__slug__contains=category.slug)[:qty]
        return self.get_latest().filter(display_on_page=page)[:qty]


