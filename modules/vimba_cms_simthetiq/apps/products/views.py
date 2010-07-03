# encoding: utf-8
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Template, Context, RequestContext 
from django import forms
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

import settings

from vimba_cms_simthetiq.apps.products import models as productmodels
from vcms.www.views import get_requested_page, _set_page_paramters
from hwm.paginator import generator as pgenerator


def Generic(request, page=None, product=None, selected_category=None, slug=None, context={}):
    """ Is called first, then it calls the right view base on module name containt in the url
    """
    context.update(get_requested_page(page_slug=page, app_slug=productmodels.APP_SLUGS))
    context.update(locals())
    
    if context["module"] in globals():
        return globals()[context["module"]](request, context)
    else:
        return HttpResponseRedirect("/")
    

def Product(request, context={}):
    #get the product page, need to link to the product
    productpage = productmodels.ProductPage.objects.get(id=context["current_page"].id)
    # get product
    #product = productmodels.Product.objects.get(id=productpage.product.id)
    try:
        # get product content list
        product_contents = productmodels.ProductContent.objects.filter(page=productpage.id)
    except:
        product_contents = None
    try:
        category = productmodels.Category.objects.get(id=productpage.category_id)
        #print("CATEGORY = %s" % category.domain.get_absolute_url())
    except:
        category = None
    
    # set navigation type if not set
    if request.session.get('navigation_type') == "":
        request.session['navigation_type'] = "standard"
        
    if request.session.get('navigation_type') == "DIS":
        menu = category.get_navigation_menu()
    elif request.session.get('navigation_type') == "standard":
        menu = StandardNavigationGroup.get_navigation()
    
    #print("PRODUCT INFORMATION %s " % product_information)
    return render_to_response('product_info.html',
                                { "menuselected":  "menu_products",
                                  "current_page":   context['current_page'],
                                  "productpage":    productpage,
                                  "category":       category,
                                  "product_contents": product_contents,
                                  "navigation_menu": menu },
                                context_instance=RequestContext(request))

def set_navigation_type(request, page=None, type="standard"):
    """ Set the naviation type into the user's session
    """
    request.session['navigation_type'] = type # standard or DIS
    return productHome(request, get_requested_page(page=page))
    

def get_navigation(request, navigation_type):
    """ Take a request and return the html navigation
    """
    from hwm.tree import generator
    if request.session.get('navigation_type') == "DIS" or navigation_type.upper() == "DIS":
        return category.get_navigation_menu()
    else: #if request.session.get('navigation_type') == "standard" :
        return generator.generate_tree(productmodels.StandardNavigationGroup.objects.get_navigation())

def productHome(request, context={}):
    from vcms.www.models import MenuLocalLink
    
    page = MenuLocalLink.objects.get(local_link="/products/home")
    context.update(_set_page_paramters(page))
    context.update(locals())
    
    # set navigation type if not set
    if request.session.get('navigation_type') == "":
        request.session['navigation_type'] = "standard"
        
    nav = get_navigation(request)

    return render_to_response('product_home.html',
                                { "menuselected":  "menu_products",
                                  "menu_style" : context['menu_style'],
                                  "current_page":   page,
                                  "navigation_menu": nav },
                                context_instance=RequestContext(request))

def getProductPaginator(products, page_num=1, item_per_page=10):
    """ getProductPaginator is a wrapper that take a model list
        to return full paginator functionnality
        @return : dict{} with paginator information
                    page_num : current paginator page
                    items : current paginator items list
                    page_total : total paginator page 
    """
    #print("products = %s" % products)
    page_num = int(page_num)
    paginator = Paginator(products, item_per_page)
    if type(page_num) != type(0):
        page_num = 1
    
    try: # make sure the page number is not off
        return paginator.page(page_num)
    except:
        return paginator.page(paginator.num_pages)
        

_DISPLAY_TYPE = { 0: 'list'
                 ,1: 'detailed_list'
                 ,2: 'grid'
                 }

def get_display_type_url(nav_type, nav_selection, display_type, full=False):
    reverse_url = reverse(str("vimba_cms_simthetiq.apps.products.views.product_" + _DISPLAY_TYPE[display_type]), 
                    kwargs={"nav_type":nav_type
                            , "nav_selection":nav_selection
                            })
    if full == True:
        reverse_url = "http://" + str(Site.objects.get(id__exact=settings.SITE_ID)) + reverse_url
        
    return reverse_url

