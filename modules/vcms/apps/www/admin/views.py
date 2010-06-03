from django.shortcuts import get_object_or_404
from django.contrib import admin
from django.http import HttpResponse, Http404
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.translation import ugettext as _, ugettext_lazy
from django.core import serializers
from django.utils import simplejson as json
from django.shortcuts import render_to_response
from django.template import RequestContext 

from vcms.apps.www.models.page import Page

@staff_member_required
def UpdateMenu(request):
    """ Switch the status of a page
    """
    if request.method == 'POST':
        postlist = request.raw_post_data
        json_pages = json.JSONDecoder().decode(postlist)
        #for page in json_pages:
        #    print("%s\t\t\t%s" % (page, json_pages[page]))
            
        has_change = False
        for page in json_pages:
            db_page = Page.objects.get(id=json_pages[page]["Id"])
            #print("DB PAGE = %s" % db_page)
            if db_page.level != json_pages[page]["Level"]:
                db_page.level = json_pages[page]["Level"]
                has_change = True
                
            if json_pages[page]["Parent"]:
                if db_page.parent != json_pages[page]["Parent"]:
                    db_page.parent = Page.objects.get(id=json_pages[page]["Parent"])
                    has_change = True
            else:
                if db_page.parent != None:
                    db_page.parent = None
                    has_change = True
                
            if db_page.tree_position != json_pages[page]["Position"]:
                db_page.tree_position = json_pages[page]["Position"]
                has_change = True
            
            if db_page.display != json_pages[page]["Display"]:
                db_page.display = json_pages[page]["Display"]
                has_change = True
            #page.default = False
            #print("%s has change : %s" % (db_page, has_change))
            if has_change:
                db_page.save()
            
            has_change = False
            
        response = HttpResponse("{returnvalue:0}")
            
    else:
        reponse = HttpResponse("{returnvalue:2}")
    
    return response

"""
@staff_member_required
def UpdateMenu2(request):
    "" Switch the status of a page
    ""
    if request.method == 'POST':
        menulist = request.POST.lists()
        #print("RESQUESTED MENULIST = %s" % menulist)
        # reset page menu's information
        pages = Page.objects.all()
        for page in pages:
            page.level = 0
            page.parent = None
            page.tree_position = 0
            page.display = False
            #page.default = False
            page.save()

        def save_menu(menulist,  mparent=None):
            #print("adding menuist = %s" % menulist)
            m=1
            for item in menulist:
                #last_menu = None #keep track of preview menu for ordering
                #try:
                page = Page.objects.get(id=item) # get linked page
                if mparent:
                    page.level =  mparent.level+1
                    page.parent = mparent
                #else:
                #    if m==1:
                #        page.default=True
                page.display = True
                page.tree_position = m
                page.save()
                m += 1

        # do 1menu first
        # prevent children not being correctly saved
        for menu in menulist:
            if menu[0] == "1menu" :
                save_menu(menu[1])

        # then add children
        for menu in menulist:
            if menu[0].split('_')[0] == "submenu":
                try:
                    parentq = Page.objects.get(id=menu[0].split('_')[1])
                    save_menu(menu[1], mparent=parentq)
                except:
                    pass

    #return serializers.serialize('xml', Menu.objects.all())
    raise Http404
"""

@staff_member_required
def show_style(request):
    return render_to_response('style.html', {}, context_instance=RequestContext(request))
    
    