# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()
    
from django.contrib.sitemaps import GenericSitemap

#subdir_path = ""

# Import Satchmo URLs
from satchmo_store.urls import urlpatterns

# Set a specific django-registration backend for the client
# __TODO: This should be located in a client-specific configuration file
from livesettings import config_value
from satchmo_utils import urlhelper
urlhelper.replace_urlpatterns(
    urlpatterns,
    [
        url(r'^register/complete/$', 'vcms.apps.store.views.complete', {}, 'registration_complete'),
        url(r'^register/(?P<activation_key>\w+)/$', 'vcms.apps.store.views.activate', {}, 'registration_activate'),
        url(r'^register/$', 'vcms.apps.store.views.register', {}, 'registration_register'),
    ]
)

urlpatterns += patterns('',
    # Uncomment this for admin:
    #(r'admin/', include('mptt.admin.urls')),
    (r'^gestion/www/update_menu', 'vcms.apps.www.admin.views.UpdateMenu'),
    (r'^gestion/', include(admin.site.urls)),
)

# __ VIMBA CMS __
urlpatterns += patterns('',
    url(r'^captcha/', include('captcha.urls')),
)

# __ SIMTHETIQ __
# ordering formular
if 'vimba_cms_simthetiq.apps.order' in settings.INSTALLED_APPS:
    urlpatterns += patterns( '', url(r'^order/', include('vimba_cms_simthetiq.apps.order.urls')),)

# __ SIMTHETIQ __
# For simthetiq product management
if 'vimba_cms_simthetiq.apps.products' in settings.INSTALLED_APPS:
    urlpatterns += patterns( '', url(r'^products/', include('vimba_cms_simthetiq.apps.products.urls')),)

# __ SIMTHETIQ __
# For simthetiq importer
if 'vimba_cms_simthetiq.apps.importer' in settings.INSTALLED_APPS:
    urlpatterns += patterns( '', url(r'^importer/', include('vimba_cms_simthetiq.apps.importer.urls')),)
   
        
#print("INSTALLED APPS %s " % settings.INSTALLED_APPS)
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )

# __ CMS __ 
# __ SITEMAP __
# auto sitemap generation
sitemaps = {}
if 'vcms.apps.www' in settings.INSTALLED_APPS:
    try: 
        from www.models.page import Page
        info_page = {
            'queryset': Page.objects.get_Published(),
            'date_field': 'date_modified'
        }
        sitemaps["pages"] = GenericSitemap(info_page)
    except:
        # no page
        pass

if 'vcms.apps.news' in settings.INSTALLED_APPS:
    urlpatterns += patterns( '', url(r'^news/', include('vcms.apps.news.urls')),)
    try:
        from news.models import News
        info_news = {
            'queryset': News.objects.all(),
            'date_field': 'date'
        }
        sitemaps["news"] = GenericSitemap(info_news)
    except:
        # now news module availlable
        pass

if settings.DEBUG:
    import os
    urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.dirname(__file__) + '/../client_cms_static', 'show_indexes': True}),
)

# Import applicaton-specific urls
for app in settings.INSTALLED_APPS:
    if app.startswith(settings.APPS_BASE_NAME):
        try:
            app_module = __import__(app, globals(), locals(), ["urls"])
            if hasattr(app_module, "urls"):
                app_urls = getattr(app_module, "urls", None)
                if hasattr(app_urls, "urlpatterns"):
                    app_urlpatterns = getattr(app_urls, "urlpatterns")
                    app_urlpatterns_prefix = getattr(app_urls, "urlpatterns_prefix", "") # If no urlpattern prefix is specified, then have the URLs begin at the root
                    urlpatterns += patterns(app_urlpatterns[0], (app_urlpatterns_prefix, include(app_urls)))
        except ImportError:
            pass

#catch all, keep at the end
urlpatterns += patterns('',
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^robots.txt$', 'vcms.apps.www.views.robots'),
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout_then_login'),
    #url(r'^forms/contact/', 'vcms.apps.www.views.Contact'),
    url(r'^contact/', include('vcms.apps.contact.urls')),
    # url(r'^afghanistan/', 'www.),
    # CMS, catch every page
    #(r'^tinymce/', include('tinymce.urls')),
    url(r'^www/', include('vcms.apps.www.urls')),
    url(r'', include('vcms.apps.www.urls')),
)
