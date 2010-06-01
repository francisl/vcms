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

language = Language.objects.get_default()


def createNewImage(name, file_name=None, description=None, tags=None, show_in_gallery=False):
    imagesDir = os.path.dirname(__file__) + "/images/"
    
    if file_name==None or description==None:
        return 0

    newImage = Image()
    newImage.name = name
    imagefile = os.path.join(os.path.dirname(__file__), imagesDir)
    imagefile = os.path.join(imagefile, file_name)
    try:
        file = File(open(imagefile, 'r'))
        newImage.file = file
    except:
        #print("image not found! %s " % imagefile)
        return 2

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
            if mediatag == "":
                continue
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


def _checkRow(line, number):
    if len(line) < 6 or len(line) > 6:
        print("Failed | line %s | %s | %s" % (number, line[0], len(line)))
        return False
    else:
        print("Success | line %s | %s | %s" % (number, line[0], len(line)))
        return True

        
def checkRows():
    print("---------------------------------------")
    print(" Images Validation ")
    try:
        rows = open(os.path.dirname(__file__) + "/datasource/images.csv", 'r')
    except:
        print("data file images.csv not found!")
        return False
    
    Error = 0
    i = 0
    for row in rows:
        if i != 0:
            row = row.split(";")
            r = _checkRow(row, i)
            if r == False:
                Error = Error + 1
        i = i + 1

    rows.close()


def importImages(drop=False, debug=False):
    status = {0:"Missing information", 2:"File not found"}
    try:
        toImport = open(os.path.dirname(__file__) + "/datasource/images.csv", 'r')
    except:
        if debug: print("data file images.csv not found!")
        return False
    logfile = open(os.path.dirname(__file__) + "/log/image_import_log.csv", 'w')
    logfile.write("Status;Descript;images;LinkedTo\n")
    
    if drop:
        for img in Image.objects.all():
            if debug: print("deleting : %s " % img)
            img.delete()

    i = 0
    for line in toImport:
        if i == 0:
            #skip title
            i = 1
        else:
            i = i + 1
            image_info = line.split(";")
            # create image only if needed
            
            #check number of line
            if len(image_info) < 6 or len(image_info) > 6:
                if debug: print("Failed;# of Column Error on line %s;;;" % str(i))
                logfile.write("Failed;# of Column Error on line %s;;;\n" % str(i))
                continue
            
            try:
                image = Image.objects.get(name=image_info[0])
            except:
                image = False
            
            if image:
                logfile.write("Failed;Already exist;%s;\n" % image_info[0])
                if debug: print("Failed;Already exist;%s;" % image_info[0])
                continue

            newImage = createNewImage(image_info[0], file_name=image_info[1], description=image_info[2], tags=image_info[3], show_in_gallery=image_info[4])

            added_to = []
            for product in image_info[5].replace("\"", "").split(','):
                product = product.lower().replace('\n','').replace('\r','').replace(" ", "")
                if newImage != 0 and newImage != 2:
                    try:
                        if newImage.name == "" or newImage.name == " ":
                            productObj = []
                        else:
                            productObj = ProductPage.objects.get(slug=product)
                            added_to = added_to + [productObj]
                    except:
                        productObj = []

                    if isinstance(productObj, ProductPage):
                        productObj.images = list(productObj.images.all()) + [newImage]
                        productObj.save(reorder=False)
                        
                    logfile.write("Success;;%s;%s\n" % (image_info[0], productObj))
                    if debug: print("Success;;%s;%s" % (image_info[0], productObj))
                else:
                    logfile.write("Failed;No Product Found;%s;%s;\n" % (image_info[0], status[newImage]))
                    if debug: print("Failed;No Product Found;%s;%s;" % (image_info[0], status[newImage]))

    toImport.close()
    logfile.close()


def relinkImages():
    try:
        toImport = open(os.path.dirname(__file__) + "/datasource/images.csv", 'r')
    except:
        print("data file images.csv not found!")
        return False
    
    logfile = open(os.path.dirname(__file__) + "/log/image_relink.log", 'w')

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

            if not image:
                continue
            print("images info 5 %s" % image_info[5])
            for product in image_info[5].replace("\"", "").replace(" ", "").split(','):
                product = product.lower().replace('\n','').replace('\r','').replace(" ", "")
                print("seaching product %s" % product)
                try:
                    productObj = ProductPage.objects.get(slug=product)
                except:
                    continue
                
                #print("product obj = %s" % productObj) 
                if isinstance(productObj, ProductPage):
                    #print("product obj is instance : typeof = %s" % type(productObj))
                    productObj.images = list(productObj.images.all()) + [image]
                    productObj.save(reorder=False)
                    logfile.write("Image %s, link to = %s products\n" % (image.name,productObj))
                    logfile.write("image as tag = %s\n" % image.tags)
                else:
                    logfile.write("Image %s Failed!\n" % image_info[0])
                    
    logfile.close()
    
    
def run():
    importImages()
