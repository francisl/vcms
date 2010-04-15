# encoding: utf-8
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Template, Context, RequestContext 
from django import forms
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from config import simthetiq_config 
from vimba_cms_simthetiq.apps.products import models as productmodels
from vcms.apps.www.views import InitPage

def Generic(request, page=None, product=None, selected_category=None, slug=None, context={}):
    """ Is called first, then it calls the right view base on module name containt in the url
    """
    context.update(InitPage(page_slug=page, app_slug=productmodels.APP_SLUGS))
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
        request.session['navigation_type'] = "compact"
        
    if request.session.get('navigation_type') == "DIS":
        menu = category.get_navigation_menu()
    elif request.session.get('navigation_type') == "compact":
        menu = CompactNavigationGroup.get_navigation()
    
    #print("PRODUCT INFORMATION %s " % product_information)
    return render_to_response('product_info.html',
                                { "menuselected":  "menu_products",
                                  "current_page":   context['current_page'],
                                  "productpage":    productpage,
                                  "category":       category,
                                  "product_contents": product_contents,
                                  "navigation_menu": menu },
                                context_instance=RequestContext(request))

def set_navigation_type(request, page=None, type="compact"):
    """ Set the naviation type into the user's session
    """
    request.session['navigation_type'] = type # compact or DIS
    return Product(request, InitPage(page=page))
    

def productHome(request, context={}):
    from vcms.apps.vwm.tree import generator
    
    context.update(InitPage(page_slug=None, app_slug=productmodels.APP_SLUGS))
    context.update(locals())
    
    # set navigation type if not set
    if request.session.get('navigation_type') == "":
        request.session['navigation_type'] = "compact"
        
    if request.session.get('navigation_type') == "DIS":
        nav = category.get_navigation_menu()
    else: #if request.session.get('navigation_type') == "compact":
        nav = generator.generate_tree(productmodels.CompactNavigationGroup.objects.get_navigation())

    print("navigation = %s" % nav)
    return render_to_response('product_info.html',
                                { "menuselected":  "menu_products",
                                  "current_page":   context['current_page'],
                                  "navigation_menu": nav },
                                context_instance=RequestContext(request))
    

"""
def Domain(request, context={}):
    #print("selected_category is set : %s " % type(context["selected_category"]))
    # selected the domain page to retreive information not in www.models.page
    try:
        #print("context['current_page'].id = %s" % context['current_page'].id)
        domain_page = productmodels.DomainPage.objects.get(id=context['current_page'].id)
    except:
        domain_page  = None
        return render_to_response('master.html', 
                              context,
                              context_instance=RequestContext(request))
    
    try:
        context['elements'] = productmodels.DomainElement.objects.filter(page=domain_page , published=True)
    except productmodels.ObjectDoesNotExist: 
        context['elements'] = []
    #print("context elements : %s " % context['elements'])
    
    # create a list of dictionary binding type to product(s)
    categories = []
    #prodByCategories = {}
    #product_paginator = getPageList()
    for category in productmodels.Category.objects.filter(domain = domain_page.id):
        #if not prodByCategories.has_key(category.name):
        #    prodByCategories[category.name] = []
        
        products = productmodels.ProductPage.objects.filter(category=category.id)
        pageproducts = []
        for p in products:
            pageproducts.append(p)
        
        #for p in product_paginator.page_range:
        #    if product_paginator.object_list[p-1].category == category.name:
        #        prodByCategories[category.name].append(product_paginator.object_list[p-1])
                     
        if len(products) != 0:
            # only takes types that have product associated to them
            categories.append({"category": category, "products": pageproducts}) 
    context['categories'] = categories
    #context['product_paginator'] = product_paginator
    #print prodByCategories
    #print "------------------"
    #print product_paginator.num_pages
    
    del categories
    
    # File Format
    context['file_format'] = domain_page.file_format.all()
    context['domain_page'] = domain_page
    
    if context["selected_category"] == None:
        del context["selected_category"]
    else:
        # needed in order to make comparaison with ids in template
        context["selected_category"] = int(context["selected_category"])
    
    return render_to_response('domain/index_domain.html',
                              context,
                              context_instance=RequestContext(request))
"""

def GalleryPage(request, context={}):
    """ this page build a gallery with all the simthetiq product image
        it is possible to filter the image by tags
    """
    context["tags"] = productmodels.MediaTags.objects.all()
    #get the product page, need to link to the product
    #gallery = productmodels.GalleryPage.objects.get(id=context["current_page"].id)
    # get product
    
    context["media_library"] = productmodels.Image.objects.filter(show_in_gallery=True)
    
    return render_to_response('gallery.html',
                                context,
                                context_instance=RequestContext(request))

  
"""
def ProductGallery(request, context={}):
    # create a list of dictionary binding type to product(s)
    categories = []
    #prodByCategories = {}
    #product_paginator = getPageList()
    for category in productmodels.Category.objects.filter(domain = domain_page.id):
        #if not prodByCategories.has_key(category.name):
        #    prodByCategories[category.name] = []
        
        products = productmodels.ProductPage.objects.filter(category=category.id)
        pageproducts = []
        for p in products:
            pageproducts.append(p)
        
        #for p in product_paginator.page_range:
        #    if product_paginator.object_list[p-1].category == category.name:
        #        prodByCategories[category.name].append(product_paginator.object_list[p-1])
                     
        if len(products) != 0:
            # only takes types that have product associated to them
            categories.append({"category": category, "products": pageproducts}) 
    context['categories'] = categories
    
    del categories
    
    # File Format
    context['file_format'] = domain_page.file_format.all()
    context['domain_page'] = domain_page
    
    if context["selected_category"] == None:
        del context["selected_category"]
    else:
        # needed in order to make comparaison with ids in template
        context["selected_category"] = int(context["selected_category"])
    
    return render_to_response('product_gallery.html',
                              context,
                              context_instance=RequestContext(request))
"""
