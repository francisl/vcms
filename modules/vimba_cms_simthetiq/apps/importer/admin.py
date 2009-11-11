# encoding: utf-8

from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required

from vimba_cms_simthetiq.apps.importer.models import JobImport, JobStatus, JobImportFile

class JobImportAdmin(admin.ModelAdmin):
    pass

class JobStatusAdmin(admin.ModelAdmin):
    pass

class JobImportFileAdmin(admin.ModelAdmin):
    pass

admin.site.register(JobImport, JobImportAdmin)
admin.site.register(JobStatus, JobStatusAdmin)
admin.site.register(JobImportFile, JobImportFileAdmin)
