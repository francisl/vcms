# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()
    
from django.contrib.sitemaps import GenericSitemap

#subdir_path = ""

urlpatterns = patterns('',
    # Uncomment this for admin:
    #(r'admin/', include('mptt.admin.urls')),
    (r'^gestion/www/update_menu', 'vimba_cms.apps.www.admin.views.UpdateMenu'),
    (r'^gestion/(.*)', admin.site.root),
)

# __ SIMTHETIQ __
# ordering formular
if 'vimba_cms_simthetiq.apps.order' in settings.INSTALLED_APPS:
    urlpatterns += patterns( '', url(r'^order/', include('vimba_cms_simthetiq.apps.order.urls')),)

# __ SIMTHETIQ __
# For simthetiq product management
if 'vimba_cms_simthetiq.apps.products' in settings.INSTALLED_APPS:
    urlpatterns += patterns( '', url(r'^products/', include('vimba_cms_simthetiq.apps.products.urls')),)
    
        
#print("INSTALLED APPS %s " % settings.INSTALLED_APPS)
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )

# __ CMS __ 
# __ SITEMAP __
# auto sitemap generation
sitemaps = {}
if 'vimba_cms.apps.www' in settings.INSTALLED_APPS:
    try: 
        from www.models import Page
        info_page = {
            'queryset': Page.objects.get_Published(),
            'date_field': 'date_modified'
        }
        sitemaps["pages"] = GenericSitemap(info_page)
    except:
        # no page
        pass

if 'vimba_cms.apps.news' in settings.INSTALLED_APPS:
    urlpatterns += patterns( '', url(r'^news/', include('vimba_cms.apps.news.urls')),)
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

    
#catch all, keep at the end
urlpatterns += patterns('',
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^robots.txt$', 'vimba_cms.apps.www.views.robots'),
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^forms/contact/', 'vimba_cms.apps.www.views.Contact'),
    url(r'^www/', include('vimba_cms.apps.www.urls')),
    # url(r'^afghanistan/', 'www.),
    # CMS, catch every page
    url(r'', include('vimba_cms.apps.www.urls')),
)


if settings.DEBUG:
    import os
    urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.dirname(__file__) + '/../static', 'show_indexes': True}),
)
