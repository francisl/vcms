# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 20-03-2010.

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from vcms.apps.simplenews import settings
from vcms.apps.simplenews.models import News, NewsCategory
from vcms.apps.simplenews.models import APP_SLUGS
from vcms.apps.www.views import InitPage, setPageParameters
from vcms.apps.vwm.tree import generator as generator
from vcms.apps.vwm.tree import helper 
from vcms.apps.vwm.paginator import generator as pgenerator

def list_news(request, category_slug, page=1, context={}):
    context.update(InitPage(page_slug=category_slug, app_slug=APP_SLUGS))
    context.update(locals())
    categories = NewsCategory.objects.get_categories_in_use()
    
    nav = []
    # add category topics
    category_nav = helper.create_tree_node("Topics", selected=True) 
    category_items = []
    for navgroup in categories:
        category_items.append(helper.create_tree_node(navgroup.name, url=navgroup.get_absolute_url()))
        print("... %s" % navgroup.get_absolute_url())
    
    category_nav["items"] = category_items
    nav.append(category_nav)

    #get archives
    archive_years = [d.year for d in News.objects.dates('date_published', 'month')]
    archive_years.reverse()
    
    archive_nav = helper.create_tree_node("Archives", selected=True) 
    archive_items = []
    for year in archive_years:
        archive_items.append(helper.create_tree_node(year, url=reverse("vcms.apps.simplenews.views.news_archives" , kwargs={ "year":year })))
        print(".... %s " % reverse("vcms.apps.simplenews.views.news_archives" , kwargs={ "year":year }))
    
    archive_nav["items"] = archive_items
    nav.append(archive_nav)

    # generate navigation
    navigation_menu = generator.generate_tree(nav)

    if category_slug:
        news = News.published.filter(category__slug=category_slug)
    else:
        news = News.published.all()
    # Paginate the results
    paginator = Paginator(news, settings.MAX_NEWS_PER_PAGE)
    try:
        news_paginator = paginator.page(page)
    except (EmptyPage, InvalidPage):
        news_paginator = paginator.page(paginator.num_pages)
    contents = news_paginator.object_list

    reverse_url = "vcms.apps.simplenews.views.list_news"
    url_args = {}
    if category_slug: # add category if necessary
        url_args.update(category_slug = category_slug)
    
    paginator_html = pgenerator.get_page_navigation(news_paginator,
                                                    pgenerator.get_paginator_previous_url(news_paginator, reverse_url, kwargs=url_args), 
                                                    pgenerator.get_paginator_next_url(news_paginator, reverse_url, kwargs=url_args))
    
    return render_to_response("list_news.html", {"navigation_menu": navigation_menu, 
                                                 "contents": contents, 
                                                 "paginator_html": paginator_html, 
                                                 "page_info": setPageParameters()["page_info"],
                                                 },
                                                 
                               context_instance=RequestContext(request))

def single_news(request, category_slug, news_slug, context={}):
    context.update(InitPage(page_slug=category_slug, app_slug=APP_SLUGS))
    context.update(locals())
    categories = NewsCategory.objects.get_categories_in_use()
    #content = context["current_page"]
    content = News.published.get(category__slug=category_slug, slug=news_slug)
    try:
        previous_news = content.get_previous_announcement()
    except News.DoesNotExist:
        previous_news = None
    try:
        next_news = content.get_next_announcement()
    except News.DoesNotExist:
        next_news = None
    context.update({ "categories": categories, "content": content, "previous_news": previous_news, "next_news": next_news })
    return render_to_response("single_news.html", context, context_instance=RequestContext(request))

def news_category(request, category_slug, category, page=1, context={}):
    context.update(InitPage(page_slug=category_slug, app_slug=APP_SLUGS))
    context.update(locals())
    context.update({ "categories": categories, "contents": contents, "paginator": news_paginator, "paginator_previous_url": paginator_previous_url, "paginator_next_url": paginator_next_url })
    return render_to_response("", context, context_instance=RequestContext(request))

def news_archives(request, category_slug, year, month=0, page=1, context={}):
    context.update(InitPage(page_slug=category_slug, app_slug=APP_SLUGS))
    context.update(locals())
    context.update({ "categories": categories, "contents": contents, "paginator": news_paginator, "paginator_previous_url": paginator_previous_url, "paginator_next_url": paginator_next_url })
    return render_to_response("", context, context_instance=RequestContext(request))
