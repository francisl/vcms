#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Fills the database with test data
PKG_REQUIREMENTS : django-extensions
USAGE : python manage.py runscript vimba_erp.tools.db_demo_generation
"""
import os
import datetime
import random
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType

from vimba_cms_simthetiq.apps.products.models import ProductPage, Image, Video, Category, DomainPage, FileFormat, Language

language = Language.objects.getDefault()

def createCategory(name, description, domain=False):
    logfile = open(os.path.dirname(__file__) + "/log/categories_import.log", 'w')
    logfile.write("-------------------------------\n")
    try:
        # no domain try default
        if domain == False:
            domain = DomainPage.objects.all()[0]
    except:
        domain = False
        logfile.write("Category creation Failed : No domain\n")
        return False

    try:
        newCategory = Category.objects.filter(name=name)[0]
        logfile.write("Category %s already exist !\n" % name)
    except:
        newCategory = Category()
        newCategory.name = name.replace("\n", "").replace("\r", "")
        newCategory.description = description
        newCategory.domain = domain
        newCategory.save()
        logfile.write("Category %s has been created!\n" % newCategory.name)
    
    logfile.close()
    return newCategory

def createDomain(name, slug, description="", keywords="", status=1, language=language, content="", video=False):
    slug = slug.lower().replace("\n", "").replace("\r", "")
    try:
        newDomain = DomainPage.objects.get(slug=slug)
        print("Domain %s already exist !" % name)
    except:
        newDomain = False
    
    if not newDomain:
        #try:
        newDomain = DomainPage()
        newDomain.name = name.replace("\n", "").replace("\r", "")
        newDomain.slug = slug
        newDomain.description = description
        newDomain.keywords = keywords
        newDomain.status = status
        newDomain.language = language
        newDomain.content = content
        if video:
            newDomain.video = video
        newDomain.save()
        print("Domain - %s - has been created!" % slug)
        #except:
        #    print("Error creating - Domain %s" % name)
        #    newDomain = domainPage.objects.all()[0]
    print("------")
    return newDomain

def importCategory():
    toImport = open(os.path.dirname(__file__) + "/exportedcategories.csv", 'r')
    logfile = open(os.path.dirname(__file__) + "/log/categories_import.log", 'w')
    logfile.close()
    for line in toImport:
        line_info = line.split(";")
        # create domain if needed
        try:
            category = Category.objects.get(name=line_info[0])
        except:
            category = False
        
        if category:
            print("Category %s already exist" % line_info[0])
            continue
        else:
            try:
                domain = DomainPage.objects.get(slug=line_info[1].lower())
                print("Domain %s already exist !" % line_info[1].replace("\n", "").lower())
            except:
                domain = False

            if not domain:
                domain = createDomain(line_info[1], line_info[1].replace(" ", ""), description=line_info[1], keywords=line_info[1], content=line_info[1], video=[])

            createCategory(line_info[0], "", domain)
        
def createFileFormat(name, code):
    try:
        f = FileFormat()
        f.name = name
        f.code = code
        f.save()
        print("Fileformat created : %s" % code)
    except:
        f = None
        print("Failed to create fileformat : %s" % code)
        
    return f

def importProducts():
    toImport = open(os.path.dirname(__file__) + "/exportedproducts.csv", 'r')
    logfile = open(os.path.dirname(__file__) + "/log/product_import.log", 'w')
    i = 0
    for line in toImport:
        logfile.write("--------------------------------\n")
        if i == 0:
            #skip title
            i = 1
        else:
            product_info = line.split(";")
            # create product only if needed
            try:
                product = ProductPage.objects.get(slug=product_info[1].lower())
            except:
                product = False
            if product:
                logfile.write("Product %s already exist\n" % product_info[0])
                continue
            
            if product_info[0] == "" or product_info[0] == " ":
                if product_info[1] == "" or product_info[1] == " ":
                    print("Product with empty name can't be created!")
                    continue
                else:
                    product_info[0] = product_info[1]

            # print col assigment
            print("Line === %s " % line)
            print("Name : " + product_info[0].replace("\r", "").replace("\n", ""))
            print("slug : " + product_info[1].replace("\n", "").replace("\r", "").lower())
            print("description : " + product_info[2].replace("_", " "))
            print("keywords : " + product_info[3].replace("_", " "))
            print("status : " + (product_info[4] if product_info[4] else 0))
            print("product_description : " + product_info[5].replace("_", " "))
            print("product_id : " + str(product_info[6] if product_info[6] else 0))
            print("polygon : " + str(int(product_info[7].replace(" ","")) if product_info[7] else 0))
            print("texture_format : " + product_info[8])
            print("texture_resolution : " + (product_info[9] if product_info[9] else 0))

            print("category : " + (product_info[11]))
            print("file format : " + (product_info[12]))
            
            
            #image = product_info[14].split("\\")
            #print("original_image = %s " % image[len(image)-1:])
            #try:
            newProduct = ProductPage()
            newProduct.name = product_info[0].replace("\r", "").replace("\n", "")
            newProduct.slug = product_info[1].replace("\n", "").replace("\r", "").replace("/", "_").lower()
            newProduct.description = product_info[2].replace("_", " ")
            newProduct.keywords = product_info[3].replace("_", " ")
            newProduct.status = (product_info[4] if product_info[4] else 0)
            newProduct.language = language
    
            newProduct.product_description = product_info[5].replace("_", " ")
            newProduct.product_id = (product_info[6] if product_info[6] else 0)
            newProduct.polygon = (int(product_info[7].replace(" ","")) if int(product_info[7].replace(" ","")) else 0)
            newProduct.texture_format = product_info[8]
            newProduct.texture_resolution = (product_info[9] if product_info[9] else 0)

            #newProduct.image = product_info[10]
            
            # foreign key ->
            try:
                c = product_info[11]
                category = Category.objects.filter(name=c)[0]
            except:
                if product_info[11] == "":
                    logfile.write("using default category !\n")
                    category = Category.objects.get(name="Other")
                else:
                    category = createCategory(product_info[11], "")
                    logfile.write("creating new category !\n")
            
            newProduct.category = category
            # save before assigning m2m key
            newProduct.save(reorder=False)
            
            # multiple line ->
            #for ff in product_info[16].split(","):
            # newProduct.save()
            # FILEFORMAT
            for fileformat in product_info[12].split(','):
                fileformat = fileformat.lower()
                fileformat = fileformat.replace(" ", "")
                try:
                    ff = FileFormat.objects.filter(code=fileformat)[0]
                    print("Fileformat exist : %s" % fileformat)
                except:
                    ff = createFileFormat(fileformat,fileformat)
                newProduct.file_format = [ff]

            newProduct.save()

            logfile.write("Created product = %s \n" % newProduct.name)
            logfile.write("     File Format = %s \n" % newProduct.file_format)
            logfile.write("            Slug = %s \n" % newProduct.slug)
            logfile.write("        Category = %s \n" % newProduct.category)
    logfile.close()

def run():
    print("import ")
    print("importing category ...")
    importCategory()
    print("importing Product ...")
    importProducts()
