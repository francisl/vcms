# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleBlogs
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francis Lavoie 20100913
import datetime
import inspect

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


def generate_paginator(page_number, items, reverse_url, item_per_page=6, reverse_kwargs={}):
    import copy
    reverse = copy.copy(reverse_kwargs)
    for key in reverse:
        if reverse_kwargs[key] == None:
            del reverse_kwargs[key]

    paginator = Paginator(items, item_per_page)
    if int(page_number) > int(paginator.num_pages):
        page_number = paginator.num_pages
    html_paginator = pgenerator.get_page_navigation(paginator, page_number, reverse_url, reverse_kwargs=reverse_kwargs)
    page_paginator = paginator.page(page_number)

    if page_paginator.start_index() == 0:
        start_index = page_paginator.start_index()
    else:
        start_index = page_paginator.start_index()-1
        
    end_index = page_paginator.end_index()
    page_items = items[start_index:end_index]

    return page_items, page_paginator, html_paginator

def get_side_menu(page):
    categories = BlogPostCategory.objects.get_category_for_page(page, counts=True)
    archives, older_archives = archives_for_one_year(page, blogs_by_month_year, blogs_older_archives_month_year)
    return categories, archives, older_archives

def get_page_information(page_slug, method_name):
    page = BlogPage.published.get_blog_page(page_slug)
    #page = get_object_or_404(BlogPage, slug=page_slug)
    if not page :
        raise Http404
    page_info = _get_page_parameters(page)
    reverse_url="vcms.simpleblogs.views." + method_name
    return page, page_info ,reverse_url
    

def page(request, page_slug=None, category=None, page_number=1, year=None, month=None, day=None, post_id=None):
    page, page_info ,reverse_url = get_page_information(page_slug, 'page')
    categories, archives, older_archives = get_side_menu(page)
    
    if category != None:
        category = get_object_or_404(BlogPostCategory, slug=category)

    blogs = BlogPost.published.get_all_for_page(page, category=category)
    pitems, ppage, page_paginator = generate_paginator(page_number, blogs, reverse_url, page.number_of_post_per_page, {'page_slug':page_slug, 'category': category})
    
    return render_to_response("announcement.html"
                                ,{ 'page': page
                                  ,'page_name': page_slug
                                  ,'posts': pitems
                                  ,'categories': categories
                                  ,'archives': archives
                                  ,'older_archives': older_archives
                                  ,'page_paginator': page_paginator
                                  ,'page_info': page_info
                                  ,'inside_navigation': True if settings.SITE_NAME == 'Classic' else False
                                }
                                ,context_instance=RequestContext(request))

def page_for_date(request, page_slug=None, category=None, page_number=1, year=None, month=1, day=1, post_id=None):
    page, page_info ,reverse_url = get_page_information(page_slug, 'page_for_date')
    categories, archives, older_archives = get_side_menu(page)
    
    if post_id == None:
        blogs = BlogPost.published.get_for_page_by_date(page, category=category, year=year, month=month, day=day)
    else:
        blogs = BlogPost.published.get_for_page_by_date(page, category=category, year=year, month=month, day=day, post_id=post_id)
    
    pitems, ppage, page_paginator = generate_paginator(page_number, blogs, reverse_url, page.number_of_post_per_page, {'page_slug':page_slug, 'year':year, 'month':month})
    return render_to_response("announcement.html"
                                ,{ 'page': page
                                  ,'page_name': page_slug
                                  ,'posts': pitems
                                  ,'categories': categories
                                  ,'archives': archives
                                  ,'older_archives': older_archives
                                  ,'page_paginator': page_paginator
                                  ,'page_info': page_info
                                  ,'inside_navigation': True if settings.SITE_NAME == 'Classic' else False
                                }
                                ,context_instance=RequestContext(request))
    