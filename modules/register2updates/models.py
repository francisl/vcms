from django.db import models
from register2updates.managers import Registered2UpdatesManager


class Registered2Updates(models.Model):
    email = models.EmailField(max_length=60)
    subscribed_date = models.DateTimeField(auto_now_add=True, editable=False)

    objects = Registered2UpdatesManager()

    def __unicode__(self):
        return self.email

