from __future__ import absolute_import, print_function

import tweepy
import re
import os
import json
import nltk
from svm import *
from svmutil import *
import csv
from collections import Counter


classifierDumpFile = 'data/modelj.txt'


def classifiyTweet(featureVector):
	global classifierDumpFile
	global stopWords
	featureList=[]
	tweets = []
	sentiment = -1 
	with open("data/featurelist.txt", 'r') as f:
		featureList = [line.rstrip('\n') for line in f]

	featureList.extend(featureVector)
	tweets.append((featureVector, sentiment));
	# Remove featureList duplicates	
	featureList = list(set(featureList))

	#load_model
	classifier = svm_load_model(classifierDumpFile)
	test_feature_vector = getSVMFeatureVector(tweets, featureList)
	p_labels, p_accs, p_vals = svm_predict([0] * len(test_feature_vector),test_feature_vector, classifier)
	print (featureVector)
	print (p_labels[0])
	return p_labels[0]

def getSVMFeatureVector(tweets, featureList):
	sortedFeatures = sorted(featureList)
	map = {}
	feature_vector = []
	for t in tweets:
		map = {}
		#Initialize empty map
		for w in sortedFeatures:
			map[w] = 0

		tweet_words = t[0]
		#Fill the map
		for word in tweet_words:
			#process the word (remove repetitions and punctuations)
			word = replaceTwoOrMore(word)
			word = word.strip('\'"?,.')
			#set map[word] to 1 if word exists
			if word in map:
				map[word] = 1
		#end for loop
		values = map.values()
		feature_vector.append(values)
	
	#return the list of feature_vector and labels
	return feature_vector
#end	

#start replaceTwoOrMore
def replaceTwoOrMore(s):
	#look for 2 or more repetitions of character and replace with the character itself
	pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
	return pattern.sub(r"\1\1", s)
#end

#start process_tweet
def processTweet(tweet):
	# process the tweets

	#Convert to lower case
	tweet = tweet.lower()
	#Convert www.* or https?://* to URL
	tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
	#Convert @username to AT_USER
	tweet = re.sub('@[^\s]+','AT_USER',tweet)
	#Remove additional white spaces
	tweet = re.sub('[\s]+', ' ', tweet)
	#Replace #word with word
	tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
	#trim
	tweet = tweet.strip('\'"')
	return tweet
#end

def getStopWordList(stopWordListFileName):
	#read the stopwords file and build a list
	stopWords = []
	stopWords.append('AT_USER')
	stopWords.append('URL')

	fp = open(stopWordListFileName, 'r')
	line = fp.readline()
	while line:
		word = line.strip()
		stopWords.append(word)
		line = fp.readline()
	fp.close()
	return stopWords
#end

def getFeatureVector(tweet,stopWords):
	featureVector = []
	#split tweet into words
	words = tweet.split()
	for w in words:
		#replace two or more with two occurrences
		w = replaceTwoOrMore(w)
		#strip punctuation
		w = w.strip('\'"?,.')
		#check if the word stats with an alphabet
		val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
		#ignore if it is a stop word
		if(w in stopWords or val is None):
			continue
		else:
			featureVector.append(w.lower())
	return featureVector




def collect():
	st = open('data/stopwords.txt', 'r')
	stopWords = getStopWordList('data/stopwords.txt')
	positive=0
	negative=0
	neutral=0

	word_list=[]

	consumer_key="LfyfmZTKVSKzVA97V6ZBviTSw"
	consumer_secret="D6yYbu3KeZ58LiSPuaMtygnXNxlS34EX5n4QrxRKKcJ5Pp8d6n"

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
	access_token="3593497752-38j0Z0LhWr1UBXVFtCUlPRHCsl33kbkGrPUNtxE"
	access_token_secret="vMBdncbvVunRWtcZaZFtgM5r7MA6KYlY6Dy7VUcQbIRA9"

	query=raw_input("Enter keyword ")
	limit=raw_input("Enter number of tweets ")

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth)
	text_file = open("data/abc.txt", "w")
	myfile = open('data/text.csv','a')

	for tweet in tweepy.Cursor(api.search, q=query,lang="en").items(int(limit)):
		tweets=tweet.text
		tweets1=tweets.encode('utf-8')
		text_file.write(tweets1)
		text_file.write("\n")
		ProcessedText=processTweet(tweets1)
		fw = getFeatureVector(ProcessedText,stopWords)
		for element in fw:
			word_list.append(str(element))
		#retrieve tweet sentiment
		tweet_sentiment=classifiyTweet(fw)

		if tweet_sentiment == 0 :
			positive += 1
		elif tweet_sentiment == 1 :
			negative += 1
		elif tweet_sentiment == 2 :
			neutral += 1

	print("\n\n================DONE===============\n\n")

	print("positve ")	
	print(positive)
	print("negative ")
	print(negative)
	print("neutral ")
	print(neutral)	
	#myfile = open('data/text.csv','a')
	#myfile.write(tweet.text)
	#myfile.write('\n'	) # adds a line between tweets
	#myfile.close()
	


	text_file.close()



collect()