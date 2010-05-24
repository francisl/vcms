# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: Store
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 12-05-2010.

INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.admindocs',
        'django.contrib.contenttypes',
        'django.contrib.comments',
        'django.contrib.sessions',
        'django.contrib.sitemaps',
        'registration',
        'keyedcache',
        'livesettings',
        'l10n',
        'sorl.thumbnail',
        'tax',
        'tax.modules.no',
        'tax.modules.area',
        'tax.modules.percent',
        'shipping',
        'product',
        'product.modules.configurable',
        'payment',
        'payment.modules.dummy',
        'payment.modules.giftcertificate',
        'satchmo_utils',
        'app_plugins',
        )

#### Satchmo unique variables ####
#from django.conf.urls.defaults import patterns, include
SATCHMO_SETTINGS = {
                    'SHOP_BASE' : '',
                    'MULTISHOP' : False,
                    'SSL'       : False,
                    #'SHOP_URLS' : patterns('satchmo_store.shop.views',)
                    }
