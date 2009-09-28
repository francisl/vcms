#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Fills the database with test data
PKG_REQUIREMENTS : django-extensions
USAGE : python manage.py runscript vimba_erp.tools.images_import
"""
import os.path
import datetime
import random
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType
from django.core.files import File

from vimba_cms_simthetiq.products.models import ProductPage, Image, Language, MediaTags

language = Language.objects.getDefault()

def importOriginalImages():
    toImport = open("tools/exportedimagesoriginal.csv", 'r')
    logfile = open("tools/log/imageoriginal_import.log", 'w')
    imagesDir = "images/"
    
    i = 0
    for line in toImport:
        if i == 0:
            #skip title
            i = 1
        else:
            logfile.write("--------------------------------\n")
            image_info = line.split(";")

            # search product
            try:
                product = ProductPage.objects.get(slug=image_info[0].lower())
            except:
                product = False
            
            if not product:
                logfile.write("Image %s has no product\n" % image_info[0])
                continue

            try:
                imagefile = os.path.join(os.path.dirname(__file__), imagesDir)
                imagefile = os.path.join(imagefile, image_info[1])
                file = File(open(imagefile, 'r'))
            except:
                logfile.write("%s : ERROR - Image file not found !\n" % image_info[1])
                continue
            
            product.original_image = file
            product.save()
            logfile.write("%s : SUCCESS - Link to %s\n" % (image_info[0], image_info[1]))
    logfile.close()

def run():
    print("importing OriginalImages ...")
    importOriginalImages()
