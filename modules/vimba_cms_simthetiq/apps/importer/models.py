# encoding: utf-8

from __future__ import division

from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete

class JobStatus(models.Model):
    logfile_name = models.CharField(max_length=80)
    STATUS = ((0,'Completed'),(1,'Loading'),(2,'Queued'),)
    status = models.IntegerField(choices=STATUS)
    eSTATUS = ((0,'Succes'),(1,'Failed'),(2,'Warning'),(3, 'Pending'),)
    estatus = models.IntegerField(choices=eSTATUS)
    last_update = models.DateField(auto_now=True)
    
   
    def __unicode__(self):
        return self.logfile_name


class JobImportFile(models.Model):
    importfile_name = models.CharField(max_length=80)
    last_update = models.DateField(auto_now=True)
    number_column = models.IntegerField()
    
   
    def __unicode__(self):
        return self.importfile_name

class JobImport(models.Model):
    name = models.CharField(max_length=36)    
    status = models.ForeignKey(JobStatus)
    importfile = models.ForeignKey(JobImportFile)
    
    def __unicode__(self):
        return self.name.capitalize()

    class Meta:
        ordering = ['name']

