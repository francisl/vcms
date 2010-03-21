# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: SimpleNews
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 20-03-2010.

from django.shortcuts import render_to_response
from django.template import RequestContext


def news_index(request, page=1):
    return render_to_response("", {}, context_instance=RequestContext(request))

def news_unique(request, news_id=1):
    return render_to_response("", {}, context_instance=RequestContext(request))

def news_category(request, category, page=1):
    return render_to_response("", {}, context_instance=RequestContext(request))

def news_archives(request, month, year, page=1):
    return render_to_response("", {}, context_instance=RequestContext(request))
