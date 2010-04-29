from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from satchmo_store.accounts.forms import RegistrationForm
from satchmo_store.contact.models import Contact, ContactRole
from satchmo_utils.unique_id import generate_id
from livesettings import config_value
from satchmo_store.accounts import signals


import logging
log = logging.getLogger('vcms.apps.store.forms')


class StoreRegistrationForm(RegistrationForm):
    def save_contact(self, request):
        log.debug("Saving contact")
        data = self.cleaned_data
        password = data['password1']
        email = data['email']
        first_name = data['first_name']
        last_name = data['last_name']
        username = generate_id(first_name, last_name, email)

        verify = (config_value('SHOP', 'ACCOUNT_VERIFICATION') == 'EMAIL')

        if verify:
            site = Site.objects.get_current()
            from vcms.apps.www.registration.models import AdminRegistrationProfile
            # TODO:
            # In django-registration trunk this signature has changed.
            # Satchmo is going to stick with the latest release so I'm changing
            # this to work with 0.7
            # When 0.8 comes out we're going to have to refactor to this:
            #user = RegistrationProfile.objects.create_inactive_user(
            #    username, email, password, site)
            # See ticket #1028 where we checked in the above line prematurely
            user = AdminRegistrationProfile.objects.create_inactive_user(username,
                    password, email)
        else:
            user = User.objects.create_user(username, email, password)

        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # If the user already has a contact, retrieve it.
        # Otherwise, create a new one.
        try:
            contact = Contact.objects.from_request(request, create=False)

        except Contact.DoesNotExist:
            contact = Contact()

        contact.user = user
        contact.first_name = first_name
        contact.last_name = last_name
        contact.email = email
        contact.role = ContactRole.objects.get(pk='Customer')
        contact.title = data.get('title', '')
        contact.save()

        if 'newsletter' not in data:
            subscribed = False
        else:
            subscribed = data['newsletter']

        signals.satchmo_registration.send(self, contact=contact, subscribed=subscribed, data=data)

        if not verify:
            user = authenticate(username=username, password=password)
            login(request, user)
            #send_welcome_email(email, first_name, last_name)
            signals.satchmo_registration_verified.send(self, contact=contact)
        else:
            site = Site.objects.get_current()
            user.send_activation_email(site)

        self.contact = contact

        return contact
