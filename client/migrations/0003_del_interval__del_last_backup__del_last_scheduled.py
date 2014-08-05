# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.delete_table(u'client_schedule')
        
        # Adding model 'Schedule'
        db.create_table(u'client_schedule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('destination', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['client.Destination'], null=True)),
            ('schedule_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('rule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['client.RRule'], null=True, blank=True)),
        ))
        db.send_create_signal(u'client', ['Schedule'])


    def backwards(self, orm):
        db.create_table(u'client_schedule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('destination', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['client.Destination'], null=True)),
            ('interval_hours', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('schedule_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('last_scheduled', self.gf('django.db.models.fields.DateTimeField')()),
            ('last_backup', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('rule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['client.RRule'], null=True, blank=True)),
        ))
        db.send_create_signal(u'client', ['Schedule'])
        

    models = {
        u'client.backup': {
            'Meta': {'object_name': 'Backup'},
            'destination_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'default': "'A'", 'max_length': '1'}),
            'last_error': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'local_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'local_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['client.Schedule']"}),
            'size': ('django.db.models.fields.BigIntegerField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'I'", 'max_length': '2'}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'client.backupstatus': {
            'Meta': {'object_name': 'BackupStatus'},
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'executing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'client.destination': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'Destination'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'primary_key': 'True'})
        },
        u'client.localbackupqueue': {
            'Meta': {'object_name': 'LocalBackupQueue'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'client.log': {
            'Meta': {'object_name': 'Log'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'destination': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['client.Destination']"}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_status': ('django.db.models.fields.BooleanField', [], {}),
            'remote_status': ('django.db.models.fields.BooleanField', [], {})
        },
        u'client.origin': {
            'Meta': {'object_name': 'Origin'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'remote_id': ('django.db.models.fields.BigIntegerField', [], {})
        },
        u'client.rrule': {
            'Meta': {'object_name': 'RRule'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'frequency': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'params': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'client.schedule': {
            'Meta': {'object_name': 'Schedule'},
            'destination': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['client.Destination']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rule': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['client.RRule']", 'null': 'True', 'blank': 'True'}),
            'schedule_time': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'client.webserver': {
            'Meta': {'object_name': 'WebServer'},
            'api_url': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'api_version': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'apikey': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        }
    }

    complete_apps = ['client']