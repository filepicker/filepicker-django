# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_filepicker.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=64)),
                ('fpfile', django_filepicker.models.FPFileField(upload_to=b'uploads')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
