from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import mail_admins
from django.db import transaction
from django.template.loader import render_to_string
from registration.models import RegistrationManager, RegistrationProfile, SHA1_RE


class AdminRegistrationManager(RegistrationManager):
    """
    Custom manager for the ``AdminRegistrationProfile`` model.

    The methods defined here provide shortcuts for account creation
    and activation (including generation and emailing of activation
    keys), and for cleaning out expired inactive accounts.

    """
    def activate_user(self, activation_key):
        """
        Validate an activation key and activate the corresponding
        ``User`` if valid.

        If the key is valid and has not expired, return the ``User``
        after activating.

        If the key is not valid or has expired, return ``False``.

        If the key is valid but the ``User`` is already active,
        return ``False``.

        To prevent reactivation of an account which has been
        deactivated by site administrators, the activation key is
        reset to the string constant ``RegistrationProfile.ACTIVATED``
        after successful activation.

        """
        # Make sure the key we're trying conforms to the pattern of a
        # SHA1 hash; if it doesn't, no point trying to look it up in
        # the database.
        if SHA1_RE.search(activation_key):
            try:
                profile = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                return False
            if not profile.activation_key_expired():
                #print "DEBUG: Envoit email a partir de AdminRegistrationManager"
                user = profile.user
                user.is_active = True
                user.save()
                profile.activation_key = self.model.ACTIVATED
                profile.save()
                # Send an email to the user
                #ctx_dict = {'activation_key': self.activation_key,
                #            'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                #            'site': site}
                #subject = render_to_string('registration/activation_email_subject.txt',
                #                           ctx_dict)
                # Email subject *must not* contain newlines
                #subject = ''.join(subject.splitlines())
                #message = render_to_string('registration/activation_email.txt',
                #                           ctx_dict)
                #user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
                return user
        return False

    def create_inactive_user(self, username, email, password,
                             site, send_email=True, save_user=True):
        """
        Create a new, inactive ``User``, generate a
        ``RegistrationProfile`` and email its activation key to the
        ``User``, returning the new ``User``.

        By default, an activation email will be sent to the new
        user. To disable this, pass ``send_email=False``.
        
        The only modification to the method from the inherited class
        is that we added a parameter to save the user within this
        method. That way, we can save only if the steps undertaken
        in the method calling this one succeeds.
        
        """
        new_user = User.objects.create_user(username, email, password)
        new_user.is_active = False

        if save_user:
            new_user.save()

        registration_profile = self.create_profile(new_user)

        if send_email:
            registration_profile.send_activation_email(site)

        return new_user


class AdminRegistrationProfile(RegistrationProfile):
    """
    A simple profile which stores an activation key for use during
    user account registration.

    Generally, you will not want to interact directly with instances
    of this model; the provided manager includes methods
    for creating and activating new accounts, as well as for cleaning
    out accounts which have never been activated.

    While it is possible to use this model as the value of the
    ``AUTH_PROFILE_MODULE`` setting, it's not recommended that you do
    so. This model's sole purpose is to store data temporarily during
    account registration and activation.

    """
    objects = AdminRegistrationManager()

    class Meta:
        proxy = True

    def send_activation_email(self, site, contact, billing_address):
        """
        Send an activation email to the Administrators to
        activate this ``RegistrationProfile``.

        The activation email will make use of two templates:

        ``registration/activation_email_subject.txt``
            This template will be used for the subject line of the
            email. Because it is used as the subject line of an email,
            this template's output **must** be only a single line of
            text; output longer than one line will be forcibly joined
            into only a single line.

        ``registration/activation_email.txt``
            This template will be used for the body of the email.

        These templates will each receive the following context
        variables:

        ``activation_key``
            The activation key for the new account.

        ``expiration_days``
            The number of days remaining during which the account may
            be activated.

        ``site``
            An object representing the site on which the user
            registered; depending on whether ``django.contrib.sites``
            is installed, this may be an instance of either
            ``django.contrib.sites.models.Site`` (if the sites
            application is installed) or
            ``django.contrib.sites.models.RequestSite`` (if
            not). Consult the documentation for the Django sites
            framework for details regarding these objects' interfaces.

        """

        #print "DEBUG: Envoit email a partir de AdminRegistrationProfile"
        ctx_dict = {'activation_key': self.activation_key,
                    'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                    'site': site,
                    'full_name': contact.full_name,
                    'organization': contact.organization.name,
                    'organization_type': contact.organization.type.name,
                    'address': billing_address.street1,
                    'suite_unit_apt': billing_address.street2,
                    'city': billing_address.city,
                    'state': billing_address.state,
                    'postal_code': billing_address.postal_code,
                    'country': billing_address.country.name,
                    'phone_number': '', # TODO
                    'role': contact.role.name
                    }
        subject = render_to_string('registration/administrator_activation_email_subject.txt',
                                   ctx_dict)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())

        message = render_to_string('registration/administrator_activation_email.txt',
                                   ctx_dict)

        mail_admins(subject, message)

    def send_welcome_email(self, site):
        """
        Send a welcome email to the user.

        The welcome email will make use of two templates:

        ``registration/welcome_email_subject.txt``
            This template will be used for the subject line of the
            email. Because it is used as the subject line of an email,
            this template's output **must** be only a single line of
            text; output longer than one line will be forcibly joined
            into only a single line.

        ``registration/welcome_email.txt``
            This template will be used for the body of the email.

        These templates will each receive the following context
        variable:

        ``site``
            An object representing the site on which the user
            registered; depending on whether ``django.contrib.sites``
            is installed, this may be an instance of either
            ``django.contrib.sites.models.Site`` (if the sites
            application is installed) or
            ``django.contrib.sites.models.RequestSite`` (if
            not). Consult the documentation for the Django sites
            framework for details regarding these objects' interfaces.

        """
        ctx_dict = {'site': site}
        subject = render_to_string('registration/welcome_email_subject.txt',
                                   ctx_dict)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())

        message = render_to_string('registration/welcome_email.txt',
                                   ctx_dict)

        self.user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
