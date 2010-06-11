# encoding: utf-8
# copyright Vimba inc. 2010
# programmer : Francis Lavoie
# 

import os
DIRNAME = os.path.abspath(os.path.dirname(__file__))
LOCAL_DEV = True

MEDIA_ROOT = os.path.join(DIRNAME, 'static/')
MEDIA_URL = '/static/'

MIDDLEWARE_CLASSES = (
"django.middleware.common.CommonMiddleware",
"django.contrib.sessions.middleware.SessionMiddleware",
"django.middleware.locale.LocaleMiddleware",
"django.contrib.auth.middleware.AuthenticationMiddleware",
"django.middleware.doc.XViewMiddleware",
"threaded_multihost.middleware.ThreadLocalMiddleware",
"satchmo_store.shop.SSLMiddleware.SSLRedirect")

TEMPLATE_DIRS = (os.path.join(DIRNAME, "templates"))
TEMPLATE_CONTEXT_PROCESSORS =     ('satchmo_store.shop.context_processors.settings',
                                 'django.core.context_processors.auth',
                                 )

INSTALLED_APPS = (
        'django.contrib.sites',
        'satchmo_store.shop',
        'django.contrib.admin',
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
        'payment',
        'payment.modules.giftcertificate',
        'satchmo_utils',
        'app_plugins',
        )

AUTHENTICATION_BACKENDS = (
    'satchmo_store.accounts.email-auth.EmailBackend',
    'django.contrib.auth.backends.ModelBackend'
    )

