from django.core import urlresolvers
from django.conf import settings
from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from satchmo_store.contact import CUSTOMER_ID
from satchmo_store.contact.models import Contact
from satchmo_store.accounts.views import _login
from livesettings import config_get_group, config_value
from vcms.apps.store.forms import StoreRegistrationForm
from vcms.apps.www.registration.models import AdminRegistrationProfile
from satchmo_store.accounts import signals


import logging
log = logging.getLogger('vcms.apps.store.views')


def register_handle_form(request, redirect=None):
    """
    Handle all registration logic.  This is broken out from "register" to allow easy overriding/hooks
    such as a combined login/register page.

    This method only presents a typical login or register form, not a full address form
    (see register_handle_address_form for that one.)

    Returns:
    - Success flag
    - HTTPResponseRedirect (success) or form (fail)
    """

    if request.method == 'POST':
        form = StoreRegistrationForm(request.POST)
        if form.is_valid():
            contact = form.save(request)

            # look for explicit "next"
            next = request.POST.get('next', '')
            if not next:
                if redirect:
                    next = redirect
                else:
                    next = urlresolvers.reverse('registration_complete')
            return (True, HttpResponseRedirect(next))

    else:
        initial_data = {}
        try:
            contact = Contact.objects.from_request(request, create=False)
            initial_data = {
                'email': contact.email,
                'first_name': contact.first_name,
                'last_name': contact.last_name,
            }
        except Contact.DoesNotExist:
            log.debug("No contact in request")
            contact = None

        initial_data['next'] = request.GET.get('next', '')

        form = StoreRegistrationForm(initial=initial_data)

    return (False, form)


def activate(request, activation_key):
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
        _login(request, account)
        contact = Contact.objects.get(user=account)
        request.session[CUSTOMER_ID] = contact.id
        #send_welcome_email(contact.email, contact.first_name, contact.last_name)
        # Send an email to the user if an Administrator has activated his/her account
        if config_value('SHOP', 'ACCOUNT_VERIFICATION') == "ADMINISTRATOR":
            site = Site.objects.get_current()
            profile = AdminRegistrationProfile.objects.get(user=account)
            profile.send_welcome_email(site)
        signals.satchmo_registration_verified.send(contact, contact=contact)

    context = RequestContext(request, {
        'account': account,
        'expiration_days': config_value('SHOP', 'ACCOUNT_ACTIVATION_DAYS'),
    })
    return render_to_response('registration/activate.html',
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

        ctx = {
            'form': todo,
            'title' : _('Registration Form'),
            'show_newsletter' : show_newsletter
        }

        if extra_context:
            ctx.update(extra_context)

        context = RequestContext(request, ctx)
        return render_to_response(template, context_instance=context)
