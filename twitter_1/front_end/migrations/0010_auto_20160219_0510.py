# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-19 05:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front_end', '0009_auto_20160219_0459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]