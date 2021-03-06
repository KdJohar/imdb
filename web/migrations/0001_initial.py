# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-13 04:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, unique=True)),
                ('imdb_score', models.DecimalField(decimal_places=2, max_digits=2)),
                ('popularity', models.DecimalField(decimal_places=2, max_digits=3)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(max_length=255)),
                ('modified_by', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('director', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Director')),
                ('genre', models.ManyToManyField(to='web.Genre')),
            ],
        ),
    ]
