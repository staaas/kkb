# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'CinemaClub'
        db.create_table('cinemaclubs_cinemaclub', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=150)),
            ('mission', self.gf('django.db.models.fields.CharField')(default='', max_length=300)),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal('cinemaclubs', ['CinemaClub'])

        # Adding model 'CinemaClubEvent'
        db.create_table('cinemaclubs_cinemaclubevent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organizer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cinemaclubs.CinemaClub'])),
            ('starts_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('ends_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('poster', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=150)),
            ('short_description', self.gf('django.db.models.fields.CharField')(default='', max_length=500, db_column='short_desciption')),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal('cinemaclubs', ['CinemaClubEvent'])


    def backwards(self, orm):
        
        # Deleting model 'CinemaClub'
        db.delete_table('cinemaclubs_cinemaclub')

        # Deleting model 'CinemaClubEvent'
        db.delete_table('cinemaclubs_cinemaclubevent')


    models = {
        'cinemaclubs.cinemaclub': {
            'Meta': {'object_name': 'CinemaClub'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'mission': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'cinemaclubs.cinemaclubevent': {
            'Meta': {'object_name': 'CinemaClubEvent'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'ends_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'}),
            'organizer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cinemaclubs.CinemaClub']"}),
            'poster': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'short_description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'db_column': "'short_desciption'"}),
            'starts_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        }
    }

    complete_apps = ['cinemaclubs']
