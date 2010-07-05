# -*- coding: UTF-8 -*-
# Application: Vimba - CMS
# Module: Store
# Copyright (c) 2010 Vimba inc. All rights reserved.
# Created by Francois Lebel on 12-05-2010.

from django.core import urlresolvers
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.sites.models import Site
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.utils.translation import gettext, ugettext_lazy as _
from django.views.decorators.cache import never_cache
from satchmo_store.accounts import signals
from satchmo_store.accounts.views import _login
from satchmo_store.accounts.forms import EmailAuthenticationForm
from satchmo_store.contact import CUSTOMER_ID
from satchmo_store.contact.models import Contact
from satchmo_store.shop.models import Config
from livesettings import config_get_group, config_value
from l10n.models import Country
from vcms.www.registration.models import AdminRegistrationProfile
from vcms.store.forms import StoreRegistrationForm
from vcms.www.views.html import _get_page_parameters


import logging
log = logging.getLogger('vcms.store.views')

# Add the Administrator verification method to the
# site settings "Account Verification" option.
from livesettings import config_get
from satchmo_store.shop.config import SHOP_GROUP
ACCOUNT_VERIFICATION = config_get(SHOP_GROUP, 'ACCOUNT_VERIFICATION')
ACCOUNT_VERIFICATION.add_choice(('ADMINISTRATOR', _('Administrator')))


def get_queryset_states_provinces(country_id):
    """
        Returns a queryset containing the active states/provinces for the given country.
        An empty QuerySet will be returned in the case where the country does not exist.
    """
    try:
        return Country.objects.get(pk=country_id).adminarea_set.filter(active=True)
    except Country.DoesNotExist:
        return Country.objects.none()

def get_states_provinces(request, country_id):
    """
        Returns a dictionary of states/provinces for the given country.
        Returns an empty HTTP response with response code 404
        if the country does not exist, or status code 501 if the
        it isn't an AJAX request..
    """
    if not request.is_ajax():
        return HttpResponse(status=501)
    try:
        states = [{"optionValue": aa.abbrev or aa.name, "optionDisplay": gettext(aa.name)} for aa in get_queryset_states_provinces(country_id)]
        return HttpResponse(simplejson.dumps(states), mimetype='application/javascript')
    except Country.DoesNotExist:
        return HttpResponse(status=404)


def register_handle_form(request, redirect=None):
    """
    Handle all registration logic.  This is broken out from "register" to allow easy overriding/hooks
    such as a combined login/register page.

    This handler allows a login or a full registration including address.

    Returns:
    - Success flag
    - HTTPResponseRedirect (success) or form (fail)
    - A dictionary with extra context fields
    """

    shop = Config.objects.get_current()
    try:
        contact = Contact.objects.from_request(request)
    except Contact.DoesNotExist:
        contact = None

    if request.method == 'POST':
        form = StoreRegistrationForm(request.POST)
        # Make sure the states/provinces available match
        # the selected country
        form.update_state_choices(request.POST['country'])

        if form.is_valid():
            
            contact = form.save()

            if not redirect:
                redirect = urlresolvers.reverse('registration_complete')
            return (True, HttpResponseRedirect(redirect))

    else:
        initial_data = {}
        if contact:
            initial_data = {
                'email': contact.email,
                'first_name': contact.first_name,
                'last_name': contact.last_name }
            address = contact.billing_address
            if address:
                initial_data['street1'] = address.street1
                initial_data['street2'] = address.street2
                initial_data['state'] = address.state
                initial_data['city'] = address.city
                initial_data['postal_code'] = address.postal_code
                try:
                    initial_data['country'] = address.country
                except Country.DoesNotExist:
                    USA = Country.objects.get(iso2_code__exact="US")
                    initial_data['country'] = USA

        form = StoreRegistrationForm(initial=initial_data)

    return (False, form, {'country' : shop.in_country_only})


def complete(request):
    context = { 'verification': config_value('SHOP', 'ACCOUNT_VERIFICATION')
                    ,"page_info": _get_page_parameters() }

    return render_to_response('registration/registration_complete.html',
                                context,
                                context_instance=RequestContext(request))


def activate(request, activation_key, template = 'registration/activate.html'):
    """
    Activates a user's account, if their key is valid and hasn't
    expired.
    """
    activation_key = activation_key.lower()
    account = AdminRegistrationProfile.objects.activate_user(activation_key)

    if account:
        # ** hack for logging in the user **
        # when the login form is posted, user = authenticate(username=data['username'], password=data['password'])
        # ...but we cannot authenticate without password... so we work-around authentication
        account.backend = settings.AUTHENTICATION_BACKENDS[0]
        contact = Contact.objects.get(user=account)
        #send_welcome_email(contact.email, contact.first_name, contact.last_name)
        # Send an email to the user if an Administrator has activated his/her account
        if config_value('SHOP', 'ACCOUNT_VERIFICATION') == "ADMINISTRATOR":
            site = Site.objects.get_current()
            profile = AdminRegistrationProfile.objects.get(user=account)
            profile.send_welcome_email(site)
            template = 'registration/administrator_activate.html'
        else:
            # Otherwise login the user as he/she is the one activating his/her account
            _login(request, account)
            request.session[CUSTOMER_ID] = contact.id

        signals.satchmo_registration_verified.send(contact, contact=contact)

    context = RequestContext(request, {
        'account': account,
        'expiration_days': config_value('SHOP', 'ACCOUNT_ACTIVATION_DAYS'),
        "page_info": _get_page_parameters(),
    })
    return render_to_response(template,
                              context_instance=context)


def register(request, redirect=None, template='registration/registration_form.html'):
    """
        Allows a new user to register an account.
    """
    ret = register_handle_form(request, redirect)
    success = ret[0]
    todo = ret[1]
    if len(ret) > 2:
        extra_context = ret[2]
    else:
        extra_context = {}

    if success:
        return todo
    else:
        if config_get_group('NEWSLETTER'):
            show_newsletter = True
        else:
            show_newsletter = False

        context = {
            'form': todo,
            'show_newsletter' : show_newsletter
        }

        if extra_context:
            context.update(extra_context)

        context.update({"page_info": _get_page_parameters()})

        return render_to_response(template,
                                    context,
                                    context_instance=RequestContext(request))


def emaillogin(request, template_name='registration/login.html',
    auth_form=EmailAuthenticationForm, redirect_field_name=REDIRECT_FIELD_NAME):
    "Displays the login form and handles the login action. Altered to use the EmailAuthenticationForm"

    redirect_to = request.REQUEST.get(redirect_field_name, '')

    # Avoid redirecting to logout if the user clicked on login after logout
    if redirect_to == urlresolvers.reverse('auth_logout'):
        redirect_to = None

    success, todo = _login(request, redirect_to)
    if success:
        # return the response redirect
        return todo
    else:
        # continue with the login form
        form = todo

    request.session.set_test_cookie()
    if Site._meta.installed:
        current_site = Site.objects.get_current()
    else:
        current_site = RequestSite(request)

    return render_to_response(template_name, {
        'form': form,
        redirect_field_name: redirect_to,
        'site_name': current_site.name,
        "page_info": _get_page_parameters(),
    }, context_instance=RequestContext(request))
emaillogin = never_cache(emaillogin)
