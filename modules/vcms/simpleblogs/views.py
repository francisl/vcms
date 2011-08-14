# -*- coding: utf-8 -*-
# Application: Vimba - CMS
# Module: SimpleBlogs
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francis Lavoie 20100913
import datetime
import inspect
import copy

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.conf import settings 

from vcms.www.views.html import _get_page_parameters
from vcms.simpleblogs.models import BlogPage, BlogPost, BlogPostCategory
from vcms.simpleblogs.models import APP_SLUGS
from hwm.tree import generator
from hwm.tree import helper 
from hwm.paginator import generator as pgenerator

if 'django_twitter' in settings.INSTALLED_APPS:
    from django_twitter.models import TwitterButtonWidgetConfig as TBW

class BlogPageController(object):
    def __init__(self, blog_page):
        self.page = blog_page

    def __call__(self, request):
        page_number = request.GET.get('page', 1)
        extrapath_len = len(request.cms_menu_extrapath)
        if extrapath_len > 0:
            first_param = request.cms_menu_extrapath[0]
            if first_param == 'archives':
                return self._call_page_for_archives(request, page_slug=self.page.slug, page_number=page_number)
            elif not first_param.isdigit():
                return page(request, page_slug=self.page.slug, page_number=page_number, category=first_param)
            elif len(first_param) == 4 and first_param.isdigit():
                return page_for_date(request, page_slug=self.page.slug, page_number=page_number)
        return page(request, page_slug=self.page.slug, page_number=page_number)

    def _call_page_for_archives(self, request, page_slug, page_number):
        return archives(request, page_slug, page_number=page_number)

    def is_requesting_archived(self, extrapath):
        if len(extrapath):
            return True if extrapath[0] == 'archives' else False
        return False

def archives_for_one_year(page, by_month_year, older_archive):
    archives = []
    delta = datetime.timedelta(days=31)
    today = datetime.date.today()
    query_date = lambda delta_time: today - (delta*delta_time)
    
    for i in range(12):
        current_date = query_date(i)
        archives.append({ 'date': current_date
                         ,'year': current_date.year
                         ,"month": current_date.month
                         ,'items_count': len(by_month_year(page, current_date.month, current_date.year))})

    older = { 'date': query_date(12), 'items_count': len(older_archive(page, query_date(12).month, query_date(12).year))}
    return archives, older

blogs_by_month_year = lambda page, month,year: BlogPost.published.get_for_page_by_date(page, year=year, month=month) 
blogs_older_archives_month_year = lambda page, month, year: BlogPost.published.get_archive_for_page(page, year=year, month=month)

def get_side_menu(page):
    categories = BlogPostCategory.objects.get_category_for_page(page, counts=True)
    archives, older_archives = archives_for_one_year(page, blogs_by_month_year, blogs_older_archives_month_year)
    return categories, archives, older_archives

def get_newsblog_page_or_404(page_slug):
    page = BlogPage.published.get_blog_page(page_slug)
    if not page :
        raise Http404
    return page
    

newsblogs_template = {'short_list': 'newsblogs_short_list.html'
                      ,'detailed_list': 'newsblogs_detailed_list.html' }
def page(request, page_slug=None, page_number=1, category=None, year=None, month=None, day=None, post_id=None):
    page = get_newsblog_page_or_404(page_slug)
    categories, archives, older_archives = get_side_menu(page)
    twitter_widget = None
    if TBW:
        twitter_widget = TBW.objects.get_widget_for_application('simpleblogs', page_slug)
    if category != None:
        category = get_object_or_404(BlogPostCategory, slug=category)

    blogs = BlogPost.published.get_all_for_page(page, category=category)
    
    page_paginator = pgenerator.get_page_paginator_from_list(blogs, page_number)
    html_navigation = pgenerator.get_navigation_from_paginator(page_paginator)
    
    return render_to_response( newsblogs_template[page.listing_style]
                               ,{ 'page': page
                                  ,'page_name': page_slug
                                  ,'posts': page_paginator.object_list
                                  ,'categories': categories
                                  ,'archives': archives
                                  ,'older_archives': older_archives
                                  ,'page_paginator': html_navigation
                                  ,'inside_navigation': True if settings.SITE_NAME == 'Classic' else False
                                  ,'twitter_widget' : twitter_widget
                                }
                                ,context_instance=RequestContext(request))

