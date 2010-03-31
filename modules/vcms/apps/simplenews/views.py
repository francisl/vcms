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


def news_index(request, category_slug, page=1):
    categories = NewsCategory.objects.all()
    if category_slug:
        news = News.objects.filter(category__slug=category_slug)
    else:
        news = News.objects.all()
    # Paginate the results
    paginator = Paginator(news, settings.MAX_NEWS_PER_PAGE)
    try:
        news_paginator = paginator.page(page)
    except (EmptyPage, InvalidPage):
        news_paginator = paginator.page(paginator.num_pages)
    contents = news_paginator.object_list
    # _TODO: Make the following generic
    if category_slug:
        paginator_previous_url = reverse("vcms.apps.simplenews.views.news_index", kwargs={ "category_slug": category_slug, "page": news_paginator.previous_page_number() })
        paginator_next_url = reverse("vcms.apps.simplenews.views.news_index", kwargs={ "category_slug": category_slug, "page": news_paginator.next_page_number() })
    else: # Remove category_slug from the dict, otherwise "None" will be used at the category
        paginator_previous_url = reverse("vcms.apps.simplenews.views.news_index", kwargs={ "page": news_paginator.previous_page_number() })
        paginator_next_url = reverse("vcms.apps.simplenews.views.news_index", kwargs={ "page": news_paginator.next_page_number() })
    return render_to_response("index.html", { "categories": categories, "contents": contents, "paginator": news_paginator, "paginator_previous_url": paginator_previous_url, "paginator_next_url": paginator_next_url }, context_instance=RequestContext(request))

def news_unique(request, category_slug, news_slug):
    context = {}
    context.update(InitPage(page_slug=news_slug, app_slug=APP_SLUGS))
    context.update(locals())
    if context["module"] in globals():
        return render_to_response("", {}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/")

def news_category(request, category_slug, category, page=1):
    return render_to_response("", {}, context_instance=RequestContext(request))

def news_archives(request, category_slug, month, year, page=1):
    return render_to_response("", {}, context_instance=RequestContext(request))
