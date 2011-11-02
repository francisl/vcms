# -*- coding: utf-8 -*-

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response
from django.template import RequestContext 


@staff_member_required
def show_style(request):
    return render_to_response('style.html'
                              ,{}
                              ,context_instance=RequestContext(request))
    
    
