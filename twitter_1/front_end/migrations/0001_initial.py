# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-05 09:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_query', models.CharField(max_length=200)),
                ('tweet_text', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(verbose_name='date created')),
                ('retweet_count', models.IntegerField(default=0)),
                ('favourite_count', models.IntegerField(default=0)),
            ],
        ),
    ]