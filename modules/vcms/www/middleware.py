from django.http import HttpResponseRedirect
from django.conf import settings
import re

class EnforceLoginMiddleware(object):
    """
    Middlware class which requires the user to be authenticated for all urls except 
    those defined in PUBLIC_URLS in settings.py. PUBLIC_URLS should be a tuple of regular 
    expresssions for the urls you want anonymous users to have access to. If PUBLIC_URLS 
    is not defined, it falls back to LOGIN_URL or failing that '/accounts/login/'.  
    Requests for urls not matching PUBLIC_URLS get redirected to LOGIN_URL with next set 
    to original path of the unauthenticted request. 
    Any urls statically served by django are excluded from this check. To enforce the same
    validation on these set SERVE_STATIC_TO_PUBLIC to False.
    """

    def __init__(self):
        self.login_url   = getattr(settings, 'LOGIN_URL', '/accounts/login/' )
        if hasattr(settings,'PUBLIC_URLS'):
            public_urls = [re.compile(url) for url in settings.PUBLIC_URLS]
        else:
            public_urls = [(re.compile("^%s$" % ( self.login_url[1:] )))]
        if getattr(settings, 'SERVE_STATIC_TO_PUBLIC', True ):
            root_urlconf = __import__(settings.ROOT_URLCONF)
            public_urls.extend([ re.compile(url.regex) 
                for url in root_urlconf.urls.urlpatterns 
                if url.__dict__.get('_callback_str') == 'django.views.static.serve' 
            ])
        self.public_urls = tuple(public_urls)

    def process_request(self, request):
        """
        Redirect anonymous users to login_url from non public urls
        """
        try:
            if request.user.is_anonymous():
                for url in self.public_urls:
                    if url.match(request.path[1:]):
                        return None
                return HttpResponseRedirect("%s?next=%s" % (self.login_url, request.path))
        except AttributeError:
            return HttpResponseRedirect("%s?next=%s" % (self.login_url, request.path))


class RequireLoginMiddleware(object):
    """
    Middleware component that wraps the login_required decorator around 
    matching URL patterns. To use, add the class to MIDDLEWARE_CLASSES and 
    define LOGIN_REQUIRED_URLS and LOGIN_REQUIRED_URLS_EXCEPTIONS in your 
    settings.py. For example:
    ------
    LOGIN_REQUIRED_URLS = (
        r'/topsecret/(.*)$',
    )
    LOGIN_REQUIRED_URLS_EXCEPTIONS = (
        r'/topsecret/login(.*)$', 
        r'/topsecret/logout(.*)$',
    )
    ------                 
    LOGIN_REQUIRED_URLS is where you define URL patterns; each pattern must 
    be a valid regex.     
    
    LOGIN_REQUIRED_URLS_EXCEPTIONS is, conversely, where you explicitly 
    define any exceptions (like login and logout URLs).
    """
    def __init__(self):
        self.required = tuple([re.compile(url) for url in settings.LOGIN_REQUIRED_URLS])
        self.exceptions = tuple([re.compile(url) for url in settings.LOGIN_REQUIRED_URLS_EXCEPTIONS])
    
    def process_view(self,request,view_func,view_args,view_kwargs):
        # No need to process URLs if user already logged in
        if request.user.is_authenticated(): return None
        # An exception match should immediately return None
        for url in self.exceptions:
            if url.match(request.path): return None
        # Requests matching a restricted URL pattern are returned 
        # wrapped with the login_required decorator
        for url in self.required:
            if url.match(request.path): return login_required(view_func)(request,*view_args,**view_kwargs)
        # Explicitly return None for all non-matching requests
        return None