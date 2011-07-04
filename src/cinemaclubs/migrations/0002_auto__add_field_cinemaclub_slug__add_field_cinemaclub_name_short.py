# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'CinemaClub.slug'
        db.add_column('cinemaclubs_cinemaclub', 'slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=40, db_index=True), keep_default=False)

        # Adding field 'CinemaClub.name_short'
        db.add_column('cinemaclubs_cinemaclub', 'name_short', self.gf('django.db.models.fields.CharField')(default='', max_length=40), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'CinemaClub.slug'
        db.delete_column('cinemaclubs_cinemaclub', 'slug')

        # Deleting field 'CinemaClub.name_short'
        db.delete_column('cinemaclubs_cinemaclub', 'name_short')


    models = {
        'cinemaclubs.cinemaclub': {
            'Meta': {'object_name': 'CinemaClub'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'mission': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'}),
            'name_short': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '40', 'db_index': 'True'}),
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
