# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie
# 
import os
from django.utils.translation import ugettext_lazy as _

SERVER_PATH = os.path.dirname(os.path.realpath( __file__ ))
MEDIA_PATH = SERVER_PATH + "/../"
#Production
#DEBUG = False
#MEDIA_PATH = SERVER_PATH + "/../../webv2_static"
#developpement
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# ## EMAIL
from config.email import *

# ## DATABASE
from config.database import *

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

# Make this unique, and don't share it with anybody.
SECRET_KEY = ')z=ki#(2ki!o7*@3-+9vrae)tq6^v(8#d)k76eo26%hz6v)nke'

# ## ###
# ## LOGIN
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

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',   # Add the request to the context
    'django.core.context_processors.media',     # Add MEDIA_URL to every RequestContext
    'django.core.context_processors.auth',      # Must specify this one if we specify a TEMPLATE_CONTEXT_PROCESSORS tuple
#    'django.core.context_processors.debug',
#    'django.core.context_processors.i18n',
)


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
    'django.middleware.csrf.CsrfViewMiddleware',
    'vcms.apps.www.middleware.EnforceLoginMiddleware',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    SERVER_PATH + '/templates',
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
    #'rosetta',       
    'mptt',
    'captcha',                              # http://code.google.com/p/django-simple-captcha/
    'registration',                         # http://bitbucket.org/ubernostrum/django-registration/
    'l10n',                                 
    # ## DJVIDEO
    # djvideo_link | http://git.participatoryculture.org/djvideo/
    # djanvideo_file | git clone http://git.participatoryculture.org/djvideo/
    'djvideo',                           
    'compressor',                           # git://github.com/dziegler/django-css.git
    'clevercss',                            # http://github.com/dziegler/clevercss                   
    # VIMBA CMS APPS
    'vcms.apps.www',
    'vcms.apps.simpleblogs',
    'vcms.apps.simplenews',
    'vcms.apps.themes',
    'vcms.apps.contact',
    # Custom apps for cms
    'vimba_cms_simthetiq.apps.order',
    'vimba_cms_simthetiq.apps.products',
    'vimba_cms_simthetiq.apps.importer',
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
    from config.debug import *
    if DEBUG_INSTALLED_APPS: 
        INSTALLED_APPS += DEBUG_INSTALLED_APPS
        MIDDLEWARE_CLASSES += DEBUG_MIDDLEWARE_CLASSES

# ## SEARCH ENGINE
from config.search_engine import *
if SEARCH_ENGINE:
    INSTALLED_APPS += (SEARCH_ENGINE,)

# ## SATCHMO
#from config.satchmo import *

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
    import socket
    if socket.gethostname() == "LAPTOP": # Francois
        DEBUG_TOOLBAR_CONFIG = { "INTERCEPT_REDIRECTS": False } # This really grinds my gears!
