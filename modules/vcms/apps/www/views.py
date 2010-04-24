# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Template, Context, RequestContext 
from django import forms
from django.utils.translation import ugettext_lazy as _

# external requirement
from captcha.fields import CaptchaField

from vcms.apps.www.models import Page, PageElementPosition, Content, DashboardPage, DashboardElement, DashboardPreview, APP_SLUGS
from config.email import EMAILS 

DROPDOWN_MENU = 0
SIMPLE_MENU = 1
MENU_STYLE = ((DROPDOWN_MENU, _('Dropdown')),
              (SIMPLE_MENU, _('Single line')))

def debugtrace(view, current_page, **argd):
    print("------------- %s -------------" % view)
    print("Current page = %s" % current_page)

    for v in argd:
        print("%s : %s" % (v,argd[v]))


def setPageParameters(page=None):
    if page:
        module = page.module
        menu_style = DROPDOWN_MENU
        current_page = page
    else:
        module = None
        menu_style = DROPDOWN_MENU
        current_page = None
        page = None
    return locals()

def InitPage(page_slug, app_slug):
    """ InitPage get a page slug and its corresponding app slug then return
        an updated context containing the required information for the CMS pages
    
        returns: 
            current_page : Page instance that is currently request
            module : Page instance modules or function to call in the Views, 
                    it use reflection to execute the appropriate views function
            menu_style : Style used to display the menu in the master template
    """
    
    #debugtrace("Initpage", page)
    
    try:
        # IF NOTHING SELECTED, GO FIRST MENU
        # ON ERROR RAISE 404
        if page_slug == None:
            current_page = Page.objects.get_Default()
        # When Page slug i
        else:
            current_page = get_object_or_404(Page, slug=page_slug, app_slug=app_slug)
        print("set -- %s" % setPageParameters(current_page))
        context = setPageParameters(current_page)
        return context 
    except:
        print("get default %s" % "error")
        raise Http404
    
def Generic(request, page=None, context={}):
    context.update(InitPage(page_slug=page, app_slug=APP_SLUGS))
    context.update(locals())
    
    if context["module"] in globals():
        """ Transfert the view specified by the model module name """
        #debugtrace("Generic in Globals", context["current_page"], **{'module':context["module"]})
        return globals()[context["module"]](request, context)
    else:
        return Simple(request, context)
    

def Simple(request, context={}):
    context['contents'] = Content.objects.filter(page=context['current_page'])
    #debugtrace("basic", context["current_page"], **{'basic content':context['contents']})

    content = Content.objects.filter(page=context["current_page"].id)
    if len(content) == 0 :
        """ When page has no content, it redirect to the first child """
        subpage = Page.objects.get_PageFirstChild(context["current_page"])

        if subpage:
            #debugtrace("Generic", context["current_page"],
            #        **{'len content': len(content), 'First subpage': subpage[0].slug})
            return HttpResponseRedirect("/"+subpage[0].app_slug+"/"+subpage[0].slug)

    return render_to_response('simple.html',
                              context,
                              context_instance=RequestContext(request))

# Register Loading optionnal plugins
DASHBOARD_MODULES = []
def dashboardRegister(module, function):
    try:
        # loading requirements first
        mod = __import__(module, globals(), locals(), [function])
        html_function = getattr(mod,function) 
        DASHBOARD_MODULES.append(html_function)
    except:
        pass
    #    #print("modules exception : %s" % module)

        
def Dashboard(request, context={}):
    """
        Display a page with preview from other pages, summary, widgets or forms
    """
    #debugtrace("Dashboard", context["current_page"].id)
    
    contents = { 'left': [], 'right': [] }
    # load all modules that are registered at startup
    for mod in DASHBOARD_MODULES:
        for content in mod(request, pageid=context["current_page"].id):
            contents[content["preview_position"]].append((content["preview_display_priority"], { "module": content["preview_content"]},))

    for content in DashboardElement.objects.get_Published(context['current_page']):
        contents[content.preview_position].append((content.preview_display_priority, 
                                                    { "title": content.name, 
                                                        "content": content.text,
                                                        "link": content.link},
                                                    ))

    for content in DashboardPreview.objects.filter(page=context['current_page']):
        contents[content.preview_position].append((content.preview_display_priority, 
                                                   { "title": content.preview.name,
                                                    "content": content.preview.content, 
                                                    "link": content.preview.get_absolute_url()},
                                                    ))

    context["contents"] = contents
    
    # sorting content
    context["contents"]['left'].sort()
    context["contents"]['right'].sort()

    #debugtrace("Dashboard", context["current_page"],
    #        **{'contents':context['contents']})

    #get the dashboard page
    page = DashboardPage.objects.get(id=context['current_page'].id)
    template = [t for t in DashboardPage.TEMPLATES if t[0] == page.template]

    print page.template
    return render_to_response(DashboardPage.TEMPLATE_FILES[page.template],  context,
                                context_instance=RequestContext(request))


def mlogin(request):
    return render_to_response('master.html', {})

def Search(request):
    if request.method == "GET":
        query = ''.join(request.GET.get('query'))
        results = {}

        # temp_results
        results[_("Page")] = Page.indexer.search(query)

        try:
            # get result from product
            from products.models import ProductInformation
            results[_("Product")] = ProductInformation.indexer.search(query)
        except:
            # no products
            pass
                    
        return render_to_response('search.html', 
                                  {'query': query, 'results': results },
                                  context_instance=RequestContext(request))

def robots(request):
    response = HttpResponse("User-agent: * \nDisallow: /", mimetype="text/plain")
    return response

