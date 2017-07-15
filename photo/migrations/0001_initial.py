# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-15 16:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalogs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=b'', verbose_name=b'\xd0\xa1\xd1\x81\xd1\x8b\xd0\xbb\xd0\xba\xd0\xb0 \xd0\xbd\xd0\xb0 \xd1\x84\xd0\xbe\xd1\x82\xd0\xbe')),
                ('name', models.CharField(max_length=255, verbose_name=b'\xd0\x9d\xd0\xb0\xd0\xb7\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5')),
                ('catalog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogs.Catalog')),
            ],
            options={
                'db_table': 'photos',
                'verbose_name': '\u0424\u043e\u0442\u043e',
                'verbose_name_plural': '\u0424\u043e\u0442\u043e\u0433\u0430\u0440\u0430\u0444\u0438\u0438',
            },
        ),
    ]