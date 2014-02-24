# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TopImage'
        db.create_table(u'leaderboards_topimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('uploaded_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('image_jpeg', self.gf('django.db.models.fields.files.ImageField')(default='average_image/default.jpg', max_length=100)),
            ('image_height', self.gf('django.db.models.fields.PositiveSmallIntegerField')(blank=True)),
            ('image_width', self.gf('django.db.models.fields.PositiveSmallIntegerField')(blank=True)),
            ('box_x', self.gf('django.db.models.fields.FloatField')()),
            ('box_y', self.gf('django.db.models.fields.FloatField')()),
            ('box_height', self.gf('django.db.models.fields.FloatField')()),
            ('box_width', self.gf('django.db.models.fields.FloatField')()),
            ('detector', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['detectors.Detector'])),
        ))
        db.send_create_signal(u'leaderboards', ['TopImage'])


    def backwards(self, orm):
        # Deleting model 'TopImage'
        db.delete_table(u'leaderboards_topimage')


    models = {
        u'accounts.detectmeprofile': {
            'Meta': {'object_name': 'DetectMeProfile'},
            'autosubscribe': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'avatar': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'favourite_snack': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en-us'", 'max_length': '10', 'blank': 'True'}),
            'mugshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'post_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'privacy': ('django.db.models.fields.CharField', [], {'default': "'registered'", 'max_length': '15'}),
            'show_signatures': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'signature': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'blank': 'True'}),
            'signature_html': ('django.db.models.fields.TextField', [], {'max_length': '1054', 'blank': 'True'}),
            'time_zone': ('django.db.models.fields.FloatField', [], {'default': '3.0'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'detectme_profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'detectors.detector': {
            'Meta': {'ordering': "('created_at',)", 'object_name': 'Detector'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.DetectMeProfile']"}),
            'average_image': ('django.db.models.fields.files.ImageField', [], {'default': "'defaults/default.png'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'hash_value': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['detectors.Detector']", 'null': 'True', 'blank': 'True'}),
            'sizes': ('django.db.models.fields.TextField', [], {}),
            'target_class': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'uploaded_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'weights': ('django.db.models.fields.TextField', [], {})
        },
        u'leaderboards.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'leaderboards.competition': {
            'Meta': {'object_name': 'Competition'},
            'finish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'leaderboards.performance': {
            'Meta': {'object_name': 'Performance'},
            'average_precision': ('django.db.models.fields.FloatField', [], {}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['leaderboards.Category']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'detector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['detectors.Detector']"}),
            'detector_author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.DetectMeProfile']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'precision': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'recall': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'test_set': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'leaderboards.topimage': {
            'Meta': {'object_name': 'TopImage'},
            'box_height': ('django.db.models.fields.FloatField', [], {}),
            'box_width': ('django.db.models.fields.FloatField', [], {}),
            'box_x': ('django.db.models.fields.FloatField', [], {}),
            'box_y': ('django.db.models.fields.FloatField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'detector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['detectors.Detector']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_height': ('django.db.models.fields.PositiveSmallIntegerField', [], {'blank': 'True'}),
            'image_jpeg': ('django.db.models.fields.files.ImageField', [], {'default': "'average_image/default.jpg'", 'max_length': '100'}),
            'image_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'blank': 'True'}),
            'uploaded_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'leaderboards.userscore': {
            'Meta': {'object_name': 'UserScore'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['leaderboards.Category']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.DetectMeProfile']"})
        }
    }

    complete_apps = ['leaderboards']