# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 20-03-2010.

from django.shortcuts import render_to_response
from django.template import RequestContext
from vcms.apps.simplenews import settings
from vcms.apps.simplenews.models import News


def news_index(request, category_slug, page=1):
    news = News.objects.all()[:settings.MAX_NEWS_PER_PAGE]
    return render_to_response("index.html", { "news": news }, context_instance=RequestContext(request))

def news_unique(request, category_slug, news_slug):
    context = {}
    context.update(InitPage(page=news_slug))
    context.update(locals())
    if context["module"] in globals():
        return render_to_response("", {}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/")

def news_category(request, category_slug, category, page=1):
    return render_to_response("", {}, context_instance=RequestContext(request))

def news_archives(request, category_slug, month, year, page=1):
    return render_to_response("", {}, context_instance=RequestContext(request))
