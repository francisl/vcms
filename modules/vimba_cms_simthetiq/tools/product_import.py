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
from django.core.files import File

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
    slug = slug.lower().replace("\n", "").replace("\r", "").replace("(", "_").replace(")", "_")
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
    try:
        toImport = open(os.path.dirname(__file__) + "/datasource/categories.csv", 'r')
    except:
        print("data categories.csv file not found!")
        
    logfile = open(os.path.dirname(__file__) + "/log/categories_import.log", 'w')
    logfile.close()
    print("----------------------------------------------------------------------")
    print("importing category ...")
    
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
        f.code = code[:3]
        f.save()
        print("Fileformat created : %s" % code)
    except:
        f = None
        print("Failed to create fileformat : %s" % code)
        
    return f

def printLine(line, printFullLine=False):
    product_info = line
    # print col assigment
    if printFullLine:
        print("Line === %s " % product_info)
    print("Name : " + product_info[0].replace("\r", "").replace("\n", "").replace("\"", ""))
    print("slug : " + product_info[1].replace("\n", "").replace("\r", "").replace("\"", "").lower())
    print("description : " + product_info[2].replace("_", " ").replace("\"", ""))
    print("keywords : " + product_info[3].replace("_", " ").replace("\"", ""))
    print("status : " + (product_info[4].replace("\"", "") if product_info[4].replace("\"", "") else 0))
    print("product_description : " + product_info[5].replace("_", " ").replace("\"", ""))
    print("product_id : " + str(product_info[6].replace("\"", "") if product_info[6].replace("\"", "") else 0))
    print("polygon : " + str(int(product_info[7].replace(" ","").replace("\"", "")) if product_info[7].replace("\"", "") else 0))
    print("texture_format : " + product_info[8].replace("\"", ""))
    print("texture_resolution : " + (product_info[9].replace("\"", "") if product_info[9].replace("\"", "") else 0))
    print("original image : " + (product_info[10].replace("\"", "")))
    print("category : " + (product_info[11].replace("\"", "")))
    print("file format : " + (product_info[12].replace("\"", "")))


def _productFileValidation():
    try:
        toImport = open(os.path.dirname(__file__) + "/datasource/products.csv", 'r')
    except:
        print("data file products.csv not found!")
        toImport = False
    
    return toImport

def _checkRow(line, number):
    if len(line) < 13 or len(line) > 13:
        print("Failed | line %s | %s | %s" % (number, line[0], len(line)))
        return False
    else:
        print("Success | line %s | %s | %s" % (number, line[0], len(line)))
        return True
        
def checkRows(printInfo=False):
    print("---------------------------------------")
    print(" Products Validation ")
    rows = _productFileValidation()
    
    Error = 0
    i = 0
    for row in rows:
        if i != 0:
            row = row.split(";")
            r = _checkRow(row, i)
            if printInfo:
                printLine(row)
            if r == False:
                Error = Error + 1
        i = i + 1

    rows.close()

def setOriginalImage(print_line=False, debug=False):
    toImport = _productFileValidation()
        
    logfile = open(os.path.dirname(__file__) + "/log/originalimage_import_log.csv", 'w')
    i = 0
    logfile.write("Status;Description;Product;Image to be set;Image Status;\n")
    print("----------------------------------------------------------------------")
    print("linking original images ...")
    for line in toImport:
        if i == 0:
            #skip title
            i = 1
        else:
            i = i+1
            product_info = line.split(";")

            #check number of line
            if len(product_info) < 13 or len(product_info) > 13:
                if debug: print("Failed;# of Column Error on line %s;;" % str(i))
                logfile.write("Failed;# of Column Error on line %s;;\n" % str(i))
                continue
            
            product_slug = product_info[1].replace("\n", "").replace("\r", "").replace("/", "_").replace("\"", "").replace("(", "_").replace(")", "_").lower()
            product_image = product_info[10]
            
            #print("line = %s" % product_info)
            if print_line:        
                printLine(product_info)
                
            try:
                product = ProductPage.objects.get(slug=product_slug)
            except:
                product = False
                
            if product:
                try:
                    product.original_image = Image.objects.get(name__iexact=product_image)
                    product.save(reorder=False)
                    logfile.write("Success;Found;%s\n" % product_slug)
                    if debug: print("Success;;%s;%s;" % (product_slug, product_image))
                except:
                    logfile.write("Failed;Image not found;%s;%s\n" % (product_slug, product_image))
                    if debug: print("Failed;Image not found;%s;%s;" % (product_slug, product_image))
                
            else:
                logfile.write("Failed;Product not Found;%s;%s;None\n" % (product_slug, product_image))
                if debug: print("Failed;%s;Product not Found;%s;None" % (product_slug, product_image))
        
    toImport.close()
    logfile.close()

            
