# encoding: utf-8
# copyright Vimba inc. 2010
# programmer : Francis Lavoie

from django.utils.translation import ugettext_lazy as _
from django.db import models
from vcms.apps.www.models import Page
from vcms.apps.contact.managers import ContactPageManager


APP_SLUGS = "contact"


class ContactPage(Page):
    page_header = models.TextField(help_text=_("Title at the top of the page"))
    form_name = models.CharField(max_length=75)
    email_message = models.TextField(help_text=_("Message that will be displayed in the email"))
    reply_email = models.EmailField(help_text=_("Email address, could be your email or a robot email(ex: no-reply@yourbusiness.com"))
    confirmation_email = models.EmailField(help_text=_("Email address where you would like to receive the information"))
    
    objects = ContactPageManager()
    
    class Meta:
        verbose_name = "Contact page"
        verbose_name_plural = "Contact pages"

    def __unicode__(self):
        return self.name

    def save(self):
        self.module = 'Contact'
        self.app_slug = 'contact'
        super(ContactPage, self).save()

