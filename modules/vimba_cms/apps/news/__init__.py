# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie

from django.conf import settings

settings.PAGE_MODULES.append({ "module": "news.admin",
                                "object": "NewsPageModuleInline",
                                "requirements": [{'module':'news.models',
                                                'object': 'NewsPageModule'},],
                                })

from vimba_cms.apps.www.views import dashboardRegister
dashboardRegister(module="vimba_cms.apps.news.views", function="Preview")