def get_avail_products_for_page(page_number, item_per_page=20):
    return getProductPaginator(productmodels.ProductPage.objects.get_available_products(), 
                                   page_num=page_number,
                                   item_per_page=item_per_page)

def get_products_top_button_list(nav_type):
    from hwm.button import generator as button
    buttons_list = []
    buttons_list.append(button.create_button('My Account', '/accounts/register', 'text'))
    buttons_list.append(button.create_button('Cart', '', 'text'))
    if nav_type == 'standard':
        buttons_list.append(button.create_button('Standard Database', '', 'text'))
    else:
        buttons_list.append(button.create_button('<b>DIS</b> Database</a>', '', 'text'))
    buttons_list.append(button.create_button('Email Page', 'mailto:?subject={{emailto.subject}}&body={% trans "I think you should check that link : " %} {{emailto.body}}', 'text'))
    buttons_list.append(button.create_button('Print Page', '', 'text'))
    return buttons_list

def product_list(request, nav_type="standard", nav_selection='all', paginator_page_number=1, context={}):
    """ generate a page of products as a small list
        @param paginator_page_number: int - index for paginator
    """
    nav = get_navigation(request, nav_type)
    #paginator_html = pgenerator()
    
    products = get_avail_products_for_page(paginator_page_number)
    paginator_html = pgenerator.get_navigation_from_paginator(products, "slist")
    #print("paginator html = %s" % paginator_html)
    #print("diplay_type_url = %s" % get_display_type_url(nav_type, nav_selection, 0))

    

    return render_to_response('slist.html',
                                {"menuselected":  "menu_products"
                                 ,"page_info": _set_page_paramters() # set basic page information
                                 ,'nav_type': nav_type
                                 ,"navigation_menu": nav
                                 ,'nav_selection': nav_selection
                                 ,'display_type': 0
                                 ,'display_list_url': get_display_type_url(nav_type, nav_selection, 0)
                                 ,'display_detailed_list_url': get_display_type_url(nav_type, nav_selection, 1)
                                 ,'display_grid_url': get_display_type_url(nav_type, nav_selection, 2)
                                 ,'paginator_html': paginator_html
                                 ,"products": products
                                 ,'buttons_list': get_products_top_button_list(nav_type)
                                 ,"emailto": {'subject': 'Simthetiq Products', 'body': get_display_type_url(nav_type, nav_selection, 0, True)} },
                                context_instance=RequestContext(request))


def product_detailed_list(request, nav_type="standard", nav_selection='all', paginator_page_number=1, context={}):
    """ generate a page of all the products as a list 
        with a short description and the product image
        @param : page_number - index for paginator
    """
    nav = get_navigation(request, nav_type)
    
    products = get_avail_products_for_page(paginator_page_number, 10)
    paginator_html = pgenerator.get_navigation_from_paginator(products, "slist")
    #print("paginator html = %s" % paginator_html)
    #print("diplay_type_url = %s" % get_display_type_url(nav_type, nav_selection, 0))

    return render_to_response('detailed_list.html',
                                {"menuselected":  "menu_products"
                                 ,"page_info": _set_page_paramters() # set basic page information
                                 ,'nav_type': nav_type
                                 ,"navigation_menu": nav
                                 ,'nav_selection': nav_selection
                                 ,'display_type': 1
                                 ,'display_list_url': get_display_type_url(nav_type, nav_selection, 0)
                                 ,'display_detailed_list_url': get_display_type_url(nav_type, nav_selection, 1)
                                 ,'display_grid_url': get_display_type_url(nav_type, nav_selection, 2)
                                 ,'paginator_html': paginator_html
                                 ,"products": products
                                 ,"emailto": {'subject': 'Simthetiq Products', 'body': get_display_type_url(nav_type, nav_selection, 0, True)} },
                                context_instance=RequestContext(request))

def product_grid(request, nav_type="standard", nav_selection='all', paginator_page_number=1, context={}):
    """ generate a page of products as as grid of product image 
        @param : page_number - index for paginator
    """
    pass

def GalleryPage(request, context={}):
    """ this page build a gallery with all the simthetiq product image
        it is possible to filter the image by tags
    """
    context["tags"] = productmodels.ProductPage.MediaTags.objects.all()
    #get the product page, need to link to the product
    #gallery = productmodels.GalleryPage.objects.get(id=context["current_page"].id)
    # get product
    
    context["media_library"] = productmodels.Image.objects.filter(show_in_gallery=True)
    
    return render_to_response('gallery.html',
                                context,
                                context_instance=RequestContext(request))

