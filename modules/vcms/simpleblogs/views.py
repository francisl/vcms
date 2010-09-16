# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleBlogs
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francis Lavoie 20100913

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from vcms.simpleblogs.models import BlogPage, BlogPost, BlogPostCategory
from vcms.simpleblogs.models import APP_SLUGS
from hwm.tree import generator
from hwm.tree import helper 
from hwm.paginator import generator as pgenerator


def blog_page(request, blog_page=None, category=None):
    page = BlogPage.objects.get_blog_page_from_string(blog_page)
    if page:
        blogs = BlogPost.published.get_all_for_page(page, category=category)
        return render_to_response("announcement.html"
                                    ,{ 'page_name': blog_page
                                        ,'posts': blogs
                                        ,'categories': BlogPostCategory.objects.get_non_empty_categories_for_page(page, counts=True)
                                        ,'model': BlogPost
                                        }
                                    ,context_instance=RequestContext(request))


def blog_page_for_date(request):
    pass