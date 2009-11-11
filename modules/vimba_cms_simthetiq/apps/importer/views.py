# encoding: utf-8
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Template, Context, RequestContext 
from django import forms

from vimba_cms_simthetiq.apps.importer import models
#from vimba_cms_simthetiq.apps.products import models as productmodels

from django.contrib.auth.decorators import login_required


## ------------------------
@login_required
def dashboard(request, context={}):
    jobs = models.JobImport.objects.all()

    return render_to_response('importer_dashboard.html',
                                { "jobs":  jobs, },
                                context_instance=RequestContext(request))

@login_required
def log(request, context={}):
    jobs = models.JobImport.objects.all()
    
    try:
        toImport = open(os.path.dirname(__file__) + "/log/", 'r')
    except:
        toImport = False
    
    i = 0
    for line in toImport:
        if i == 0:
            #skip title
            i = 1
        else:
            i = i + 1
            log = line.split(";")
            
    
    return render_to_response('importer_dashboard.html',
                                { "jobs":  jobs, },
                                context_instance=RequestContext(request))


@login_required
def importDataSource(request):
    from vimba_cms_simthetiq.tools import images_import as ii
    from vimba_cms_simthetiq.tools import product_import as pi

    pi.importProducts(drop=True, debug=True)
    ii.importImages(drop=True, debug=True)
    pi.setOriginalImage()

