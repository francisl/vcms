#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Fills the database with test data
PKG_REQUIREMENTS : django-extensions
USAGE : python manage.py runscript vimba_erp.tools.images_original_import
"""
import os.path
import datetime
import random
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType
from django.core.files import File

from vimba_cms_simthetiq.products.models import ProductPage, Image, Language, MediaTags

language = Language.objects.getDefault()

def importImages():
    toImport = open("tools/exportedimagesoriginal.csv", 'r')
    imagesDir = "images/"
    
    i = 0
    for line in toImport:

        if i == 0:
            #skip title
            i += 1
        else:
            i += 1
            image_info = line.split(";")
            # create image only if needed
            try:
                image = Images.objects.get(name=image_info[0])
            except:
                image = False
            #if image:
            #    print("Image %s already exist" % image_info[0])
            #    continue
            
            try:
                if newImage.name == "" or newImage.name == " ":
                    print("continue, image with no name on line %d" % i)
                    continue
                else:
                    products = ProductPage.objects.filter(name__startswith=image_info[0])
            except:
                #no product found
                print("continue, image has no product(%s) attached to it" % image_info[0])
                continue
                
            if not image:
                print("Creating image = %s " % image_info[1])
                #try:
                newImage = Image()
                newImage.name = image_info[0]
                if image_info[1][0] == "*":
                    continue
                imagefile = os.path.join(os.path.dirname(__file__), imagesDir)
                imagefile = os.path.join(imagefile, image_info[1])
                try:
                    file = File(open(imagefile, 'r'))
                    print("FILE = %s " % file)
                    newImage.file = file
                    #newImage.file.save(image_info[1], file)
                except:
                    print("image not found! %s " % imagefile)
                    continue
                print("IMAGE LOCATION = %s" % newImage.file.path)
                newImage.description = image_info[2]
                newImage.show_in_gallery = image_info[4]

                #for mt in image_info[3].split(","):
                newImage.save()
                print("tags = %s" % image_info[3].split(','))
                for mediatag in image_info[3].split(','):
                    if len(mediatag) > 0:
                        if mediatag[0] == " ":
                            mediatag = mediatag[1:]
                    else:
                        continue
                    try:
                        mt = MediaTags.objects.filter(code=mediatag)[0]
                        print("MediaTags do exist : %s" % mediatag)
                    except:
                        mt = MediaTags()
                        mt.tagname = mediatag
                        mt.save()
                        print("MediaTags created: %s" % mt)
                    newImage.tags = [mt]
                    #newImage.save()
                newImage.save()
                image = newImage
            
            print("-- Linking to product")

            product.original_image = image
            product.save()
            
            print("---------")

def run():
    print("importing Image ...")
    importImages()
