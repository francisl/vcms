# encoding: utf-8
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Template, Context, RequestContext 
from django import forms
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from config import simthetiq_config 
from vimba_cms_simthetiq.apps.products import models as productmodels
from vcms.apps.www.views import InitPage, setPageParameters

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
    from vcms.apps.www.models import MenuLocalLink
    page = MenuLocalLink.objects.get(local_link="/products/home")
    context.update(setPageParameters(page))
    context.update(locals())
    
    # set navigation type if not set
    if request.session.get('navigation_type') == "":
        request.session['navigation_type'] = "compact"
        
    if request.session.get('navigation_type') == "DIS":
        nav = category.get_navigation_menu()
    else: #if request.session.get('navigation_type') == "compact":
        nav = generator.generate_tree(productmodels.CompactNavigationGroup.objects.get_navigation())

    print("navigation = %s" % str(nav))
    print("context menustyle = %s" % str(context["menu_style"]))
    print("context current_page = %s" % str(context["current_page"]))
    return render_to_response('product_home.html',
                                { "menuselected":  "menu_products",
                                  "menu_style" : context['menu_style'],
                                  "current_page":   page,
                                  "navigation_menu": nav },
                                context_instance=RequestContext(request))
    

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

