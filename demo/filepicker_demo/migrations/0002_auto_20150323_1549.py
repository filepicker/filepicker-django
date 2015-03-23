# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_filepicker.models


class Migration(migrations.Migration):

    dependencies = [
        ('filepicker_demo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BasicFilesModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=64)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FileModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fpfile', django_filepicker.models.FPFileField(upload_to=b'uploads')),
                ('fpurl', models.URLField(max_length=255, null=True, blank=True)),
                ('mid', models.ForeignKey(to='filepicker_demo.BasicFilesModel')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='TestModel',
        ),
    ]
