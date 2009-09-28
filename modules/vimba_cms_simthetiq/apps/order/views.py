# -*- coding: utf-8 -*-
# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from config import simthetiq_config
from django import forms
from vimba_cms_simthetiq.apps.order.list import *
from vimba_cms_simthetiq.apps.products.models import FileFormat, ProductPage


class FreeOrderForm(forms.Form):
    Business_name = forms.CharField(required=True)
    Street = forms.CharField(required=True)
    City = forms.CharField(required=True)
    Postal_code = forms.CharField(required=True, max_length=6)
    State = forms.CharField(required=True)
    Country = forms.ChoiceField(choices=COUNTRY_LIST, initial="US", required=True)
    Firstname = forms.CharField(required=True)
    Lastname = forms.CharField(required=True)
    Phone_number = forms.CharField()
    Email = forms.EmailField(required=True)
    Application_type = forms.ModelChoiceField(FileFormat.objects.all())
    Product = forms.ModelChoiceField(ProductPage.objects.all(), required=True)
    Message = forms.CharField(widget=forms.Textarea, required=True)
  
def Order(request):
    return render_to_response('order/order.html', {})

def OrderForm(request):
    orderform = FreeOrderForm()
    requiredfields = ["id_%s" % fieldname for fieldname,fieldobject in orderform.fields.items() if fieldobject.required]
    if request.method == "POST":
        # Post means it has been sent by the submit buttom, some should have been completed
        orderform = FreeOrderForm(request.POST)
        if orderform.is_valid():
            #Email after form as been validated
            completed = [True, True]
            from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
            try:
                #Email to simthetiq
                subject = 'An order from Simthetiq has been proceed'
                email_from = simthetiq_config.simthetiq_email_from_order
                email_to = simthetiq_config.simthetiq_orderemail_to
                text_content = render_to_response('order/email_internal.txt', { "orderinfo": orderform.cleaned_data, "Title": subject })
                html_content = render_to_response('order/email_internal.html', { "orderinfo": orderform.cleaned_data, "Title": subject })
                msg = EmailMultiAlternatives(subject, text_content, email_from, [email_to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            except:
                completed[0] = False
        
            try:
                #Email to customer
                subject = 'Your order from Simthetiq has been proceed'
                email_from = simthetiq_config.simthetiq_email_from_order
                email_to = [orderform.data["Email"]]
                text_content = render_to_response('order/email_customer.txt', { "orderinfo": orderform.cleaned_data, "Title": subject })
                html_content = render_to_response('order/email_customer.html', { "orderinfo": orderform.cleaned_data, "Title": subject })
                #msg = send_mail(subject, html_content, email_from, email_to, fail_silently=False)
                msg = EmailMessage(subject, html_content, email_from, email_to)
                msg.content_subtype = "html"  # Main content is now text/html
                #msg = EmailMultiAlternatives(subject, text_content, email_from, [email_to])
                #msg.attach_alternative(html_content, "text/html")
                msg.send()
            except ValueError:
                completed[1] = False

            # send confirmation that email has been sent
            return render_to_response('email_confirmation.html', {"completed": completed[0]})
    
    return render_to_response('order/orderform.html', {'orderform': orderform, "requiredfields" : requiredfields })


def Confirm(request):
    if request.method != 'POST': return HttpResponseRedirect("/")
    return render_to_response('order/confirmation.html')

