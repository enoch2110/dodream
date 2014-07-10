# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Academy'
        db.create_table(u'academy_academy', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'academy', ['Academy'])

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
            ('registered_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 7, 10, 0, 0))),
            ('information', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, null=True, blank=True)),
            ('academy', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['academy.Academy'])),
        ))
        db.send_create_signal(u'academy', ['Student'])

        # Adding model 'Staff'
        db.create_table(u'academy_staff', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('contact', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Group'])),
            ('main_course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['academy.Course'])),
            ('specs', self.gf('django.db.models.fields.TextField')(max_length=100)),
            ('registered_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 7, 10, 0, 0))),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, null=True, blank=True)),
            ('academy', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['academy.Academy'])),
        ))
        db.send_create_signal(u'academy', ['Staff'])

        # Adding model 'Guardian'
        db.create_table(u'academy_guardian', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('contact', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('relation', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['academy.Student'])),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'academy', ['Guardian'])

        # Adding model 'Course'
        db.create_table(u'academy_course', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['academy.CourseCategory'])),
            ('price', self.gf('django.db.models.fields.IntegerField')()),
            ('price_info', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('syllabus', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'academy', ['Course'])

        # Adding model 'CourseCategory'
        db.create_table(u'academy_coursecategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['academy.CourseCategory'], null=True, blank=True)),
        ))
        db.send_create_signal(u'academy', ['CourseCategory'])


    def backwards(self, orm):
        # Deleting model 'Academy'
        db.delete_table(u'academy_academy')

        # Deleting model 'Student'
        db.delete_table(u'academy_student')

        # Deleting model 'Staff'
        db.delete_table(u'academy_staff')

        # Deleting model 'Guardian'
        db.delete_table(u'academy_guardian')

        # Deleting model 'Course'
        db.delete_table(u'academy_course')

        # Deleting model 'CourseCategory'
        db.delete_table(u'academy_coursecategory')


    models = {
        u'academy.academy': {
            'Meta': {'object_name': 'Academy'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'academy.course': {
            'Meta': {'object_name': 'Course'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['academy.CourseCategory']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.IntegerField', [], {}),
            'price_info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'syllabus': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'academy.coursecategory': {
            'Meta': {'object_name': 'CourseCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['academy.CourseCategory']", 'null': 'True', 'blank': 'True'})
        },
        u'academy.guardian': {
            'Meta': {'object_name': 'Guardian'},
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'relation': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['academy.Student']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'academy.staff': {
            'Meta': {'object_name': 'Staff'},
            'academy': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['academy.Academy']"}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'main_course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['academy.Course']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'registered_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 7, 10, 0, 0)'}),
            'specs': ('django.db.models.fields.TextField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'academy.student': {
            'Meta': {'object_name': 'Student'},
            'academy': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['academy.Academy']"}),
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
            'registered_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 7, 10, 0, 0)'}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'use_sms': ('django.db.models.fields.BooleanField', [], {}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['academy']