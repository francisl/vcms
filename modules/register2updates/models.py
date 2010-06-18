from django.db import models
# Create your models here.


class Registered2Updates(models.Model):
    email = models.EmailField(max_length=60)
    subscribed_date = models.DateTimeField(auto_now_add=True, editable=False)

    def __unicode__(self):
        return self.email


