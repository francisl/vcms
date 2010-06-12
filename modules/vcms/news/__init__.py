# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie

from django.conf import settings
# make widget available to cms
settings.PAGE_MODULES.append({ "admin": "vcms.apps.news.admin",
                                "models": "vcms.apps.news.models",
                                "model": 'NewsPageModule',
                                "inline": "NewsPageModuleInline",
                            })

from vcms.apps.www.views import dashboardRegister
dashboardRegister(module="vcms.apps.news.views", function="Preview")
