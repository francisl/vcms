# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie
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
DATABASE_NAME = './database/djangodata'    # Or path to database file if using sqlite3.
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
MEDIA_ROOT = os.path.dirname(__file__) + "/../client_cms_static/"
#VIMBA_CMS_MEDIA_ROOT = os.path.dirname(__file__) + "/../vimba_cms_static/"

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'
#VIMBA_CMS_MEDIA_URL = '/static/'
#THEME = "Simthetiq"

#TEMPLATE_CONTEXT_PROCESSORS = ('django.core.context_processors.auth',
#        'django.core.context_processors.debug',
#        'django.core.context_processors.i18n',
#        'django.core.context_processors.media'
#) 

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/adminmedia/'

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
    'vcms.middleware.EnforceLoginMiddleware',
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
    'django_extensions',
    'sorl.thumbnail',
    'rosetta',
    'djapian',
    'mptt',
    'captcha',              # http://code.google.com/p/django-simple-captcha/
    # VIMBA CMS APPS
    'vcms.apps.www',
    'vcms.apps.news',
    'vcms.apps.themes',
    # Custom apps for cms
    'vimba_cms_simthetiq.apps.order',
    'vimba_cms_simthetiq.apps.products',
    'vimba_cms_simthetiq.apps.importer',
)

# ----------------------------
# sorl-thumbnail config option
THUMBNAIL_DEBUG = False

# ----------------------------
# use to load dashboard module/widget dynamically
PAGE_MODULES = []

# ----------------------------
if DEBUG:
    import settings_debug

# OPTIMISATION
# CACHE 
#CACHE_BACKEND = 'db://cms_opt_cache'
#CACHE_MIDDLEWARE_SECONDS = 30
#CACHE_MIDDLEWARE_KEY_PREFIX = ""

CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.random_char_challenge'
CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_dots',)


# CHANGE THIS ----------------------------------------------------
EMAIL_HOST='smtp.webfaction.com'
EMAIL_PORT=25   
EMAIL_HOST_USER='simthetiq_noreply'
EMAIL_HOST_PASSWORD='cfd6d14a'
# secure
#EMAIL_PORT=465
EMAIL_USE_TLS=False
