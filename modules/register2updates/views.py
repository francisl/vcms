
from django import forms
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail, EmailMultiAlternatives

from register2updates.models import Registered2Updates
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

class Register2UpdateForm(forms.Form):
    email = forms.EmailField()
    email_confirmation = forms.EmailField()

def register_2_updates(request):

    html_info = {}
    html_info['confirm'] = _('JUST KEEP ME UP TO DATE')
    html_info['INFO_EMAIL'] = INFO_EMAIL
    html_info['INFO_PHONE'] = INFO_PHONE
    template = "request_updates.html"

    if request.method == "POST":
        form = Register2UpdateForm(request.POST)
       
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
        form = Register2UpdateForm()
        html_info.update(dict(form=form))
    
    return render_to_response(template
                              ,html_info
                              ,context_instance=RequestContext(request))
    
