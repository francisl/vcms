# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie
import os

# Search facilities
SEARCH_ENGINE = "haystack" 

# DJAPIAN CONFIG
if SEARCH_ENGINE == "djapian":
    DJAPIAN_DATABASE_PATH = SERVER_PATH + "../database"

# HAYSTACK
"""
To rebuild a new search index :
    ./manage.py rebuild_index
"""
if SEARCH_ENGINE == "haystack":
    WHOOSH_SEARCH_ENGINE = 'whoosh'
    XAPIAN_SEARCH_ENGINE = 'xapian'
    HAYSTACK_SEARCH_ENGINE = XAPIAN_SEARCH_ENGINE

    if HAYSTACK_SEARCH_ENGINE == WHOOSH_SEARCH_ENGINE :
        HAYSTACK_WHOOSH_PATH = os.path.dirname(__file__) + '/../database/whoosh'
        # Build the search index in real time when in development
        SEARCH_INDEX = "RealTimeSearchIndex"
    elif HAYSTACK_SEARCH_ENGINE == XAPIAN_SEARCH_ENGINE:
        HAYSTACK_XAPIAN_PATH = os.path.dirname(__file__) + "/../database/xapian"
        # Regular search index when in production, if needed, the index will have to be built or updated through the manage.py commands
        SEARCH_INDEX = "SearchIndex"
    else:
        # no search engine define
        pass
    
    HAYSTACK_SITECONF = 'haystacksearch'
    # Haystack_link | http://haystacksearch.org/docs/
    # haystack_file | git clone git://github.com/toastdriven/django-haystack.git
    # Haystack_require_whoosh | svn co http://svn.whoosh.ca/projects/whoosh/trunk/

