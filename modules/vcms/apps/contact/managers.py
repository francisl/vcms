# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie

from django.db import models
from django.contrib.sites.managers import CurrentSiteManager

class ContactPageManager(models.Manager):
    def get_contact_information_for_page(self, page):
        """ take a page instance
            returns:
                a dictionary with email information
                False on error
            keys:
                msg = email html formated message
                from = email address that will appear in "from"
                confirmation = email address to send the contact request
        """
        try:
            defaultpage = self.filter(id=page)
            return {"msg":defaultpage.email_message, "from": defaultpage.reply_email, "confirmation": defaultpage.confirmation_email}
        except:
            return False
