# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MemberPayment'
        db.create_table(u'memberdb_memberpayment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Membership', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'MemberPayment', to=orm['memberdb.Membership'])),
            ('year', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('payment_date', self.gf('django.db.models.fields.DateField')()),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'memberdb', ['MemberPayment'])


    def backwards(self, orm):
        # Deleting model 'MemberPayment'
        db.delete_table(u'memberdb_memberpayment')


    models = {
        u'memberdb.member': {
            'Meta': {'ordering': "(u'name', u'id')", 'object_name': 'Member'},
            'category': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'})
        },
        u'memberdb.memberpayment': {
            'Membership': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'MemberPayment'", 'to': u"orm['memberdb.Membership']"}),
            'Meta': {'object_name': 'MemberPayment'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_date': ('django.db.models.fields.DateField', [], {}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '4'})
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