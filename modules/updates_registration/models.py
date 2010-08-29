from django.db import models
from updates_registration.managers import UpdatesRegistrationManager


class UpdatesRegistration(models.Model):
    email = models.EmailField(max_length=60)
    subscribed_date = models.DateTimeField(auto_now_add=True, editable=False)

    objects = UpdatesRegistrationManager()

    def __unicode__(self):
        return self.email

