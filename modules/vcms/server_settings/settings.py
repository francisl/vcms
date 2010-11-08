# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie
# 
import os
from django.utils.translation import ugettext_lazy as _

ADMINS = (
    ('support', 'support@vimba.ca')
)

SERVER_PATH = os.path.dirname(os.path.realpath( __file__ ))
MEDIA_PATH = SERVER_PATH + "/../"

#Production
#DEBUG = False
#MEDIA_PATH = SERVER_PATH + "/../../webv2_static"
#developpement
DEBUG = False
TEMPLATE_DEBUG = False
ENABLE_STATIC = False

# ## EMAIL
if DEBUG:
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 1025
DEFAULT_FROM_EMAIL = "noreply@exemple.com"
EMAIL_SUBJECT_PREFIX = ""

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
MEDIA_ROOT = MEDIA_PATH + "/client_cms_static/"

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/adminmedia/'

# ## ###
# ## LOGIN
LOGIN_URL = '/accounts/login/'
#LOGIN_REDIRECT_URL = '/'
# Set of URLs that does not require to be logged in.
# Used by the EnforceLoginMiddleware middleware
#PUBLIC_URLS = (
#    r'admin/',
#    r'login/',
#    r'logout/',
#)

ROOT_URLCONF = 'urls'

AUTHENTICATION_BACKENDS = (
    'satchmo_store.accounts.email-auth.EmailBackend',   # Required by Satchmo
    'django.contrib.auth.backends.ModelBackend'
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'satchmo_store.shop.context_processors.settings',   # Required by Satchmo
    'django.core.context_processors.auth',                  # Must specify this one if we specify a TEMPLATE_CONTEXT_PROCESSORS tuple
    'django.core.context_processors.request',               # Add the request to the context
    'django.core.context_processors.media',                 # Add MEDIA_URL to every RequestContext
#    'django.core.context_processors.debug',
#    'django.core.context_processors.i18n',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    SERVER_PATH + '/templates',
    #os.path.dirname(__file__) + '/www/templates',
)

MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware'
                      # cache system
                      #'django.middleware.cache.UpdateCacheMiddleware',
                      #'django.middleware.cache.FetchFromCacheMiddleware',
                      ,'django.contrib.sessions.middleware.SessionMiddleware'
                      ,"django.middleware.locale.LocaleMiddleware" # Required by Satchmo
                      ,'django.contrib.auth.middleware.AuthenticationMiddleware'
                      ,'django.middleware.doc.XViewMiddleware'
                      #'django.middleware.csrf.CsrfViewMiddleware' __TODO: Disabled since Satchmo 0.9.x doesn't officially support Django > 1.1 and this CSRF protection has been added in 1.2
                      ,'threaded_multihost.middleware.ThreadLocalMiddleware' # Required by Satchmo
                      ,'satchmo_store.shop.SSLMiddleware.SSLRedirect'        # Required by Satchmo
                      #'vcms.www.middleware.EnforceLoginMiddleware',
                      )

INSTALLED_APPS = ('django.contrib.sites'
                  ,'satchmo_store.shop' # Satchmo, must preceed django.contrib.admin
                  ,'django.contrib.admin'
                  ,'django.contrib.auth'
                  ,'django.contrib.contenttypes'
                  ,'django.contrib.sessions'
                  ,'django.contrib.sitemaps'
                  ,'django.contrib.humanize'
                  #'tagging'
                  ,'django_extensions'
                  ,'easy_thumbnails'
                  ,'haystack'
                  ,'treebeard'
                  #'rosetta'
                  ,'mptt'
                  ,'captcha'                              # http://code.google.com/p/django-simple-captcha/
                  ,'registration'                         # http://bitbucket.org/ubernostrum/django-registration/
                  ,'l10n'
                  # ## DJVIDEO
                  # djvideo_link | http://git.participatoryculture.org/djvideo/
                  # djanvideo_file | git clone http://git.participatoryculture.org/djvideo/
                  ,'djvideo'
                  ,'compressor'                           # git://github.com/dziegler/django-css.git
                  # VIMBA CMS APPS
                  ,'vcms.www'
                  ,'vcms.simpleblogs'
                  #,'vcms.simplenews'
                  ,'hwm'
                  ,'vcms.themes'
                  ,'vcontact'
                  ,'updates_registration'
                  ,'vcms.store'
                  # Custom apps for cms
                  ,'vimba_cms_simthetiq.apps.order'
                  ,'vimba_cms_simthetiq.apps.store'
                  ,'vimba_cms_simthetiq.apps.products'
                  ,'vimba_cms_simthetiq.apps.importer'
                  ,'south'
                  #SATCHMO
                  ,'satchmo_store.contact'
                  ,'product'
                  ,'payment'
                  ,'payment.modules.dummy'
                  ,'payment.modules.giftcertificate'
                  ,'satchmo_utils'
                  ,'app_plugins'
                  ,'vimba_cms_simthetiq.widget.simthetiq_recommends'
                  )

