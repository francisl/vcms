from django import forms
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _, ugettext
from l10n.models import Country
from satchmo_store.accounts.forms import RegistrationForm, RegistrationAddressForm
from satchmo_store.accounts.mail import send_welcome_email
from satchmo_store.contact.models import AddressBook, Contact, ContactRole, Organization
from satchmo_store.contact.forms import ContactInfoForm, ProxyContactForm
from satchmo_store.shop.models import Config
from satchmo_store.shop.utils import clean_field
from satchmo_utils.unique_id import generate_id
from signals_ahoy.signals import form_postsave
from livesettings import config_value
from satchmo_store.accounts import signals
from vcms.apps.www.registration.models import AdminRegistrationProfile
from satchmo_store.contact import signals


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

        account_verification = config_value('SHOP', 'ACCOUNT_VERIFICATION')

        if account_verification == "ADMINISTRATOR":
            user = AdminRegistrationProfile.objects.create_inactive_user(username,
                    password, email, False) # Make sure we don't send the email
            # Manually send the activation email, AdminRegistrationProfile
            # sends the email to the Administrators, instead of the default
            # that sends to the user.
            site = Site.objects.get_current()
            profile = AdminRegistrationProfile.objects.get(user=user)
            profile.send_activation_email(site)
        elif account_verification == 'EMAIL':
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
        elif account_verification == "IMMEDIATE":
            # Create the user without further validation
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

        # The action activation is set to IMMEDIATE, therefore we shall login the user
        if account_verification == 'IMMEDIATE':
            user = authenticate(username=username, password=password)
            login(request, user)
            send_welcome_email(email, first_name, last_name)
            signals.satchmo_registration_verified.send(self, contact=contact)

        self.contact = contact

        return contact


#class CustomStoreRegistrationForm(RegistrationAddressForm):
#    username = forms.CharField(label=_('Username'), max_length=30, required=True)
#    first_last_name = forms.CharField(label=_('First & last name'), max_length=60, required=True)
#    country = models.ForeignKey(Country, blank=False, null=False, verbose_name=_('Country'))
#    state = forms.CharField(_("State"), max_length=30, blank=True, null=True)
#    city = forms.CharField(_("City"), max_length=50, blank=True, null=True)
#    postal_code = forms.CharField(_("Zip / Postal code"), blank=True, null=True, max_length=9)

#    def __init__(self, *args, **kwargs):
#        super(CustomStoreRegistrationForm, self).__init__()
#        self.fields.keyOrder = ['username', 'password1', 'password2', 'organization', 'first_last_name', 'country', 'state', 'city', 'postal_code']

selection = ''

