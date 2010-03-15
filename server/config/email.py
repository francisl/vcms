# encoding: utf-8
#
#  Created by Francis Lavoie on 08-01-22.
#  Copyright (c) 2008 __MyCompanyName__. All rights reserved.

# ## ###
# ## SMTP SERVER CONFIG
EMAIL_HOST='smtp.webfaction.com'
# stmp: 25, stmp-ssl: 465, stmp-tls: 587
EMAIL_PORT=587                    
EMAIL_HOST_USER='simthetiq_noreply'
EMAIL_HOST_PASSWORD='cfd6d14a'
EMAIL_USE_TLS=True  # False OR True


# ## ###
# ## DJANGO INTERNAL EMAIL
ADMINS = (
    ('simthetiq support', 'support@simthetiq.com'),
)
MANAGERS = ADMINS

# ## ###
# ## CUSTOM EMAIL SETTINGS
# TODO : PUT these setting inside the database

EMAILS = { "CONTACT": { "FROM" : "no-reply@simthetiq.com",
                        "TO" : "vcloutier@simthetiq.com", 
                        "CAPTCHA": False },
            "ORDER" : { "FROM" : "order@simthetiq.com",
                        "TO" : "order@simthetiq.com", 
                        "CAPTCHA": False }                 
         }

