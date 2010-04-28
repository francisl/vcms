# encoding: utf-8
# copyright Vimba inc. 2010
# programmer : Francis Lavoie

from django.template.loader import render_to_string


def get_page_naviation(paginator, paginator_slug=False, css_id="", css_class=""):
    """ generate a paginator naviation
        With previous, next page link, the current page and the total amount of page
        ˙
        @type paginator: paginator object
        @param paginator: The page paginator
        @type paginator_slug: string
        @param paginator_slug : to append to the previous/next URL

        @param css_id : string, id of the list container
        @param css_class : string, class name of thelist container
        @return: string containting a html page navigation
        
        @exemple - using product:
            >>> from vimba_cms_simthetiq.apps.products import models as productmodels
            >>> from django.core.paginator import Paginator
            >>> products = productmodels.ProductPage.objects.get_available_products()
            >>> paginator = Paginator(products, 5)
            >>> paginator_html = pgenerator.get_page_naviation(products, "slist")
            >>> # test
            >>> type(paginator_html)
            <type 'str'>
    """
    
    return render_to_string('paginator/paginator_nav.html', 
                            {"paginator": paginator, 
                             "paginator_slug": paginator_slug,
                             "css_id":css_id, "css_class": css_class}) 