class CustomStoreRegistrationForm(ProxyContactForm):
    """
        Custom registration form for a store. This form has been
        mostly copied from satchmo_store.contact.forms.ContactInfoForm
        with minimal changes made to it.
    """
    username = forms.CharField(label=_('Username'), max_length=30, required=True)
    password = forms.CharField(label=_('Password'), max_length=30, widget=forms.PasswordInput(), required=True)
    password_confirm = forms.CharField(label=_('Confirm password'), max_length=30, widget=forms.PasswordInput(), required=True)
    organization = forms.CharField(max_length=50, label=_('Company name'), required=True)
    first_name = forms.CharField(max_length=30, label=_('First Name'), required=True)
    last_name = forms.CharField(max_length=30, label=_('Last Name'), required=True)
    #country, added in constructor
    state = forms.CharField(max_length=30, label=_('State / Province'), required=True)
    city = forms.CharField(max_length=30, label=_('City'), required=True)
    postal_code = forms.CharField(max_length=10, label=_('ZIP / Postal code'), required=True)
    email = forms.EmailField(max_length=75, label=_('Email'), required=True)
    email_confirm = forms.EmailField(max_length=75, label=_('Confirm email'), required=True)

    def __init__(self, *args, **kwargs):
        super(CustomStoreRegistrationForm, self).__init__(*args, **kwargs)
        shop = kwargs.pop('shop', None)
        if not shop:
            shop = Config.objects.get_current()
        self._shop = shop
        self.required_billing_data = config_value('SHOP', 'REQUIRED_BILLING_DATA')
        self.enforce_state = config_value('SHOP','ENFORCE_STATE')
        self._default_country = shop.sales_country
        self._local_only = shop.in_country_only
        billing_country = (self._contact and getattr(self._contact.billing_address, 'country', None)) or self._default_country
        self.fields['country'] = forms.ModelChoiceField(shop.countries(), required=False, label=_('Country'), empty_label=None, initial=billing_country.pk)
        self.fields.keyOrder = [
            'username',
            'password',
            'password_confirm',
            'organization',
            'first_name',
            'last_name',
            'country',
            'state',
            'city',
            'postal_code',
            'email',
            'email_confirm']

    def _check_state(self, data, country):
        if country and self.enforce_state and country.adminarea_set.filter(active=True).count() > 0:
            if not data or data == selection:
                raise forms.ValidationError(
                    self._local_only and _('This field is required.') \
                               or _('State is required for your country.'))
            if (country.adminarea_set
                        .filter(active=True)
                        .filter(Q(name__iexact=data)|Q(abbrev__iexact=data))
                        .count() != 1):
                raise forms.ValidationError(_('Invalid state or province.'))
        return data

    def clean(self):
        # Prevent account hijacking by disallowing duplicate emails.
        email1 = self.cleaned_data.get('email', None)
        email2 = self.cleaned_data.get('email_confirm', None)
        if email1 and email2:
            if email1 == email2:
                users_with_email = Contact.objects.filter(email=email1)
                if len(users_with_email) > 0 or (len(users_with_email) > 0 and users_with_email[0].id != self._contact.id):
                    self._errors["email"] = self.error_class([_("That email address is already in use.")])
                    del self.cleaned_data['email']
                    del self.cleaned_data['email_confirm']
            else:
                self._errors["email"] = self.error_class([_("Your email addresses does not match.")])
                del self.cleaned_data['email']
                del self.cleaned_data['email_confirm']
        else:
            self._errors["email_confirm"] = self.error_class([_("Your email address is required and must be confirmed.")])
        return self.cleaned_data

    def clean_postal_code(self):
        postcode = self.cleaned_data.get('postal_code')
        if not postcode and 'postal_code' not in self.required_billing_data:
            return postcode
        country = None

        if self._local_only:
            shop_config = Config.objects.get_current()
            country = shop_config.sales_country
        else:
            country = clean_field(self, 'country')

        if not country:
            # Either the store is misconfigured, or the country was
            # not supplied, so the country validation will fail and
            # we can defer the postcode validation until that's fixed.
            return postcode

        return self.validate_postcode_by_country(postcode, country)

    def clean_state(self):
        data = self.cleaned_data.get('state')
        if self._local_only:
            country = self._default_country
        else:
            country = clean_field(self, 'country')
            if country == None:
                raise forms.ValidationError(_('This field is required.'))
        self._check_state(data, country)
        return data

    def clean_country(self):
        if self._local_only:
            return self._default_country
        else:
            if not self.cleaned_data.get('country'):
                log.error("No country! Got '%s'" % self.cleaned_data.get('country'))
                raise forms.ValidationError(_('This field is required.'))
        return self.cleaned_data['country']

    def save(self, **kwargs):
        if not kwargs.has_key('contact'):
            kwargs['contact'] = None
        return self.save_info(**kwargs)

    def save_info(self, contact=None, **kwargs):
        """Save the contact info into the database.
        Checks to see if contact exists. If not, creates a contact
        and copies in the address and phone number."""

        customer = Contact()
        log.debug('creating new contact')

        data = self.cleaned_data.copy()

        country = data['country']
        if not isinstance(country, Country):
            country = Country.objects.get(pk=country)
            data['country'] = country
        data['country_id'] = country.id

        #shipcountry = data['ship_country']
        shipcountry = country
        if not isinstance(shipcountry, Country):
            shipcountry = Country.objects.get(pk=shipcountry)
            data['ship_country'] = shipcountry

        data['ship_country_id'] = shipcountry.id

        organization_name = data.pop('organization', None)
        if organization_name:
            org = Organization.objects.by_name(organization_name, create=True)
            customer.organization = org
        else:
            # in case customer wants to remove organization name from their profile
            customer.organization = None

        for field in customer.__dict__.keys():
            try:
                setattr(customer, field, data[field])
            except KeyError:
                pass

        if not customer.role:
            customer.role = ContactRole.objects.get(pk='Customer')

        customer.save()

        # we need to make sure we don't blindly add new addresses
        # this isn't ideal, but until we have a way to manage addresses
        # this will force just the two addresses, shipping and billing
        # TODO: add address management like Amazon.
        bill_address = customer.billing_address
        if not bill_address:
            bill_address = AddressBook(contact=customer)

        changed_location = False
        address_keys = bill_address.__dict__.keys()
        for field in address_keys:
            if (not changed_location) and field in ('state', 'country_id', 'city'):
                if getattr(bill_address, field) != data[field]:
                    changed_location = True
            try:
                setattr(bill_address, field, data[field])
            except KeyError:
                pass

        bill_address.is_default_billing = True
        bill_address.is_default_shipping = True

        bill_address.save()

        form_postsave.send(ContactInfoForm, object=customer, formdata=data, form=self)

        if changed_location:
            signals.satchmo_contact_location_changed.send(self, contact=customer)

        return customer.id

    def validate_postcode_by_country(self, postcode, country):
        responses = signals.validate_postcode.send(self, postcode=postcode, country=country)
        # allow responders to reformat the code, but if they don't return
        # anything, then just use the existing code
        for responder, response in responses:
            if response:
                return response

        return postcode
