# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Student'
        db.create_table(u'academy_student', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('gender', self.gf('django.db.models.fields.BooleanField')()),
            ('birthday', self.gf('django.db.models.fields.DateField')()),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('contact', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('school', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('attend_method', self.gf('django.db.models.fields.IntegerField')()),
            ('use_sms', self.gf('django.db.models.fields.BooleanField')()),
            ('registered_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 7, 1, 0, 0))),
            ('information', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'academy', ['Student'])

        # Adding model 'Guardian'
        db.create_table(u'academy_guardian', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('contact', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('relation', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['academy.Student'])),
        ))
        db.send_create_signal(u'academy', ['Guardian'])


    def backwards(self, orm):
        # Deleting model 'Student'
        db.delete_table(u'academy_student')

        # Deleting model 'Guardian'
        db.delete_table(u'academy_guardian')


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