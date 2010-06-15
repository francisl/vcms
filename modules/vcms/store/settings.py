# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: Store
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 12-05-2010.

#import os
#DIRNAME = os.path.abspath(os.path.dirname(__file__))

INSTALLED_APPS = (
                  'django.contrib.sites'
                  ,'django.contrib.auth'
                  ,'django.contrib.admindocs'
                  ,'django.contrib.contenttypes'
                  ,'django.contrib.comments'
                  ,'django.contrib.sessions'
                  ,'django.contrib.sitemaps'
                  ,'registration'
                  ,'keyedcache'
                  ,'livesettings'
                  ,'l10n'
                  ,'sorl.thumbnail'
                  ,'tax'
                  ,'tax.modules.no'
                  ,'tax.modules.area'
                  ,'tax.modules.percent'
                  ,'shipping'
                  ,'product'
                  ,'product.modules.configurable'
                  ,'payment'
                  ,'payment.modules.dummy'
                  ,'payment.modules.giftcertificate'
                  ,'satchmo_utils'
                  ,'app_plugins'
        )

#TEMPLATE_DIRS = (os.path.join(DIRNAME, "templates"))
#TEMPLATE_CONTEXT_PROCESSORS =     ('satchmo_store.shop.context_processors.settings',
#                                 'django.core.context_processors.auth',
#                                 )
