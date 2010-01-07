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
    context.update(InitPage(page=page))
    context.update(locals())
    
    if context["module"] in globals():
        return globals()[context["module"]](request, context)
    else:
        return HttpResponseRedirect("/")
    

def Product(request, context={}):
    #print("------------- product -------------")
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
    
    #print("PRODUCT INFORMATION %s " % product_information)
    return render_to_response('product_info.html',
                                { "menuselected":  "menu_products",
                                  "current_page":   context['current_page'],
                                  "productpage":    productpage,
                                  "category":       category,
                                  "product_contents": product_contents },
                                context_instance=RequestContext(request))


def getPageList():
    return Paginator(productmodels.ProductPage.objects.all(), 1)

def Domain(request, context={}):
    #print("------------- Domain -------------")
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


def GalleryPage(request, context={}):
    #print("------------- Gallery -------------")
    tags = productmodels.MediaTags.objects.all()
    #get the product page, need to link to the product
    #gallery = productmodels.GalleryPage.objects.get(id=context["current_page"].id)
    # get product
    
    media = productmodels.Image.objects.filter(show_in_gallery=True)
    
    """
    media_array = []
     
    media_len = len(mediat)
    cols = media_len/5
    if media_len % 5: # add one row if necessary
        cols = cols + 1

    bdrange = [0,5]
    for col in range(cols):
        #sprint("range : %s" % range(cols))
        media_array.append(mediat[bdrange[0]:bdrange[1]])
        bdrange[0],bdrange[1] = bdrange[1], bdrange[1]+5
    """
    
    return render_to_response('gallery.html',
                                { 
                                "current_page":  context['current_page'],
                                "tags": tags,
                                #"media": mediat,
                                "media_library": media,
                                #"media_array": media_array,
                                #"cols": range(cols),
                                #"rows": range(5)
                                },
                                context_instance=RequestContext(request))
     