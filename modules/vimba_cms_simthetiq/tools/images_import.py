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

from vimba_cms_simthetiq.apps.products.models import ProductPage, Image, Language, MediaTags

language = Language.objects.getDefault()


def createNewImage(name, file_name=None, description=None, tags=None, show_in_gallery=False):
    imagesDir = os.path.dirname(__file__) + "/images/"
    
    if file_name==None or description==None or tags==None:
        return False

    newImage = Image()
    newImage.name = name
    imagefile = os.path.join(os.path.dirname(__file__), imagesDir)
    imagefile = os.path.join(imagefile, file_name)
    try:
        file = File(open(imagefile, 'r'))
        newImage.file = file
    except:
        #print("image not found! %s " % imagefile)
        return False

    newImage.description = description
    newImage.show_in_gallery = show_in_gallery

    #for mt in image_info[3].split(","):
    newImage.save()
    for mediatag in tags.split(','):
        if len(mediatag) > 0:
            if mediatag[0] == " ":
                mediatag = mediatag[1:]
        try:
            mt = MediaTags.objects.filter(tagname=mediatag)[0]
            #print("MediaTags do exist : %s" % mediatag)
        except:
            mt = MediaTags()
            mt.tagname = mediatag
            mt.save()
            #print("New MediaTags created: %s" % mt)
        newImage.tags = [mt]
        newImage.save()
    newImage.save()
    #except:
    #    print("Can't create image %s" % name)
    #    newImage = False

    return newImage

def importImages():
    toImport = open(os.path.dirname(__file__) + "/exportedimages.csv", 'r')
    logfile = open(os.path.dirname(__file__) + "/log/image_import.log", 'w')

    i = 0
    for line in toImport:
        if i == 0:
            #skip title
            i = 1
        else:
            logfile.write("--------------------------------\n")
            image_info = line.split(";")
            # create image only if needed
            try:
                image = Image.objects.get(name=image_info[0])
            except:
                image = False
            if image:
                logfile.write("Image %s already exist\n" % image_info[0])
                continue

            newImage = createNewImage(image_info[0], file_name=image_info[1], description=image_info[2], tags=image_info[3], show_in_gallery=image_info[4])
            
            added_to = []
            for product in image_info[5].replace("\"", "").split(','):
                product = product.lower().replace('\n','').replace('\r','').replace(" ", "")
                if newImage:
                    try:
                        if newImage.name == "" or newImage.name == " ":
                            productObj = []
                        else:
                            productObj = ProductPage.objects.get(slug=product)
                            added_to = added_to + [productObj]
                    except:
                        #no product found
                        productObj = []

                    print("product obj = %s" % productObj) 
                    if isinstance(productObj, ProductPage):
                        print("product obj is instance : typeof = %s" % type(productObj))
                        productObj.images = list(productObj.images.all()) + [newImage]
                        productObj.save(reorder=False)
                    logfile.write("Image %s, link to = %s products\n" % (newImage.name,productObj))
                    logfile.write("image as tag = %s\n" % newImage.tags)
                else:
                    logfile.write("Image %s Failed!\n" % image_info[0])
                    
    logfile.close()

def run():
    print("importing Image ...")
    importImages()
