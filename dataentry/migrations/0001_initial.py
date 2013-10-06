# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Account'
        db.create_table(u'dataentry_account', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=255)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'dataentry', ['Account'])

        # Adding M2M table for field groups on 'Account'
        m2m_table_name = db.shorten_name(u'dataentry_account_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('account', models.ForeignKey(orm[u'dataentry.account'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['account_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'Account'
        m2m_table_name = db.shorten_name(u'dataentry_account_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('account', models.ForeignKey(orm[u'dataentry.account'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['account_id', 'permission_id'])

        # Adding model 'InterceptionRecord'
        db.create_table(u'dataentry_interceptionrecord', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('irf_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('time', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('number_of_victims', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('number_of_traffickers', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('staff_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('who_in_group', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('drugged_or_drowsy', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('meeting_someone_across_border', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('seen_in_last_month_in_nepal', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('traveling_with_someone_not_with_her', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('wife_under_18', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('married_in_past_2_weeks', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('married_in_past_2_8_weeks', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('less_than_2_weeks_before_eloping', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('between_2_12_weeks_before_eloping', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('caste_not_same_as_relative', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('caught_in_lie', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('where_going', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('doesnt_know_going_to_india', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('running_away_over_18', self.gf('django.db.models.fields.BooleanField')()),
            ('running_away_under_18', self.gf('django.db.models.fields.BooleanField')()),
            ('going_to_gulf_for_work', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('no_address_in_india', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('no_company_phone', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('no_appointment_letter', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('valid_gulf_country_visa', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('passport_with_broker', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('not_real_job', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('couldnt_confirm_job', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('no_bags_long_trip', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('shopping_overnight_stuff_in_bags', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('no_enrollment_docs', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('doesnt_know_school_name', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('no_school_phone', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('not_enrolled_in_school', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('reluctant_treatment_info', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('no_medical_documents', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('fake_medical_documents', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('no_medical_appointment', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('doesnt_know_villiage_details', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('reluctant_villiage_info', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('reluctant_family_info', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('refuses_family_info', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('under_18_cant_contact_family', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('under_18_family_doesnt_know', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('under_18_family_unwilling', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('over_18_family_doesnt_know', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('over_18_family_unwilling', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('talked_to_brother', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('talked_to_sister', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('talked_to_father', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('talked_to_mother', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('talked_to_grandparent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('talked_to_aunt_uncle', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('talked_to_other', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('talked_to_other_value', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('reported_total_red_flags', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'dataentry', ['InterceptionRecord'])


    def backwards(self, orm):
        # Deleting model 'Account'
        db.delete_table(u'dataentry_account')

        # Removing M2M table for field groups on 'Account'
        db.delete_table(db.shorten_name(u'dataentry_account_groups'))

        # Removing M2M table for field user_permissions on 'Account'
        db.delete_table(db.shorten_name(u'dataentry_account_user_permissions'))

        # Deleting model 'InterceptionRecord'
        db.delete_table(u'dataentry_interceptionrecord')


    models = {
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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'dataentry.account': {
            'Meta': {'object_name': 'Account'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"})
        },
        u'dataentry.interceptionrecord': {
            'Meta': {'object_name': 'InterceptionRecord'},
            'between_2_12_weeks_before_eloping': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'caste_not_same_as_relative': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'caught_in_lie': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'couldnt_confirm_job': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'doesnt_know_going_to_india': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'doesnt_know_school_name': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'doesnt_know_villiage_details': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'drugged_or_drowsy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fake_medical_documents': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'going_to_gulf_for_work': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'irf_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'less_than_2_weeks_before_eloping': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'married_in_past_2_8_weeks': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'married_in_past_2_weeks': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'meeting_someone_across_border': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'no_address_in_india': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'no_appointment_letter': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'no_bags_long_trip': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'no_company_phone': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'no_enrollment_docs': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'no_medical_appointment': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'no_medical_documents': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'no_school_phone': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'not_enrolled_in_school': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'not_real_job': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number_of_traffickers': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'number_of_victims': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'over_18_family_doesnt_know': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'over_18_family_unwilling': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'passport_with_broker': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'refuses_family_info': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reluctant_family_info': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reluctant_treatment_info': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reluctant_villiage_info': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reported_total_red_flags': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'running_away_over_18': ('django.db.models.fields.BooleanField', [], {}),
            'running_away_under_18': ('django.db.models.fields.BooleanField', [], {}),
            'seen_in_last_month_in_nepal': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shopping_overnight_stuff_in_bags': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'staff_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'talked_to_aunt_uncle': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'talked_to_brother': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'talked_to_father': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'talked_to_grandparent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'talked_to_mother': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'talked_to_other': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'talked_to_other_value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'talked_to_sister': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'time': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'traveling_with_someone_not_with_her': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'under_18_cant_contact_family': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'under_18_family_doesnt_know': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'under_18_family_unwilling': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'valid_gulf_country_visa': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'where_going': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'who_in_group': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'wife_under_18': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['dataentry']