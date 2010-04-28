# encoding: utf-8
# copyright Vimba inc. 2010
# programmer : Francis Lavoie

from django.template.loader import render_to_string


def get_page_navigation(paginator, paginator_slug=False, css_id="", css_class=""):
    """ generate a paginator naviation
        With previous, next page link, the current page and the total amount of page
        ˙
        @type paginator: paginator object
        @param paginator: The page paginator
        @type paginator_slug: string
        @param paginator_slug: to append to the previous/next URL

        @param css_id: string, id of the list container
        @param css_class: string, class name of the list container
        @return: string containing a html page navigation
        
        @exemple - using product:
            >>> from vimba_cms_simthetiq.apps.products import models as productmodels
            >>> from django.core.paginator import Paginator
            >>> from vcms.apps.vwm.paginator import generator as pgenerator
            >>> products = productmodels.ProductPage.objects.get_available_products()
            >>> paginator = Paginator(products, 5)
            >>> paginator_html = pgenerator.get_page_navigation(products, "slist")
            >>> # test
            >>> type(paginator_html)
            <class 'django.utils.safestring.SafeUnicode'>
            
    """
    
    return render_to_string('paginator/paginator_nav.html', 
                            {"paginator": paginator, 
                             "paginator_slug": paginator_slug,
                             "css_id":css_id, "css_class": css_class}) 