# ## ###
# sorl-thumbnail config option
THUMBNAIL_DEBUG = False

# ----------------------------
# use to load dashboard module/widget dynamically
PAGE_MODULES = []

# OPTIMISATION
# CACHE 
#CACHE_BACKEND = 'db://cms_opt_cache'
#CACHE_MIDDLEWARE_SECONDS = 30
#CACHE_MIDDLEWARE_KEY_PREFIX = ""
CACHE_TIMEOUT = 10

# ## ###
# ## CAPTCHA CONFIGURATION
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.random_char_challenge'
CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_dots',)

# ## ###
# ## COMPRESSOR (JS/CSS)
COMPRESS = True
COMPILER_FORMATS = {
    '.sass': {
        'binary_path':'sass',
        'arguments': '*.sass *.css'
    },
    '.ccss': {
        'binary_path':'clevercss',
        'arguments': '*.ccss'
    },
}

# ## ###
# ## LOAD LOCAL SETTING
# ## DEBUG
if DEBUG:
    from config_sqlite.debug import *
    if DEBUG_INSTALLED_APPS: 
        INSTALLED_APPS += DEBUG_INSTALLED_APPS
        MIDDLEWARE_CLASSES += DEBUG_MIDDLEWARE_CLASSES

# ## SEARCH ENGINE
from config_sqlite.search_engine import *
if SEARCH_ENGINE:
    INSTALLED_APPS += (SEARCH_ENGINE,)

# ## SATCHMO
#from config_sqlite.satchmo import *

# Import applicaton-specific settings
def get_all_installed_apps(apps_base_name, installed_apps, module_name, modules_set=set()):
    """Gives the list of installed apps recursively, looking in every
    app's INSTALLED_APPS setting from their respective settings module."""
    for app in installed_apps:
        if app.startswith(apps_base_name):
            try:
                app_module = __import__(app, globals(), locals(), [module_name])
                app_settings = getattr(app_module, module_name, None)
                # Do not traverse through apps that have already been processed
                if app_module.__name__ not in modules_set:
                    if hasattr(app_settings, "INSTALLED_APPS"):
                        value = getattr(app_settings, "INSTALLED_APPS")
                        # Recursively go through every installed apps if they aren't already in modules_set
                        modules_set.update(get_all_installed_apps(apps_base_name, value, module_name, modules_set))
                        # Add the current app after recursively going into its dependencies to save us from infinite recursion
                        modules_set.update(value)
                        modules_set.add(app)
            except ImportError:
                pass
    return modules_set

APPS_BASE_NAME = 'vcms'
SETTINGS_MODULE = 'settings'

INSTALLED_APPS += tuple(get_all_installed_apps(APPS_BASE_NAME, INSTALLED_APPS, SETTINGS_MODULE))

# Import the settings of every app into this module
for app in INSTALLED_APPS:
    if app.startswith(APPS_BASE_NAME):
        try:
            app_module = __import__(app, globals(), locals(), [SETTINGS_MODULE])
            app_settings = getattr(app_module, SETTINGS_MODULE, None)
            for setting in dir(app_settings):
                if setting == setting.upper():
                    value = getattr(app_settings, setting)
                    if isinstance(value, tuple):
                        locals()[setting] += value
                    else:
                        locals()[setting] = value
        except ImportError:
            pass

if DEBUG:
    #import socket
    #if socket.gethostname() == "LAPTOP": # Francois
    DEBUG_TOOLBAR_CONFIG = { "INTERCEPT_REDIRECTS": False } # This really grinds my gears!

# THEME
from config.theme import *

# Load the local Satchmo settings
from config_sqlite.satchmo_local import *

# Custom settings for apps
from config_sqlite.settings import *

