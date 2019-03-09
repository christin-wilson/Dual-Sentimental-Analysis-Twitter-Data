from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Tweet(models.Model):
	id_num=models.BigIntegerField(default=0)
	id_str=models.CharField(max_length=30)
	set_num=models.BigIntegerField(default=0)
	user_query= models.CharField(max_length=200)
	user_name = models.CharField(max_length=200)
	user_id_str = models.CharField(max_length=200)
	tweet_text = models.CharField(max_length=200)
	created_at = models.DateTimeField('date created')
	retweet_count = models.IntegerField(default=0)
	favourite_count = models.IntegerField(default=0)
	tweet_sentiment = models.IntegerField(default=-1)
		# tweet_sentiment 2 = neutral ; 0 = positive ; 1 = negative

class FeatureVector(models.Model):
	id_num=models.BigIntegerField(default=0)
	set_num=models.BigIntegerField(default=0)
	feature= models.CharField(max_length=500)
	user_query=models.CharField(max_length=200, default='test')
	tweet_sentiment = models.IntegerField(default=-1)

class History(models.Model):
	id = models.AutoField(primary_key=True)
	user_query=models.CharField(max_length=200)
	timestamp=models.DateTimeField(auto_now=True)
	positive=models.IntegerField(default=0)
	negative=models.IntegerField(default=0)
	neutral=models.IntegerField(default=0)
	feature_list=models.CharField(max_length=500)
	