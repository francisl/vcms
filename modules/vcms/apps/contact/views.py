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

# from other aps
from vcms.apps.www.model import Content
from vcms.apps.www.urls import InitPage

# external requirement
from config.email import EMAILS 
from captcha.fields import CaptchaField

class ContactForm(forms.Form):
        cie_name = forms.CharField(required=True)
        firstname = forms.CharField(required=True)
        lastname = forms.CharField(required=True)
        phone_number = forms.CharField()
        email = forms.EmailField(required=True)
        email2 = forms.EmailField(required=True)
        message = forms.CharField(widget=forms.Textarea, required=True)
        if EMAILS["CONTACT"]["CAPTCHA"] : captcha = CaptchaField()


def Contact(request, page=None, context={}):
    context.update(InitPage(page=page))
    context.update(locals())
    context["current_page"]
    
    requiredfields = ["id_%s" % fieldname for fieldname,fieldobject in form.fields.items() if fieldobject.required]
    completed = False
    if request.method == "POST":
        # Post means it has been sent by the submit buttom, some should have been completed
        form = ContactForm(request.POST)
        
        if form.is_valid() and form["email"].data == form["email2"].data:
            # valid and both email are equal
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
    
    form = ContactForm()
    contents = Content.get_content_for_page(context["currentpage"])
    print("content for contant page %s : %s" % (context["currentpage"], contents))
            
    context.update(locals())
    return render_to_response('contact.html', 
                              context,
                              context_instance=RequestContext(request))

