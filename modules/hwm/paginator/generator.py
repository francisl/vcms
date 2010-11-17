# encoding: utf-8
# copyright Vimba inc. 2010
# programmer : Francis Lavoie

from django.template.loader import render_to_string
from django.core.urlresolvers import reverse

def get_navigation_from_paginator(paginator, paginator_slug=False, css_id=None, css_class=None):
    """ generate a paginator naviation from a paginator object
        Use a slug to generate the next/previous URL
                ˙
        @type paginator: paginator object
        @param paginator: The page paginator
        @type paginator_slug: string
        @param paginator_slug: to append to the previous/next URL

        @param css_id: string, id of the list container
        @param css_class: string, class name of the list container
        @return: string containing a html page navigation
        
        @exemple - using product:
            >>> from vcms_simthetiq.simthetiq_products import models as productmodels
            >>> from django.core.paginator import Paginator
            >>> from hwm.paginator import generator as pgenerator
            >>> products = productmodels.ProductPage.objects.get_available_products()
            >>> paginator = Paginator(products, 5)
            >>> paginator_html = pgenerator.get_navigation_from_paginator(products, "slist")
            >>> # test
            >>> type(paginator_html)
            <class 'django.utils.safestring.SafeUnicode'>
            
    """
    
    return render_to_string('paginator/pagination_nav_paginator.html', 
                            {"paginator": paginator, 
                             "paginator_slug": paginator_slug,
                             "css_id":css_id, "css_class": css_class}) 


def get_page_navigation(paginator, current_page_number, reverse_url=None, previous_url=None, next_url=None, css_id=None, css_class=None, reverse_kwargs={}):
    """ generate a paginator naviation with specified navigation
        With previous, next page link, the current page and the total amount of page
        
        @type paginator: paginator 
        @param paginator: page paginator
        @type previous_url: string
        @param previous_url: url for the previous page 
        @type next_url: string
        @type next_url: url for the next page

        @param css_id: string, id of the list container
        @param css_class: string, class name of the list container
        @return: string containing a html page navigation
        
        @exemple - using product:
            >>> from vcms_simthetiq.simthetiq_products import models as productmodels
            >>> from django.core.paginator import Paginator
            >>> from hwm.paginator import generator as pgenerator
            >>> products = productmodels.ProductPage.objects.get_available_products()
            >>> paginator = Paginator(products, 5)
            >>> paginator_html = pgenerator.get_page_navigation(paginator, paginator.previous_page_number, paginator.next_page_number)
            >>> # test
            >>> type(paginator_html)
            <class 'django.utils.safestring.SafeUnicode'>
            
    """
    
    current_page = paginator.page(current_page_number)
    if previous_url == None and reverse_url != None:
        previous_url = get_paginator_previous_url(paginator.page(current_page_number), reverse_url, kwargs=reverse_kwargs)
    if next_url == None and reverse_url != None:
        next_url = get_paginator_next_url(paginator.page(current_page_number), reverse_url, kwargs=reverse_kwargs)

    return render_to_string('paginator/pagination_nav.html', 
                            { "current_page": current_page
                              ,"paginator": paginator
                              ,"previous_url": previous_url
                              ,"next_url": next_url
                              ,"css_id":css_id, "css_class": css_class})


def get_paginator_next_url(page_paginator, reverse_url, page_key="page_number", kwargs={}):
    """ return the next page url using the reverse django facilities
        
        @type page_paginator: page_paginator 
        @param page_paginator: page paginator
        @type reverse_url: string
        @param reverse_url: full python path of the views function 
        @type page: string
        @type next_url: url for the next page
        
        @exemple - using product:
            >>> from vcms_simthetiq.simthetiq_products import models as productmodels
            >>> from django.core.paginator import Paginator
            >>> from hwm.paginator import generator as pgenerator
            >>> products = productmodels.ProductPage.objects.get_available_products()
            >>> paginator = Paginator(products, 5)
            >>> reverse_url = "vcms.simplenews.views.list_news"
            >>> previous_url = pgenerator.get_paginator_previous_url(paginator.page(1), reverse_url)
    """
    if page_paginator.has_next():
        kwargs[page_key] = page_paginator.next_page_number()
        return reverse(reverse_url, kwargs=kwargs)
    return None 

def get_paginator_previous_url(page_paginator, reverse_url, page_key="page_number", kwargs={}):
    """ return the next page url using the reverse django facilities
        
        @type page_paginator: page_paginator 
        @param page_paginator: page paginator
        @type reverse_url: string
        @param reverse_url: full python path of the views function 
        @type page: string
        @type next_url: url for the next page
        
        @exemple - using product:
            >>> from vcms_simthetiq.simthetiq_products import models as productmodels
            >>> from django.core.paginator import Paginator
            >>> from hwm.paginator import generator as pgenerator
            >>> products = productmodels.ProductPage.objects.get_available_products()
            >>> paginator = Paginator(products, 5)
            >>> reverse_url = "vcms.simplenews.views.list_news"
            >>> previous_url = pgenerator.get_paginator_previous_url(paginator.page(1), reverse_url)
    """
    if page_paginator.has_previous():
        kwargs[page_key] = page_paginator.previous_page_number()
        return reverse(reverse_url, kwargs=kwargs)
    return None 
