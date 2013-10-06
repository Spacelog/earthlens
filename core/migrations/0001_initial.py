# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Mission'
        db.create_table(u'core_mission', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'core', ['Mission'])

        # Adding model 'Image'
        db.create_table(u'core_image', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mission', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Mission'])),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('geographic_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('features_text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('tilt_text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('focal_length_text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('camera_model_text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('film_text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('exposure_text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('cloud_cover_text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('date_text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('caption_text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('nadir_latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('nadir_longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('sun_azimuth', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('sun_elevation', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('altitude', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Image'])

        # Adding model 'ImageFile'
        db.create_table(u'core_imagefile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Image'])),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('width', self.gf('django.db.models.fields.IntegerField')()),
            ('height', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'core', ['ImageFile'])


    def backwards(self, orm):
        # Deleting model 'Mission'
        db.delete_table(u'core_mission')

        # Deleting model 'Image'
        db.delete_table(u'core_image')

        # Deleting model 'ImageFile'
        db.delete_table(u'core_imagefile')


    models = {
        u'core.image': {
            'Meta': {'object_name': 'Image'},
            'altitude': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'camera_model_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'caption_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cloud_cover_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'date_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'exposure_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'features_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'film_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'focal_length_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'geographic_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mission': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Mission']"}),
            'nadir_latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'nadir_longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sun_azimuth': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sun_elevation': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tilt_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'core.imagefile': {
            'Meta': {'object_name': 'ImageFile'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Image']"}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        },
        u'core.mission': {
            'Meta': {'object_name': 'Mission'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['core']