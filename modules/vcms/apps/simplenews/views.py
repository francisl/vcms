# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 20-03-2010.

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from vcms.apps.simplenews import settings
from vcms.apps.simplenews.models import News, NewsCategory
from vcms.apps.simplenews.models import APP_SLUGS
from vcms.apps.www.views import InitPage


def list_news(request, category_slug, page=1, context={}):
    from vcms.apps.vwm.tree import generator
    from vcms.apps.vwm.tree import helper 

    context.update(InitPage(page_slug=category_slug, app_slug=APP_SLUGS))
    context.update(locals())
    categories = NewsCategory.objects.get_categories_in_use()
    nav = []
    for navgroup in categories:
        nav.append(helper.create_tree_node(navgroup.name, url=navgroup.get_absolute_url()))
        
    navigation_menu = generator.generate_tree(nav)
    print("navigation_menu %s " % navigation_menu)
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
    # _TODO: Make the following generic
    if category_slug:
        paginator_previous_url = reverse("vcms.apps.simplenews.views.list_news", kwargs={ "category_slug": category_slug, "page": news_paginator.previous_page_number() })
        paginator_next_url = reverse("vcms.apps.simplenews.views.list_news", kwargs={ "category_slug": category_slug, "page": news_paginator.next_page_number() })
    else: # Remove category_slug from the dict, otherwise "None" will be used at the category
        paginator_previous_url = reverse("vcms.apps.simplenews.views.list_news", kwargs={ "page": news_paginator.previous_page_number() })
        paginator_next_url = reverse("vcms.apps.simplenews.views.list_news", kwargs={ "page": news_paginator.next_page_number() })
    context.update({ "categories": categories, "contents": contents, "paginator": news_paginator, "paginator_previous_url": paginator_previous_url, "paginator_next_url": paginator_next_url })
    return render_to_response("list_news.html", {"navigation_menu": navigation_menu, 
                                                 "contents": contents, 
                                                 "paginator": news_paginator, 
                                                 "paginator_previous_url": paginator_previous_url, 
                                                 "paginator_next_url": paginator_next_url,
                                                 "current_page": context['current_page'],
                                                 "menu_style": context['menu_style'],
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

def news_archives(request, category_slug, month, year, page=1, context={}):
    context.update(InitPage(page_slug=category_slug, app_slug=APP_SLUGS))
    context.update(locals())
    context.update({ "categories": categories, "contents": contents, "paginator": news_paginator, "paginator_previous_url": paginator_previous_url, "paginator_next_url": paginator_next_url })
    return render_to_response("", context, context_instance=RequestContext(request))
