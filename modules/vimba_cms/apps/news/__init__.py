# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie

from django.conf import settings
# make widget available to cms
settings.PAGE_MODULES.append({ "admin": "vimba_cms.apps.news.admin",
                                "models": "vimba_cms.apps.news.models",
                                "model": 'NewsPageModule',
                                "inline": "NewsPageModuleInline",
                            })

from vimba_cms.apps.www.views import dashboardRegister
dashboardRegister(module="vimba_cms.apps.news.views", function="Preview")
