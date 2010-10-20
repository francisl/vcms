#!/usr/bin/env python
# -*- coding: utf-8 -*-

from vimba_cms_simthetiq.apps.products.models import ProductPage, Image, Video, Category, DomainPage, FileFormat
from site_language.models import Language


language = Language.objects.get_default()
 
num_product=10
for i in range(num_product):
    newProduct = ProductPage(name="test " + str(i), slug="test_" + str(i), description="test " + str(i), 
                            keywords = "", status=0, language = language, product_description = "test " + str(i), 
                            product_id=0, polygon=0, texture_format="test format", texture_resolution=0, category=Category.objects.all()[0])
    newProduct.save()

c = Category.objects.all()[0]
    
newProduct = ProductPage(name="test 1", slug="test_1", description="test 1", keywords = "", status=0, language = language, product_description = "test 1", product_id=0, polygon=0, texture_format="", texture_resolution=0, category=Category.objects.all()[0])
newProduct.save()
newProduct2 = ProductPage(name="test 2", slug="test_2", description="test 2", keywords = "", status=0, language = language, product_description = "test 2", product_id=0, polygon=0, texture_format="", texture_resolution=0, category=Category.objects.all()[0])
newProduct2.save()
newProduct3 = ProductPage(name="test 3", slug="test_3", description="test 3", keywords = "", status=0, language = language, product_description = "test 3", product_id=0, polygon=0, texture_format="", texture_resolution=0, category=Category.objects.all()[0])
newProduct3.save()
newProduct4 = ProductPage(name="test 4", slug="test_4", description="test 4", keywords = "", status=0, language = language, product_description = "test 4", product_id=0, polygon=0, texture_format="", texture_resolution=0, category=Category.objects.all()[0])
newProduct4.save()
newProduct5 = ProductPage(name="test 5", slug="test_5", description="test 5", keywords = "", status=0, language = language, product_description = "test 5", product_id=0, polygon=0, texture_format="", texture_resolution=0, category=Category.objects.all()[0])
newProduct5.save()
newProduct6 = ProductPage(name="test 6", slug="test_6", description="test 6", keywords = "", status=0, language = language, product_description = "test 6", product_id=0, polygon=0, texture_format="", texture_resolution=0, category=Category.objects.all()[0])
newProduct6.save()
newProduct7 = ProductPage(name="test 7", slug="test_7", description="test 7", keywords = "", status=0, language = language, product_description = "test 7", product_id=0, polygon=0, texture_format="", texture_resolution=0, category=Category.objects.all()[0])
newProduct7.save()
newProduct8 = ProductPage(name="test 8", slug="test_8", description="test 8", keywords = "", status=0, language = language, product_description = "test 8", product_id=0, polygon=0, texture_format="", texture_resolution=0, category=Category.objects.all()[0])
newProduct8.save()
newProduct9 = ProductPage(name="test 9", slug="test_9", description="test 9", keywords = "", status=0, language = language, product_description = "test 9", product_id=0, polygon=0, texture_format="", texture_resolution=0, category=Category.objects.all()[0])
newProduct9.save()
