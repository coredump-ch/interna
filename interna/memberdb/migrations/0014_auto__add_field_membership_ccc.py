# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Membership.ccc'
        db.add_column(u'memberdb_membership', 'ccc',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Membership.ccc'
        db.delete_column(u'memberdb_membership', 'ccc')


    models = {
        u'memberdb.member': {
            'Meta': {'ordering': "(u'name', u'id')", 'object_name': 'Member'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'github': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'})
        },
        u'memberdb.membership': {
            'Member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'Membership'", 'to': u"orm['memberdb.Member']"}),
            'Meta': {'ordering': "(u'-start', u'-Member__pk')", 'object_name': 'Membership'},
            'category': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'ccc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid_until': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateField', [], {})
        }
    }

    complete_apps = ['memberdb']