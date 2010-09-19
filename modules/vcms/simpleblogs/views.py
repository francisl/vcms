# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleBlogs
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francis Lavoie 20100913
import datetime
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from vcms.simpleblogs.models import BlogPage, BlogPost, BlogPostCategory
from vcms.simpleblogs.models import APP_SLUGS
from hwm.tree import generator
from hwm.tree import helper 
from hwm.paginator import generator as pgenerator

def archives_for_one_year(by_month_year, older_archive):
    archives = []
    delta = datetime.timedelta(days=31)
    today = datetime.date.today()
    query_date = lambda delta_time: today - (delta*delta_time)
    
    for i in range(12):
        current_date = query_date(i)
        archives.append({ 'date': current_date, 'year': current_date.year, "month": current_date.month, 'items_count': len(by_month_year(current_date.month, current_date.year))})

    older = { 'date': query_date(12), 'items_count': len(older_archive(query_date(12).month, query_date(12).year))}
    return archives, older
            
blogs_by_month_year = lambda month,year: BlogPost.published.filter(date_published__month=month, date_published__year=year) 
blogs_older_archives_month_year = lambda month, year: BlogPost.published.filter(date_published__lt=datetime.date(year, month, 1))

def generate_paginator(page_number, items, item_per_page=6, reverse_url="vcms.simpleblogs.views.blog_page", reverse_kwargs={}):
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
    categories = BlogPostCategory.objects.get_non_empty_categories_for_page(page, counts=True)
    archives, older_archives = archives_for_one_year(blogs_by_month_year, blogs_older_archives_month_year)
    return categories, archives, older_archives

def page(request, page=None, category=None, page_number=1, year=None, month=None, day=None, post_id=None):
    page_slug = page
    page = get_object_or_404(BlogPage, slug=page)
    if category:
        category = get_object_or_404(BlogPostCategory, slug=category)
    reverse_url="vcms.simpleblogs.views.page"
    if page:
        blogs = BlogPost.published.get_all_for_page(page, category=category.slug)
        categories, archives, older_archives = get_side_menu(page)
        pitems, ppage, page_paginator = generate_paginator(page_number, blogs, page.number_of_post_per_page, reverse_url, {'page':page_slug, 'category': category.slug})
        return render_to_response("announcement.html"
                                    ,{'page_name': page_slug
                                      ,'posts': pitems
                                      ,'categories': categories
                                      ,'archives': archives
                                      ,'older_archives': older_archives
                                      ,'page_paginator': page_paginator
                                      ,'model': BlogPost
                                    }
                                    ,context_instance=RequestContext(request))

def page_for_date(request, page=None, category=None, page_number=1, year=None, month=1, day=1, post_id=None):
    page_slug = page
    page = get_object_or_404(BlogPage, slug=page)
    reverse_url="vcms.simpleblogs.views.page_for_date"
    if page:
        blogs = BlogPost.published.get_for_page_by_date(page, category=category, year=year, month=month, day=day)
        categories, archives, older_archives = get_side_menu(page)
        pitems, ppage, page_paginator = generate_paginator(page_number, blogs, page.number_of_post_per_page, reverse_url, {'page':page_slug, 'year':year, 'month':month})
        return render_to_response("announcement.html"
                                    ,{'page_name': page_slug
                                      ,'posts': pitems
                                      ,'categories': categories
                                      ,'archives': archives
                                      ,'older_archives': older_archives
                                      ,'page_paginator': page_paginator

                                      ,'model': BlogPost
                                    }
                                    ,context_instance=RequestContext(request))
    
    
    