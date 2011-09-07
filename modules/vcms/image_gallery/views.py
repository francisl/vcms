# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import Http404
from django.core.paginator import Paginator
from django.http import Http404

from site_media.models import Image, ImageCategory
from hwm.paginator import generator as pgenerator

from vcms.www.views.html import _get_page_parameters
from vcms.image_gallery.models import ImageGalleryPage

def gallery(request, page=None, current_page=None, category=None, page_number=1, reverse_url="vcms.image_gallery.views.gallery"):
    reverse_kwargs={}
    try:
        page = request.current_page['current_page']
    except:
        raise Http404
    
    if len(request.cms_menu_extrapath) == 2:
        category = request.cms_menu_extrapath[0]
        page_number = request.cms_menu_extrapath[1]
    if len(request.cms_menu_extrapath):
        if request.cms_menu_extrapath[0].isdigit():
            page_number = request.cms_menu_extrapath[0]
        else:
            category = request.cms_menu_extrapath[0]
            
    page_info = _get_page_parameters(page)
    reverse_kwargs['page'] = page.slug

    if category:
        images_category = ImageCategory.objects.get_image_category_from_slug(category)
        reverse_kwargs['category'] = category
        images = page.get_all_images_for_category(images_category)
    else:
        images = page.get_all_images()
    
    thumbnail_size =  str(page.thumbnail_width) + 'x' + str(page.thumbnail_height)
    
    paginator = Paginator(images, page.thumbnail_per_page)
    if int(page_number) > int(paginator.num_pages):
        page_number = paginator.num_pages
    paginator_html = pgenerator.get_page_navigation(paginator, page_number, reverse_url, reverse_kwargs=reverse_kwargs)
    paginator_page = paginator.page(page_number)

    start_index = paginator_page.start_index()-1
    end_index = paginator_page.end_index()
    
    return render_to_response('gallery_content.html'
                              ,{ 'gallery_categories': page.get_image_categories() 
                                 ,'gallery_images': images[start_index:end_index]
                                 ,'gallery_page': page
                                 ,'page_category': category
                                 ,'thumbnail_size': thumbnail_size
                                 ,'paginator_html': paginator_html
                                 ,'page_info': page_info }
                              ,context_instance=RequestContext(request))
