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

replacement = [ url(r'^register/complete/$', 'vcms.store.views.complete', {}, 'registration_complete')
               ,url(r'^register/(?P<activation_key>\w+)/$', 'vcms.store.views.activate', {}, 'registration_activate')
               ] 
urlhelper.replace_urlpatterns( urlpatterns, replacement)

if 'updates_registration' in settings.INSTALLED_APPS: # register2update
    urlpatterns += patterns( '', url(r'^register/', include('updates_registration.urls')),)
    
# __ VIMBA CMS __
urlpatterns += patterns('',
    url(r'^www/', include('vcms.www.urls')),
    url(r'^captcha/', include('captcha.urls')),
)

# __ VIMBA CMS GALLERY __
# ordering formular
if 'vcms.image_gallery' in settings.INSTALLED_APPS:
    urlpatterns += patterns( '', url(r'^gallery/', include('vcms.image_gallery.urls')),)
 
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )

# __ CMS __ 
# __ SITEMAP __
# auto sitemap generation
sitemaps = {}
if 'vcms.www' in settings.INSTALLED_APPS:
    try: 
        from www.models.page import BasicPage
        info_page = {
            'queryset': BasicPage.objects.get_Published(),
            'date_field': 'date_modified'
        }
        sitemaps["pages"] = GenericSitemap(info_page)
    except:
        # no page
        pass

if 'vcms.news' in settings.INSTALLED_APPS:
    urlpatterns += patterns( '', url(r'^news/', include('vcms.news.urls')),)
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

if settings.ENABLE_STATIC:
    import os
    urlpatterns += patterns('',
(r'^googlehostedservice\.html$', 'django.views.static.serve', {'document_root': os.path.dirname(__file__) + '/../client_cms_static/html/googlehostedservice.html', 'show_indexes': True}),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.dirname(__file__) + '/../client_cms_static', 'show_indexes': True}),
    (r'^vcms.client/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.dirname(__file__) + '/../vimba_cms_static/vcms.client', 'show_indexes': True}),
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
    (r'^robots.txt$', 'vcms.www.views.robots'),
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout_then_login'),
    (r'^contact/', include('vcontact.urls')),
    (r'', include('vcms.www.urls')),
)

urlpatterns += patterns('',
    (r'^gestion/style', 'vcms.www.admin.views.show_style'),
    #(r'^gestion/www/update_menu', 'vcms.www.admin.views.UpdateMenu'),
    (r'^gestion/', include(admin.site.urls)),
    (r'^contact/', include('vcontact.urls')),
)
