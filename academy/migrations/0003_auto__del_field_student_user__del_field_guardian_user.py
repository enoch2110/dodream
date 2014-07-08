# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Student.user'
        db.delete_column(u'academy_student', 'user_id')

        # Deleting field 'Guardian.user'
        db.delete_column(u'academy_guardian', 'user_id')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Student.user'
        raise RuntimeError("Cannot reverse this migration. 'Student.user' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Student.user'
        db.add_column(u'academy_student', 'user',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Guardian.user'
        raise RuntimeError("Cannot reverse this migration. 'Guardian.user' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Guardian.user'
        db.add_column(u'academy_guardian', 'user',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True),
                      keep_default=False)


    models = {
        u'academy.guardian': {
            'Meta': {'object_name': 'Guardian'},
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'relation': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['academy.Student']"})
        },
        u'academy.student': {
            'Meta': {'object_name': 'Student'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'attend_method': ('django.db.models.fields.IntegerField', [], {}),
            'birthday': ('django.db.models.fields.DateField', [], {}),
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'gender': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'information': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'registered_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 7, 1, 0, 0)'}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'use_sms': ('django.db.models.fields.BooleanField', [], {})
        }
    }

    complete_apps = ['academy']