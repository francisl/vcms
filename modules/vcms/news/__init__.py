# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie

from django.conf import settings
# make widget available to cms
settings.PAGE_MODULES.append({ "admin": "vcms.news.admin",
                                "models": "vcms.news.models",
                                "model": 'NewsPageModule',
                                "inline": "NewsPageModuleInline",
                            })

from vcms.www.views import dashboardRegister
dashboardRegister(module="vcms.news.views", function="Preview")
