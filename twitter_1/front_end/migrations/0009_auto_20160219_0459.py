# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-19 04:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front_end', '0008_history'),
    ]

    operations = [
        migrations.AddField(
            model_name='featurevector',
            name='set_num',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tweet',
            name='set_num',
            field=models.BigIntegerField(default=0),
        ),
    ]