def importProducts(printLine=False, drop=False, debug=False, hasTitle=True):
    
    toImport = _productFileValidation()
    logfile = open(os.path.dirname(__file__) + "/log/product_import_log.csv", 'w')
    i = 0
    if debug: print("----------------------------------------------------------------------")
    if debug: print("importing Product ...")
    logfile.write("status;status;Product;description;category")
    
    if drop == True:
        for p in ProductPage.objects.all():
            if p.slug != "afghanistan_database":
                if debug: print("deleting : %s " % p)
                p.delete()
                
    for line in toImport:
        if hasTitle and i == 0:
            #skip title
            i = 1
        else:
            i = i + 1
            product_info = line.split(";")
            
            #check number of line
            if len(product_info) < 13 or len(product_info) > 13:
                if debug: print("Failed;# of Column Error on line %s;;;" % str(i))
                logfile.write("Failed;# of Column Error on line %s;;;\n" % str(i))
                continue
            
            if product_info[0].replace("\"", "") == "" or product_info[0].replace("\"", "") == " ":
                if product_info[1].replace("\"", "") == "" or product_info[1].replace("\"", "") == " ":
                    if debug: print("Failed;No name supplied%s;;" % product_info[0].replace("\"", ""))
                    logfile.write("Failed;No name supplied%s;;\n" % product_info[0].replace("\"", ""))
                    continue
                else:
                    product_info[0] = product_info[1]
                    
            # create product only if needed
            try:
                newProduct = ProductPage.objects.get(slug=product_info[1].replace("\"", "").lower())
                itIsNew = "Updating product"
                product = True
            except:
                newProduct = ProductPage()
                itIsNew = "New Product has been created"
                product = False
            
            if printLine:        
                printLine(product_info)
            
            #try:
            newProduct.name = product_info[0].replace("\r", "").replace("\n", "").replace("\"", "")
            newProduct.slug = product_info[1].replace("\n", "").replace("\r", "").replace("/", "_").replace("\"", "").replace("(", "_").replace(")", "_").lower()
            newProduct.description = product_info[2].replace("_", " ").replace("\"", "")
            newProduct.keywords = product_info[3].replace("_", " ").replace("\"", "")
            newProduct.status = (product_info[4].replace("\"", "") if product_info[4].replace("\"", "") else 0)
            newProduct.language = language
            newProduct.product_description = product_info[5].replace("_", " ").replace("\"", "")
            newProduct.product_id = (product_info[6].replace("\"", "") if product_info[6].replace("\"", "") else 0)
            newProduct.polygon = (int(product_info[7].replace(" ","").replace("\"", "")) if int(product_info[7].replace(" ","").replace("\"", "")) else 0)
            newProduct.texture_format = product_info[8].replace("\"", "")
            newProduct.texture_resolution = (product_info[9].replace("\"", "") if product_info[9].replace("\"", "") else 0)

            # foreign key ->
            try:
                c = product_info[11].replace("\"", "")
                category = Category.objects.filter(name=c)[0]
            except:
                if product_info[11].replace("\"", "") == "":
                    category = Category.objects.get(name="Other")
                else:
                    category = createCategory(product_info[11].replace("\"", ""), "")

            
            newProduct.category = category
            # save before assigning m2m key
            newProduct.save(reorder=False)
            
            # multiple line ->
            #for ff in product_info[16].split(","):
            # newProduct.save()
            # FILEFORMAT
            for fileformat in product_info[12].replace("\"", "").split(','):
                fileformat = fileformat.lower()
                fileformat = fileformat.replace(" ", "")
                try:
                    ff = FileFormat.objects.filter(code=fileformat[:3])[0]
                    #print("Fileformat exist : %s" % fileformat)
                except:
                    ff = createFileFormat(fileformat,fileformat)
                newProduct.file_format = [ff]


            newProduct.save()
            logfile.write("Success;;%s;%s;%s\n" % (newProduct.name, itIsNew, category))
            if debug: print("Success;;%s;%s;%s" % (newProduct.name, itIsNew, category))
    
    toImport.close()
    logfile.close()

def run():
    importCategory()
    importProducts()
