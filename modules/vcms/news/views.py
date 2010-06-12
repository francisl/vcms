# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie
from django.http import HttpResponseRedirect
#from django.http import Http404
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
#from django.template import Context, 
from django.template import RequestContext
#from django.template import loader

from vcms.news.models import APP_SLUGS
from vcms.news.models import News as m_News
from vcms.news.models import NewsPage as m_NewsPage
from vcms.news.models import NewsPageModule as m_NewsPageModule

from vcms.www.views import InitPage

def Generic(request, page=None, slug=None, context={}):
    context.update(InitPage(page_slug=page, app_slug=APP_SLUGS))
    context.update(locals())
    
    if context["module"] in globals():
        return globals()[context["module"]](request, context)
    else:
        return HttpResponseRedirect("/")

def News(request, context, as_widget=False, page=None, category="all", template='news.html'):
    #debugtrace("News", context["current_page"])
    #print("CATEGORY = %s" % category)
    #print("CATEGORIES = %s" % categories)
    #context['news']= m_News.objects.all()
    if as_widget:
        if category == "all":
            context['news'] = m_News.objects.all()[:3]
        else:
            context['news'] = m_News.objects.filter(categories__in=category)[:3]
            
        template= 'news_dashboard.html'
        #print("as widget contxt = %s" % context['news'])
    else:
        # take the news page and get all the categories it should display
        page = m_NewsPage.objects.get(id=context['current_page'].id)
        categories = [p.id for p in page.categories.all()]
        context['news'] = m_News.objects.filter(categories__in=categories)
        #print("no widget contxt = %s" % context['news'])

    return render_to_response(template,
                              context, context_instance=RequestContext(request))

def NewsSingle(request, id, template='news.html'):
    #debugtrace("NewsSingle", context["current_page"])
    news= m_News.objects.filter(id=id)
    return render_to_response(template,
                              {'news':news}, context_instance=RequestContext(request))

def Preview(request, pageid=None):
    modules = []
    news_modules = m_NewsPageModule.objects.filter(page=pageid)
    for module in news_modules:
        news_categories = module.categories.all()
        news = m_News.objects.filter(categories__in=news_categories)[:3]
        context = {"news": news,
                   "title": module.title,
                   "images": module.show_image_preview, 
                   "videos": module.show_video_preview,
                  }

        html_content = render_to_string("news_module.html", context, context_instance=RequestContext(request))
        modules.append({"preview_display_priority" : module.preview_display_priority,
                        "preview_position" : module.preview_position,
                        "preview_content": html_content
                        })
        
    return modules
    