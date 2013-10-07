# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing index on 'Image', fields ['code']
        db.delete_index(u'core_image', ['code'])

        # Adding unique constraint on 'Image', fields ['code']
        db.create_unique(u'core_image', ['code'])


    def backwards(self, orm):
        # Removing unique constraint on 'Image', fields ['code']
        db.delete_unique(u'core_image', ['code'])

        # Adding index on 'Image', fields ['code']
        db.create_index(u'core_image', ['code'])


    models = {
        u'core.image': {
            'Meta': {'object_name': 'Image'},
            'altitude': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'camera_model_code': ('django.db.models.fields.TextField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'camera_model_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'caption_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cloud_cover_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'exposure_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'features_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'film_code': ('django.db.models.fields.TextField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'film_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'focal_length_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'geographic_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'mission': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Mission']"}),
            'nadir_latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'nadir_longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'nadir_to_photo_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['core']