# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Template, Context, RequestContext 
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

import inspect # external requirement
from captcha.fields import CaptchaField

from vcms.www.models.page import APP_SLUGS
from vcms.www.models.page import BasicPage as Page
from vcms.www.models.page import BasicPage
from vcms.www.models.menu import CMSMenu


DROPDOWN_MENU = 0
SIMPLE_MENU = 1
MENU_STYLE = ((DROPDOWN_MENU, _('Dropdown')),
              (SIMPLE_MENU, _('Single line')))

def _get_page_parameters(page=None):
    """ Set the default parameter for a CMS page 
        module , menu_style, current_page, page
    """
    page_info = {}
    page_info.update(menu_style = DROPDOWN_MENU)
    page_info.update(data = { 'title': settings.SITE_NAME
                                ,'description':settings.SITE_DESCRIPTION
                                ,'footer':settings.FOOTER_HTML })
    if page:
        page_info.update(module = page.module)
        page_info.update(current_page = page)
        page_info.update(page = page)

    else:
        page_info.update(module = None)
        page_info.update(current_page = None)
        page_info.update(page = None)
    return page_info

def get_requested_page(page_slug, app_slug):
    """ get_requested_page get a page slug and its corresponding app slug then return
        an updated context containing the required information for the CMS pages
    """
    #try:
    # IF NOTHING SELECTED, GO FIRST MENU ON ERROR RAISE 404
    if page_slug == None:
        current_page = CMSMenu.objects.get_default_page()
    else:
        current_page = Page.objects.get_page_or_404(page_slug, app_slug)
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

    if context["page_info"]['page'].module in globals():
        """ Transfert the view specified by the model module name """
        return globals()[context["page_info"]['page'].module](request, context)
    else:
        return Simple(request, context)
    

def MainPage(request, context={}, page_instance=None):
    return render_to_response('mainpage.html',
                              context,
                              context_instance=RequestContext(request))

def simple_page(request, context={}, menu_instance=None):
    return SimplePage(request, context)

def SimplePage(request, context={}):
    return render_to_response('simple.html',
                              context,
                              context_instance=RequestContext(request))
    



def Simple(request, context={}):
    current_page = context["page_info"]['page']
    content = []
    if len(content) == 0 :
        """ When page has no content, it redirect to the first child """
        subpage = Page.objects.get_children() #context["page_info"]['page'])

        if subpage:
            return HttpResponseRedirect("/"+subpage[0].app_slug+"/"+subpage[0].slug)

    return render_to_response('simple.html',
                              context,
                              context_instance=RequestContext(request))
        

def mlogin(request):
    return render_to_response('master.html', {})


def robots(request):
    from django.contrib.sites.models import Site
    try:
        current_site = Site.objects.get(id=settings.SITE_ID)
        site_text = "Sitemap: http://%s/sitemap.xml" % current_site.domain 
    except:
        site_text = ""
    text = "\nUser-agent: * \nDisallow: /media/ \n\n%s" % site_text
    return HttpResponse(text, mimetype="text/plain")


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
                               ,'menu': menu
                               , 'page_info': _get_page_parameters() },
                              context_instance=RequestContext(request))

def cms500(request):
    return render_to_response('500.html'
                              ,{'MEDIA_URL': settings.MEDIA_URL}
                              ,context_instance=RequestContext(request))
