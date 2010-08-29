
from django import forms
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from django.template import RequestContext
from django.utils import simplejson
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail, EmailMultiAlternatives

from updates_registration.models import UpdatesRegistration
from config.contacts import INFO_EMAIL, INFO_PHONE
from config.email import EMAILS


def _send_email(email_to, email_from, subject="Thank you for subscribing to Simthetiq Updates"):
    try:
        text_content = render_to_response('registered2updates_confirmation_email.txt', { 'INFO_EMAIL':INFO_EMAIL, 'INFO_PHONE':INFO_PHONE })
        html_content = render_to_response('registered2updates_confirmation_email.html', { 'INFO_EMAIL':INFO_EMAIL, 'INFO_PHONE':INFO_PHONE })
        msg = EmailMultiAlternatives(subject, text_content, email_from, [email_to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return True
    except:
        return False

class UpdatesRegistrationForm(forms.Form):
    registration_email = forms.EmailField(label=_("Email"))
    registration_email_confirmation = forms.EmailField(label=_("Email Confirmation"))

def register_2_updates_old(request):

    html_info = {}
    html_info['confirm'] = _('JUST KEEP ME UP TO DATE')
    html_info['INFO_EMAIL'] = INFO_EMAIL
    html_info['INFO_PHONE'] = INFO_PHONE
    template = "request_updates.html"

    if request.method == "POST":
        form = UpdatesRegistrationForm(request.POST)
       
        if form.is_valid():
            html_info['email_registered'] = form.cleaned_data['email']
            if form.cleaned_data['email'] != form.cleaned_data['email_confirmation']:
                html_info['EMAIL_MATCH_ERROR'] = True
            elif Registered2Updates.objects.is_registered(html_info['email_registered']):
                html_info['EMAIL_ALREADY_EXIST_ERROR'] = True
            else:
                new_request = Registered2Updates(email=form.cleaned_data['email'])
                as_been_sent = _send_email(form.cleaned_data['email_confirmation'], EMAILS["CONTACT"]["FROM"])
                new_request.save()
                template = "registered2updates_confirmation.html"
                    
        html_info.update(dict(form=form))
               
    else:
        form = UpdatesRegistrationForm()
        html_info.update(dict(form=form))
    
    return render_to_response(template
                              ,html_info
                              ,context_instance=RequestContext(request))
    
def updates_registration(request):
    if request.method == "POST":
        form_object = UpdatesRegistrationForm(request.POST)
        form = UpdatesRegistrationFormManager(form_object, request)
        form_success = form.validate()
         
        if form_success:
            return form.notify_and_redirect()
               
    else:
        form_object = UpdatesRegistrationForm()
        form = UpdatesRegistrationFormManager(form_object, request)
        
    
    return render_to_response("request_updates.html"
                              ,{'form': form.render_html()}
                              ,context_instance=RequestContext(request))
     
def register_success(request):
    return render_to_response("registered2updates_confirmation.html"
                              ,{}
                              ,context_instance=RequestContext(request))
    
class UpdatesRegistrationFormManager(object):
    def __init__(self, form, request, template_form="request_updates_form.html"):
        self.template_form = template_form
        self.is_valid = False
        self.request = request
        self.form = form
        self.confirm_button_text = _('JUST KEEP ME UP TO DATE')
        self.email = self.email_confirmation = None
        self.EMAIL_MATCH_ERROR = False
        self.EMAIL_ALREADY_EXIST_ERROR = False
        
    def _validate(self):
        if self.form.is_valid(): 
            self.email = self.form.cleaned_data['email']
            self.email_confirmation = self.form.cleaned_data['email_confirmation']
            if self.email != self.email_confirmation:
                self.EMAIL_MATCH_ERROR = True
            elif UpdatesRegistration.objects.is_registered(self.email):
                self.EMAIL_ALREADY_EXIST_ERROR = True
            else:
                self.is_valid = True
        else: 
            self.is_valid = False

    def validate(self):
        self._validate()
        return self.is_valid
        
    def notify_and_redirect(self):
        new_request = UpdatesRegistration(email=self.email)
        as_been_sent = _send_email(self.email_confirmation, EMAILS["CONTACT"]["FROM"])
        new_request.save()
        redirect = urlresolvers.reverse('updatesregistration.views.register_success')
        return HttpResponseRedirect(redirect)
            
    
    def render_html(self):
        return render_to_string(self.template_form
                                ,{'form': self.form 
                                  ,'confirm_button_text':self.confirm_button_text
                                  ,'EMAIL_MATCH_ERROR': self.EMAIL_MATCH_ERROR
                                  ,'EMAIL_ALREADY_EXIST_ERROR': self.EMAIL_ALREADY_EXIST_ERROR
                                  }
                                ,context_instance=RequestContext(self.request))
    
