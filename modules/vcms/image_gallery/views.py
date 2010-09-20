# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import Http404
from django.core.paginator import Paginator

from site_media.models import Image, ImageCategory
from hwm.paginator import generator as pgenerator

from vcms.www.views.html import _get_page_parameters
from vcms.image_gallery.models import ImageGalleryPage

def gallery(request, page=None, category=None, page_number=1):
    reverse_kwargs={}
    reverse_kwargs['page'] = page
    
    page = get_object_or_404(ImageGalleryPage, slug=page)
    page_info = _get_page_parameters(page)

    images_category = ImageCategory.objects.filter(default_name=category)
    if len(images_category) > 0:
        reverse_kwargs['category'] = category
    images = page.get_all_images_for_category(images_category)
    
    thumbnail_size =  str(page.thumbnail_width) + 'x' + str(page.thumbnail_height)
    
    reverse_url = "vcms.image_gallery.views.gallery"

    paginator = Paginator(images, page.thumbnail_per_page)
    if int(page_number) > int(paginator.num_pages):
        page_number = paginator.num_pages
    paginator_html = pgenerator.get_page_navigation(paginator, page_number, reverse_url, reverse_kwargs=reverse_kwargs)
    
    paginator_page = paginator.page(page_number)


    start_index = paginator_page.start_index()-1
    end_index = paginator_page.end_index()
    
    print(type(page))
    return render_to_response('gallery_content.html'
                              ,{ 'gallery_categories': page.get_image_categories() 
                                 ,'gallery_images': images[start_index:end_index]
                                 ,'gallery_page': page
                                 ,'thumbnail_size': thumbnail_size
                                 ,'paginator_html': paginator_html
                                 ,'page_info': page_info }
                              ,context_instance=RequestContext(request))
