# encoding: utf-8
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Template, Context, RequestContext 
from django import forms
from django.core.paginator import Paginator, InvalidPage, EmptyPage

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
    return productHome(request, InitPage(page=page))
    

def get_navigation(request):
    """ Take a request and return the html navigation
    """
    from vcms.apps.vwm.tree import generator
    if request.session.get('navigation_type') == "DIS":
        return category.get_navigation_menu()
    else: #if request.session.get('navigation_type') == "compact":
        return generator.generate_tree(productmodels.CompactNavigationGroup.objects.get_navigation())

def productHome(request, context={}):
    from vcms.apps.www.models import MenuLocalLink
    
    page = MenuLocalLink.objects.get(local_link="/products/home")
    context.update(setPageParameters(page))
    context.update(locals())
    
    # set navigation type if not set
    if request.session.get('navigation_type') == "":
        request.session['navigation_type'] = "compact"
        
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
        print("page_num condition!!!!")
        print(type(page_num))
        print(type(0))
        page_num = 1
        
    print("page num = %s" % page_num)
    try: # make sure the page number is not off
        return paginator.page(page_num)
    except:
        return paginator.page(paginator.num_pages)
        

def ProductSList(request, paginator_page_number=1, slug='', context={}):
    """ generate a page of products as a small list
        @param paginator_page_number: int - index for paginator
    """
    from vcms.apps.vwm.paginator import generator as pgenerator
    context.update(setPageParameters())
    context.update(locals())
    page = None
    nav = get_navigation(request)
    #paginator_html = pgenerator()
    print("paginator_page_number = %s" % paginator_page_number)

    products = getProductPaginator(productmodels.ProductPage.objects.get_available_products(), 
                                   page_num=paginator_page_number,
                                   item_per_page=20)
    
    paginator_html = pgenerator.get_page_naviation(products, "slist")
    print("paginator_html = %s" % paginator_html)

    return render_to_response('slist.html',
                                { "menuselected":  "menu_products",
                                  "menu_style" : context['menu_style'],
                                  "current_page":   page,
                                  "navigation_menu": nav,
                                  'paginator_html': paginator_html,
                                  "products": products },
                                context_instance=RequestContext(request))

def ProductList(request, context={}):
    """ generate a page of all the products as a list 
        with a short description and the product image
        @param : page_number - index for paginator
    """
    pass

def ProductGrid(request, context={}):
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

