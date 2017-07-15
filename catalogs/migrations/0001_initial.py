# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-15 16:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_tablespace=b'indexes', max_length=255, verbose_name=b'\xd0\x9d\xd0\xb0\xd0\xb7\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5')),
            ],
            options={
                'db_table': 'catalogs',
                'verbose_name': '\u041a\u0430\u0442\u0430\u043b\u043e\u0433',
                'verbose_name_plural': '\u041a\u0430\u0442\u0430\u043b\u043e\u0433\u0438',
            },
        ),
    ]
