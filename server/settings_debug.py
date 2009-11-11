# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie


# Adding django debug toolbar if available
try:
    import debug_toolbar
    #INSTALLED_APPS += ('debug_toolbar',)
    #MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    #INTERNAL_IPS = ('127.0.0.1',)
except:
    pass

# Adding django command extension if available

try:
    import django_extensions
    INSTALLED_APPS += ('django_extensions',)
except:
    #print("no extensions!")
    pass

