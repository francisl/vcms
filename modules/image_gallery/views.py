# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404
from django.core.paginator import Paginator

from site_media.models import Image, ImageCategory
from image_gallery.models import ImageGalleryPage
from hwm.paginator import generator as pgenerator


def gallery(request, page=None, category=None, page_number=1):
    reverse_kwargs={}
    gallery_page = ImageGalleryPage.objects.get_seletcted_page(page)
    reverse_kwargs['page'] = page
    if gallery_page == None:
        raise Http404

    images_category = ImageCategory.objects.filter(default_name=category)
    if len(images_category) > 0:
        reverse_kwargs['category'] = category
    images = gallery_page.get_all_images_for_category(images_category)
    
    thumbnail_size =  str(gallery_page.thumbnail_width) + 'x' + str(gallery_page.thumbnail_height)
    
    reverse_url = "image_gallery.views.gallery"

    paginator = Paginator(images, gallery_page.thumbnail_per_page)
    if int(page_number) > int(paginator.num_pages):
        print('yes its bigger')
        page_number = paginator.num_pages
    page_paginator = pgenerator.get_page_navigation(paginator, page_number, reverse_url, reverse_kwargs=reverse_kwargs)
    
    page = paginator.page(page_number)


    start_index = page.start_index()-1
    end_index = page.end_index()
    
    print("start index %s" % start_index)
    print("End index %s" % end_index)
    
    return render_to_response('gallery_content.html'
                              ,{ 'gallery_categories': gallery_page.get_image_categories() 
                                 ,'gallery_images': images[start_index:end_index]
                                 ,'gallery_page': gallery_page
                                 ,'thumbnail_size': thumbnail_size
                                 ,'page_paginator': page_paginator }
                              ,context_instance=RequestContext(request))
