# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-03 04:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front_end', '0005_tweet_tweet_sentiment'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeatureVector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_num', models.BigIntegerField(default=0)),
                ('feature', models.CharField(max_length=500)),
            ],
        ),
    ]
