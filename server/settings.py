# encoding: utf-8
# Django settings for simthetiq project.
# 
import os
from django.utils.translation import ugettext_lazy as _
#Production
#SITEPATH = sys.path[0] + "/simthetiq"
#DEBUG = False
#developpement
#SITEPATH = sys.path[0]
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('simthetiq support', 'support@simthetiq.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'                 # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = '../database/djangodata'    # Or path to database file if using sqlite3.
DATABASE_USER = ''                          # Not used with sqlite3.
DATABASE_PASSWORD = ''                      # Not used with sqlite3.
DATABASE_HOST = ''                          # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''                          # Set to empty string for default. Not used with sqlite3.

DJAPIAN_DATABASE_PATH = os.path.dirname(__file__) + "/../database"

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be avilable on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Montreal'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'
DEFAULT_LANGUAGE = 0

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.dirname(__file__) + "/../static/"

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/'

#TEMPLATE_CONTEXT_PROCESSORS = ('django.core.context_processors.auth',
#        'django.core.context_processors.debug',
#        'django.core.context_processors.i18n',
#        'django.core.context_processors.media'
#) 

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ')z=ki#(2ki!o7*@3-+9vrae)tq6^v(8#d)k76eo26%hz6v)nke'

# LOGIN
LOGIN_URL = '/login/'

#LOGIN_REDIRECT_URL = '/'
# Set of URLs that does not require to be logged in.
# Used by the EnforceLoginMiddleware middleware
PUBLIC_URLS = (
    r'admin/',
    r'login/',
    r'logout/',
)

ROOT_URLCONF = 'server.urls'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    # cache system
    #'django.middleware.cache.UpdateCacheMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'vimba_cms.middleware.EnforceLoginMiddleware',
)


TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.dirname(__file__) + '/templates',
    #os.path.dirname(__file__) + '/www/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.admin',
    'django.contrib.humanize',
    #'tagging',
    'sorl.thumbnail',
    'rosetta',
    'djapian',
    'mptt',
    # VIMBA CMS APPS
    'vimba_cms.apps.www',
    'vimba_cms.apps.news',
    # Custom apps for cms
    'vimba_cms_simthetiq.apps.order',
    'vimba_cms_simthetiq.apps.products',
)

# use to load dashboard module dynamically
PAGE_MODULES = []

if DEBUG:
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

# OPTIMISATION
# CACHE 
#CACHE_BACKEND = 'db://cms_opt_cache'
#CACHE_MIDDLEWARE_SECONDS = 30
#CACHE_MIDDLEWARE_KEY_PREFIX = ""


# CHANGE THIS ----------------------------------------------------
EMAIL_HOST='smtp.webfaction.com'
EMAIL_PORT=25   
EMAIL_HOST_USER='simthetiq_noreply'
EMAIL_HOST_PASSWORD='cfd6d14a'
# secure
#EMAIL_PORT=465
EMAIL_USE_TLS=False
