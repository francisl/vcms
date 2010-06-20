from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class Registered2UpdatesManager(models.Manager):
    def is_registered(self, email):
        try:
            if self.get(email=email):
                return True
        except ObjectDoesNotExist:
            return False

