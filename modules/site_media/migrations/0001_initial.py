# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ImageCategory'
        db.create_table('site_media_imagecategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('default_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=150)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('site_media', ['ImageCategory'])

        # Adding model 'ImageCategoryTranslation'
        db.create_table('site_media_imagecategorytranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=150)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['site_media.ImageCategory'])),
            ('lang', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['www.Language'])),
        ))
        db.send_create_signal('site_media', ['ImageCategoryTranslation'])

        # Adding model 'Image'
        db.create_table('site_media_image', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('default_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=150)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('file_size', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
        ))
        db.send_create_signal('site_media', ['Image'])

        # Adding M2M table for field category on 'Image'
        db.create_table('site_media_image_category', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('image', models.ForeignKey(orm['site_media.image'], null=False)),
            ('imagecategory', models.ForeignKey(orm['site_media.imagecategory'], null=False))
        ))
        db.create_unique('site_media_image_category', ['image_id', 'imagecategory_id'])

        # Adding model 'ImageDescription'
        db.create_table('site_media_imagedescription', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['site_media.Image'])),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=150)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('lang', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['www.Language'])),
        ))
        db.send_create_signal('site_media', ['ImageDescription'])


    def backwards(self, orm):
        
        # Deleting model 'ImageCategory'
        db.delete_table('site_media_imagecategory')

        # Deleting model 'ImageCategoryTranslation'
        db.delete_table('site_media_imagecategorytranslation')

        # Deleting model 'Image'
        db.delete_table('site_media_image')

        # Removing M2M table for field category on 'Image'
        db.delete_table('site_media_image_category')

        # Deleting model 'ImageDescription'
        db.delete_table('site_media_imagedescription')


    models = {
        'site_media.image': {
            'Meta': {'object_name': 'Image'},
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['site_media.ImageCategory']", 'symmetrical': 'False'}),
            'default_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'file_size': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'site_media.imagecategory': {
            'Meta': {'object_name': 'ImageCategory'},
            'default_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'site_media.imagecategorytranslation': {
            'Meta': {'object_name': 'ImageCategoryTranslation'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['site_media.ImageCategory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['www.Language']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'})
        },
        'site_media.imagedescription': {
            'Meta': {'object_name': 'ImageDescription'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['site_media.Image']"}),
            'lang': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['www.Language']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'})
        },
        'www.language': {
            'Meta': {'object_name': 'Language'},
            'language': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'})
        }
    }

    complete_apps = ['site_media']
