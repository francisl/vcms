# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Template, Context, RequestContext 
from django import forms
from django.utils.translation import ugettext_lazy as _

import inspect
# external requirement
from captcha.fields import CaptchaField

from vcms.www.models import PageElementPosition
from vcms.www.models.old import Content, APP_SLUGS
from vcms.www.models.page import BasicPage as Page
from vcms.www.models.page import BasicPage
from vcms.www.models.menu import CMSMenu
from vcms.www.models.page import DashboardPage
from vcms.www.models.page import DashboardElement
from vcms.www.models.page import DashboardPreview
from django.core.exceptions import ObjectDoesNotExist

DROPDOWN_MENU = 0
SIMPLE_MENU = 1
MENU_STYLE = ((DROPDOWN_MENU, _('Dropdown')),
              (SIMPLE_MENU, _('Single line')))

def debugtrace(view, current_page, **argd):
    print("------------- %s -------------" % view)
    print("Current page = %s" % current_page)

    for v in argd:
        print("%s : %s" % (v,argd[v]))

def _get_page_parameters(page=None):
    """ Set the default parameter for a CMS page 
        module , menu_style, current_page, page
    """
    page_info = {}
    if page:
        page_info.update(module = page.module)
        page_info.update(menu_style = DROPDOWN_MENU)
        page_info.update(current_page = page)
        page_info.update(page = page)
    else:
        page_info.update(module = None)
        page_info.update(menu_style = DROPDOWN_MENU)
        page_info.update(current_page = None)
        page_info.update(page = None)
    return page_info

#def get_requested_page(page_slug, app_slug):
def get_requested_page(page_slug, app_slug):
    """ get_requested_page get a page slug and its corresponding app slug then return
        an updated context containing the required information for the CMS pages
    """
    #debugtrace("get_requested_page - entry", page_slug)

    #try:
    # IF NOTHING SELECTED, GO FIRST MENU ON ERROR RAISE 404
    if page_slug == None:
        current_page = CMSMenu.objects.get_default_page()
    # When Page slug i
    else:
        current_page = get_object_or_404(BasicPage, slug=page_slug, app_slug=app_slug)
    #except:
    #    raise Http404
    #return _get_page_parameters(current_page)
    return current_page

def _get_page_instance(page):
    return getattr(page, page.module.lower())

def _get_page_containers(page):
    return page.get_containers()

def Generic(request, page=None, context={}):
    basic_page = get_requested_page(page_slug=page, app_slug=APP_SLUGS)
    page_instance = _get_page_instance(basic_page)
    context.update(page_info=_get_page_parameters(page_instance))
    context.update(containers=_get_page_containers(page_instance))

    if context["page_info"]['page'].module in globals():
        """ Transfert the view specified by the model module name """
        #debugtrace("Generic in Globals", context["page_info"]['page'], **{'module':context["module"]})
        return globals()[context["page_info"]['page'].module](request, context)
    else:
        return Simple(request, context)
    

def MainPage(request, context={}):
    context.update(context["containers"])
    return render_to_response('mainpage.html',
                              context,
                              context_instance=RequestContext(request))

def SimplePage(request, context={}):
    from vcms.www.models.widget import RelativeWidgetWrapper
    content_container = context["containers"]["Content"]
    ContentWidgets = RelativeWidgetWrapper.objects.filter(container=content_container)
    context.update(content_widgets = ContentWidgets)

    #import treebeard
    
    #form = treebeard.forms()
    #context.update(form=form)
    return render_to_response('simple.html',
                              context,
                              context_instance=RequestContext(request))
    
        
    
def Simple(request, context={}):
    current_page = context["page_info"]['page']
    #context['contents'] = Content.objects.filter(page=current_page)
    #debugtrace("basic", context["page_info"]['page'], **{'basic content':context['contents']})

    content = []
    #content = Content.objects.filter(page=context["page_info"]['page'].id)
    if len(content) == 0 :
        """ When page has no content, it redirect to the first child """
        subpage = Page.objects.get_children() #context["page_info"]['page'])

        if subpage:
            #debugtrace("Generic", context["page_info"]['page'],
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

        
def Dashboard(request, context={}):
    """
        Display a page with preview from other pages, summary, widgets or forms
    """
    #debugtrace("Dashboard", context["page_info"]['page'].id)
    
    contents = { 'left': [], 'right': [] }
    # load all modules that are registered at startup
    for mod in DASHBOARD_MODULES:
        for content in mod(request, pageid=context["page_info"]['page'].id):
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

    #debugtrace("Dashboard", context["page_info"]['page'],
    #        **{'contents':context['contents']})

    #get the dashboard page
    page = DashboardPage.objects.get(id=context['current_page'].id)
    template = [t for t in DashboardPage.TEMPLATES if t[0] == page.template]

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
        print("results = %s" % results)
        try:
            # get result from product
            from products.models import ProductInformation
            results[_("Product")] = ProductInformation.indexer.search(query)
        except:
            # no products
            pass
                    
        return render_to_response('search/search_simple.html', 
                                  {'query': query, 'results': results },
                                  context_instance=RequestContext(request))

def robots(request):
    response = HttpResponse("User-agent: * \nDisallow: /", mimetype="text/plain")
    return response


from django.contrib.admin.views.decorators import staff_member_required
@staff_member_required
def testCMSMenuForm(request, menuid):
    from django.http import HttpResponseRedirect
    from vcms.www.models.menu import CMSMenu
    from mptt.exceptions import InvalidMove
    from mptt.forms import MoveNodeForm
    from django.conf import settings

    menu = get_object_or_404(CMSMenu, id=menuid)
    if request.method == 'POST':
        form = MoveNodeForm(menu, request.POST, valid_targets=CMSMenu.objects.all())
        if form.is_valid():
            try:
                menu = form.save()
            except InvalidMove:
                pass
    else:
        form = MoveNodeForm(menu)

    return render_to_response('testmovemenu.html',
                              {'form': form
                               ,'menu': menu },
                              context_instance=RequestContext(request))

