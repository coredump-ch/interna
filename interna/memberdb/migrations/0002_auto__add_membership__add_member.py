# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Membership'
        db.create_table(u'memberdb_membership', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Member', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'Membership', to=orm['memberdb.Member'])),
            ('start', self.gf('django.db.models.fields.DateField')()),
            ('end', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'memberdb', ['Membership'])

        # Adding model 'Member'
        db.create_table(u'memberdb_member', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal(u'memberdb', ['Member'])


    def backwards(self, orm):
        # Deleting model 'Membership'
        db.delete_table(u'memberdb_membership')

        # Deleting model 'Member'
        db.delete_table(u'memberdb_member')


    models = {
        u'memberdb.member': {
            'Meta': {'object_name': 'Member'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        u'memberdb.membership': {
            'Member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'Membership'", 'to': u"orm['memberdb.Member']"}),
            'Meta': {'object_name': 'Membership'},
            'end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.DateField', [], {})
        }
    }

    complete_apps = ['memberdb']