def page_for_date(request, page_slug=None, category=None, page_number=1, year=None, month=1, day=1, post_id=None):
    extrapath_len = len(request.cms_menu_extrapath)
    if extrapath_len > 43:
        raise Http404
    req_year = year
    if extrapath_len > 0:
        req_year = request.cms_menu_extrapath[0]
        year = req_year if type(int(req_year)) == type(0) else 2009
    month = 1
    if extrapath_len > 1:
        req_month = int(request.cms_menu_extrapath[1])
        month = req_month if (type(req_month) == type(0) and req_month < 13)  else 1

    day = day
    if extrapath_len > 2:
        req_day = int(request.cms_menu_extrapath[2])
        day = req_day if (type(req_day) == type(0) and req_day < 31)  else 1

    if extrapath_len > 3:
        req_post = int(request.cms_menu_extrapath[3])
        post_id = req_post if (type(req_post) == type(0))  else post_id
    
    page = get_newsblog_page_or_404(page_slug)
    categories, archives, older_archives = get_side_menu(page)

    blogs = BlogPost.published.get_for_page_by_date(page, category=category, year=year, month=month, day=day, post_id=post_id)

    page_paginator = pgenerator.get_page_paginator_from_list(blogs, page_number, item_per_page=page.number_of_post_per_page)
    html_navigation = pgenerator.get_navigation_from_paginator(page_paginator)

    if post_id != None:
        return post_page(request, page, post_id, page_paginator, html_navigation, categories, archives, older_archives)
    
    return render_to_response(newsblogs_template[page.listing_style]
                                ,{ 'page': page
                                  ,'page_name': page_slug
                                  ,'posts': page_paginator.object_list
                                  ,'categories': categories
                                  ,'archives': archives
                                  ,'older_archives': older_archives
                                  ,'page_paginator': html_navigation
                                  ,'inside_navigation': True if settings.SITE_NAME == 'Classic' else False
                                }
                                ,context_instance=RequestContext(request))

def archives(request, page_slug=None, year=2009, category=None, page_number=1):
    extrapath_len = len(request.cms_menu_extrapath)
    if extrapath_len > 3:
        raise Http404
    req_year = year
    if extrapath_len > 1:
        req_year = request.cms_menu_extrapath[1]
        year = int(req_year) if type(int(req_year)) == type(0) else 2009

    page = get_newsblog_page_or_404(page_slug)
    categories, archives, older_archives = get_side_menu(page)
    blogs = BlogPost.published.get_archive_for_page(page, category=category, year=year)

    page_paginator = pgenerator.get_page_paginator_from_list(blogs, page_number, item_per_page=page.number_of_post_per_page) 
    html_navigation = pgenerator.get_navigation_from_paginator(page_paginator)
    
    return render_to_response(newsblogs_template[page.listing_style]
                                ,{ 'page': page
                                  ,'page_name': page_slug
                                  ,'posts': page_paginator.object_list
                                  ,'categories': categories
                                  ,'archives': archives
                                  ,'older_archives': older_archives
                                  ,'page_paginator': html_navigation
                                  ,'inside_navigation': True if settings.SITE_NAME == 'Classic' else False
                                }
                                ,context_instance=RequestContext(request))

def post(request, page_slug=None, category=None, page_number=1, year=None, month=1, day=1, post_id=None):
    page = get_newsblog_page_or_404(page_slug)
    categories, archives, older_archives = get_side_menu(page)
    blogs = BlogPost.published.get_for_page_by_date(page, year=year, month=month, day=day, post_id=post_id)
    page_paginator = pgenerator.get_page_paginator_from_list(blogs, page_number, item_per_page=page.number_of_post_per_page)
    html_navigation = pgenerator.get_navigation_from_paginator(page_paginator)
    return post_page(request, page, post_id, page_paginator, html_navigation,categories, archives, older_archives)

def post_page(request, page, post_id, page_paginator, html_navigation, categories, archives, older_archives):
    return render_to_response(newsblogs_template['detailed_list']
                                ,{ 'page': page
                                  ,'page_name': page.slug
                                  ,'posts': page_paginator.object_list
                                  ,'categories': categories
                                  ,'archives': archives
                                  ,'older_archives': older_archives
                                  ,'page_paginator': html_navigation
                                  ,'inside_navigation': True if settings.SITE_NAME == 'Classic' else False
                                }
                                ,context_instance=RequestContext(request))
    
