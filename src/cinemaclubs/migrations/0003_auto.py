# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding M2M table for field curators on 'CinemaClub'
        db.create_table('cinemaclubs_cinemaclub_curators', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('cinemaclub', models.ForeignKey(orm['cinemaclubs.cinemaclub'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('cinemaclubs_cinemaclub_curators', ['cinemaclub_id', 'user_id'])


    def backwards(self, orm):
        
        # Removing M2M table for field curators on 'CinemaClub'
        db.delete_table('cinemaclubs_cinemaclub_curators')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'cinemaclubs.cinemaclub': {
            'Meta': {'object_name': 'CinemaClub'},
            'curators': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'}),
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
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['cinemaclubs']
