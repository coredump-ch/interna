# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Member.city'
        db.alter_column(u'memberdb_member', 'city', self.gf('django.db.models.fields.CharField')(default='', max_length=100))

        # Changing field 'Member.github'
        db.alter_column(u'memberdb_member', 'github', self.gf('django.db.models.fields.CharField')(default='', max_length=32))

        # Changing field 'Member.twitter'
        db.alter_column(u'memberdb_member', 'twitter', self.gf('django.db.models.fields.CharField')(default='', max_length=32))

        # Changing field 'Member.phone'
        db.alter_column(u'memberdb_member', 'phone', self.gf('django.db.models.fields.CharField')(default='', max_length=16))

    def backwards(self, orm):

        # Changing field 'Member.city'
        db.alter_column(u'memberdb_member', 'city', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'Member.github'
        db.alter_column(u'memberdb_member', 'github', self.gf('django.db.models.fields.CharField')(max_length=32, null=True))

        # Changing field 'Member.twitter'
        db.alter_column(u'memberdb_member', 'twitter', self.gf('django.db.models.fields.CharField')(max_length=32, null=True))

        # Changing field 'Member.phone'
        db.alter_column(u'memberdb_member', 'phone', self.gf('django.db.models.fields.CharField')(max_length=16, null=True))

    models = {
        u'memberdb.member': {
            'Meta': {'ordering': "(u'name', u'id')", 'object_name': 'Member'},
            'category': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'github': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'})
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