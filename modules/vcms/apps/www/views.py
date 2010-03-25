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

from vcms.apps.www.models import Page, PageElementPosition, Content, DashboardPage, DashboardElement, DashboardPreview
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
    
def InitPage(page):
    """ InitPage get a page slug and return an updated context with required information for the CMS pages
    
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
        if page == None:
            current_page = Page.objects.get_Default()
            #print("NONE current page = %s" % current_page)
        # When Page IS SELECTED
        else:
            current_page = get_object_or_404(Page, slug=page)
        module = current_page.module
        #debugtrace("Initpage phase 2", current_page, **{'module':module})
        menu_style = DROPDOWN_MENU
        return locals()
    except:
        raise Http404
    
def Generic(request, page=None, context={}):
    context.update(InitPage(page=page))
    print("page ==== %s" % page)
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

    for content in DashboardPreview.objects.filter(page=context['current_page'].id):
        contents[content.preview_position].append((content.preview_display_priority, { "title": content.preview.name, 
                                                                                        "content": content.preview.content, 
                                                                                        "link": content.preview.get_absolute_url()
                                                                                        },))

    context["contents"] = contents
    #news = News.objects.all()
    

    # sorting content
    context["contents"]['left'].sort()
    context["contents"]['right'].sort()

    #debugtrace("Dashboard", context["current_page"],
    #        **{'contents':context['contents']})

    #get the dashboard page
    page = DashboardPage.objects.get(id=context['current_page'].id)
    template = [t for t in DashboardPage.TEMPLATES if t[0] == page.template]

    if page.template == DashboardPage.CONTACT:
        return Contact(request, context)
    #elif page.template == DashboardPage.NEWS:
    #    return News(request, context, as_widget=True)
    else:
        return render_to_response('dashboard.html',  context,
                                context_instance=RequestContext(request))


class ContactForm(forms.Form):
        cie_name = forms.CharField(required=True)
        firstname = forms.CharField(required=True)
        lastname = forms.CharField(required=True)
        phone_number = forms.CharField()
        email = forms.EmailField(required=True)
        email2 = forms.EmailField(required=True)
        message = forms.CharField(widget=forms.Textarea, required=True)
        if EMAILS["CONTACT"]["CAPTCHA"] : captcha = CaptchaField()
    
      
def Contact(request, context={}):
    form = ContactForm()
    requiredfields = ["id_%s" % fieldname for fieldname,fieldobject in form.fields.items() if fieldobject.required]
    completed = False
    if request.method == "POST":
        # Post means it has been sent by the submit buttom, some should have been completed
        form = ContactForm(request.POST)
        if form.is_valid() and form["email"].data == form["email2"].data:
            #Email
            from django.core.mail import send_mail, EmailMultiAlternatives
            #Email to simthetiq
            try:
                subject = 'A message has been send through the contact form'
                email_from = EMAILS["CONTACT"]["FROM"]
                email_to = EMAILS["CONTACT"]["TO"]
                text_content = render_to_response('contact/email_internal.txt', { "orderinfo": form.cleaned_data  })
                html_content = render_to_response('contact/email_internal.html', { "orderinfo": form.cleaned_data  })
                msg = EmailMultiAlternatives(subject, text_content, email_from, [email_to])
                msg.attach_alternative(html_content, "text/html")
                cdr = msg.send()
                #Email to customer
                subject = 'Your message has been sent to Simthetiq'
                email_from = EMAILS["CONTACT"]["FROM"]
                email_to = form.data["email"]
                text_content = render_to_response('contact/email_customer.txt', { "orderinfo": form.cleaned_data  })
                html_content = render_to_response('contact/email_customer.html', { "orderinfo": form.cleaned_data  })
                msg = EmailMultiAlternatives(subject, text_content, email_from, [email_to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                completed = True
            except:
                pass
                completed = False
            
            # return render_to_response('contact.html', { "menuselected":"menu_contact", "form": contactform, "successful": False, "emailerror": True, } )
            context.update(locals())
            return render_to_response('email_confirmation.html', 
                                      context,
                                      context_instance=RequestContext(request))
        
        elif form["email"].data != form["email2"].data: 
            form.errors["email"] = ["Email don't match"]
            form.errors["email2"] = ["Email don't match"]
            
    context.update(locals())
    return render_to_response('contact.html', 
                              context,
                              context_instance=RequestContext(request))


#from django.contrib.sitemaps import Sitemap

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

