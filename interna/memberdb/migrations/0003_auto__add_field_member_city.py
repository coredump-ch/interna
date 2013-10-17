# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Member.city'
        db.add_column(u'memberdb_member', 'city',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Member.city'
        db.delete_column(u'memberdb_member', 'city')


    models = {
        u'memberdb.member': {
            'Meta': {'ordering': "(u'name', u'id')", 'object_name': 'Member'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'})
        },
        u'memberdb.membership': {
            'Member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'Membership'", 'to': u"orm['memberdb.Member']"}),
            'Meta': {'ordering': "(u'-start', u'-Member__pk')", 'object_name': 'Membership'},
            'end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.DateField', [], {})
        }
    }

    complete_apps = ['memberdb']