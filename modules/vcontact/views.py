# encoding: utf-8
# copyright Vimba inc. 2010
# programmer : Francis Lavoie

from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext 
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings

# from other aps
from vcontact.models import ContactPage
from vcms.www.models import Content
from vcms.www.views import get_requested_page

# external requirement
from captcha.fields import CaptchaField

class ContactForm(forms.Form):
    firstname = forms.CharField(required=True)
    lastname = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    cie_name = forms.CharField(required=False)
    message = forms.CharField(widget=forms.Textarea, required=True)
    if settings.EMAILS["CONTACT"]["CAPTCHA"] : captcha = CaptchaField()


def Contact(request, page=None, context={}):
    context.update(current_page=get_requested_page(page_slug=page, app_slug='contact'))
    context.update(locals())
    #contact_page = ContactPage.objects.get(slug=context["page_info"]['page'].slug)
    form = ContactForm()
    
    requiredfields = ["id_%s" % fieldname for fieldname,fieldobject in form.fields.items() if fieldobject.required]
    completed = False
    if request.method == "POST":
        # Post means it has been sent by the submit buttom, some should have been completed
        form = ContactForm(request.POST)
        
        if form.is_valid():
        #Email to simthetiq
            try:
                subject = 'A message has been send through the contact form'
                email_from = settings.EMAILS["CONTACT"]["FROM"]
                email_to = settings.EMAILS["CONTACT"]["TO"]
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
                html_content = render_to_response('contact/email_customer.html', { "orderinfo": form.cleaned_data, "email_for_removal":email_from  })
                msg = EmailMultiAlternatives(subject, text_content, email_from, [email_to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                completed = True
            except:
                pass
                completed = False

            # return render_to_response('contact.html', { "menuselected":"menu_contact", "form": contactform, "successful": False, "emailerror": True, } )
            context.update(locals())
            return render_to_response('confirmation.html', 
                                      context,
                                      context_instance=RequestContext(request))
                
    #contents = Content.objects.get_contents_for_page(context["page_info"]['page'])
    #print("content for contant page %s : %s" % (context["page_info"]['page'], contents))
            
    context.update(locals())
    return render_to_response('contact.html', 
                              context,
                              context_instance=RequestContext(request))

