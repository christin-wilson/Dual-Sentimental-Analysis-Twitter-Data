from celery.task import Task
from celery.registry import tasks

from .models import Tweet
from .models import FeatureVector
from .models import History
import re
import os
import json
from svm import *
from svmutil import *
import csv
from collections import Counter

#initialize stopWords
stopWords = []
pwd = os.path.dirname(__file__)
classifierDumpFile = pwd+'/trainedModels/model.txt'
#classifierDumpFile = pwd+'/trainedModels/svm_trained_model.txt'


def get_tweet(query,limit):
	#Warning:This code is blocking type
	#Should be replaced with node.js or celery or something else :P
	from tweepy import Stream
	from tweepy import OAuthHandler
	from tweepy.streaming import StreamListener
	import tweepy
    #test responce
	#test over
	ckey ='LvOQ2plBMV6Ac3wsNeOPIrEJC'
	csecret = 'Hrd4QiS7ro2jfIdzfkB2iO76VdNIW6ZaAPDrjku9h8enQgB2pM'
	atoken = '4518935234-KokgDnoVJdIP7u3MyyABGsi4Mm35qCwf38c9WX0'
	asecret ='BUYPidZE2NwuTSfzFxFPKjjA6pru9reWCJEQzu5FhVFxy'

	auth = tweepy.OAuthHandler(ckey, csecret)
	auth.set_access_token(atoken, asecret)

	count=0
	api = tweepy.API(auth)

	print("\nYou gave me this: "+query)
	
	for tweet in tweepy.Cursor(api.search,q=query,lang="en",show_user="true").items(int(limit)):
	  if not tweet.retweeted and 'RT @' not in tweet.text:
		t=Tweet() #creating tweet model object
		t.user_query=query
		t.id_num=tweet.id
		t.id_str=tweet.id_str
		print("Tweet : "+ tweet.text)
		t.tweet_text=tweet.text
		t.created_at=tweet.created_at
		t.user_name=tweet.user.name
		t.user_id_str=tweet.user.id_str
		#t.favourite_count=tweet.favourites_count
		t.retweet_count=tweet.retweet_count
		t.set_num=0
		t.save()
		print("\nInserted\n")
	
	print("\n\n================DONE===============\n\n")
	return 1

def Process_tweet(query):
	print("\n\n================PREPROCESSING===============\n\n")

	global stopWords 
	stopWords = getStopWordList()
	#print stopWords
	H=History()
	H.save()

	positive = 0
	negative = 0
	neutral = 0
	word_list=[]

	for tweet in Tweet.objects.filter(user_query=query,set_num=0):
	    #convert to lower case
	    #tweet.tweet_text=tweet.tweet_text.lower()
	    #remove URL's
	    #tweet.tweet_text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet.tweet_text)
	    # remove @user
	    #tweet.tweet_text = re.sub('@[^\s]+','AT_USER',tweet.tweet_text)
	    #Remove additional white spaces
	    #tweet.tweet_text = re.sub('[\s]+', ' ', tweet.tweet_text)
	    #Replace #word with word
	    #tweet.tweet_text = re.sub(r'#([^\s]+)', r'\1', tweet.tweet_text)
	    #trim
	    #tweet.tweet_text = tweet.tweet_text.strip('\'"')

	    ProcessedText=processTweet(tweet.tweet_text)
	    

	    # retrieve feature vector 
	    f = FeatureVector()
	    fw = getFeatureVector(ProcessedText)
	    f.id_num=tweet.id_num
	    f.feature=json.dumps(fw)
	    for element in fw:
	    	word_list.append(str(element))
		#retrieve tweet sentiment
	    f.tweet_sentiment=classifiyTweet(fw)
	    tweet.tweet_sentiment=f.tweet_sentiment

	    if f.tweet_sentiment == 0 :
	    	positive += 1
	    elif f.tweet_sentiment == 1 :
	    	negative += 1
	    elif f.tweet_sentiment == 2 :
	    	neutral += 1

	    f.user_query=tweet.user_query
	    # to convert back use x = json.loads(f.feature)

	    f.set_num=H.id
	    f.save()
	    tweet.save()

	    print "\nfeature vector : ", fw, "saved!\n"

	H.user_query=query
	H.positive=positive
	H.negative=negative
	H.neutral=neutral
	counts=Counter()
	counts = Counter(word_list).most_common(10)
	H.feature_list=counts

	if not( positive == 0 and negative==0 and neutral ==0 ) :
		H.save()

	print("\n\n================DONE===============\n\n")



def processTweet(text):
	#convert to lower case
	text=text.lower()
	#remove URL's
	text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',text)
	# remove rt @user
	text = re.sub('rt @[^\s]+','AT_USER',text)
	# remove @user
	text = re.sub('@[^\s]+','AT_USER',text)
	#Remove additional white spaces
	text = re.sub('[\s]+', ' ', text)
	#Replace #word with word
	text = re.sub(r'#([^\s]+)', r'\1', text)
	#trim
	text = text.strip('\'"')

	return text




################################################# feature vector extraction		

#start replaceTwoOrMore
def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)
#end

#start getStopWordList
def getStopWordList():
    stopWordListFileName = '/data/feature_list/stop_words_copy.txt'
    #read the stopwords file and build a list
    stopWords=[]
    stopWords.append('AT_USER')
    stopWords.append('URL')

    pwd = os.path.dirname(__file__)
    #print "\n XXXX ", pwd

    fp = open(pwd+stopWordListFileName, 'r')
    
    line = fp.readline()
    while line:
        word = line.strip()
        stopWords.append(word)
        line = fp.readline()
    fp.close()
    return stopWords
#end

#start getfeatureVector
def getFeatureVector(tweet):
    global stopWords 
   
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
#end


def classifiyTweet(featureVector):
	global classifierDumpFile
	global stopWords
	featureList=[]
	tweets = []
	sentiment = -1 
	featureList.extend(featureVector)
	tweets.append((featureVector, sentiment));
	# Remove featureList duplicates	
	featureList = list(set(featureList))

	#load_model
	classifier = svm_load_model(classifierDumpFile)
	test_feature_vector = getSVMFeatureVector(tweets, featureList)
	p_labels, p_accs, p_vals = svm_predict([0] * len(test_feature_vector),test_feature_vector, classifier)
	print featureVector
	print p_labels[0]
	return p_labels[0]




################################################# feature vector extraction



################################################# training using marked tweets

#Read the tweets one by one and process it
def train_system() :



	global classifierDumpFile

    #print "\n XXXX ", pwd
    #fp = open(pwd+stopWordListFileName, 'r')
	#inpTweets = csv.reader(open(pwd+'/data/sampleTweets.csv', 'rb'), delimiter=',', quotechar='|')
	
	

	inpTweets = csv.reader(open(pwd+'/data/full_training_dataset.csv', 'rb'), delimiter=',', quotechar='\"')
	featureList = []
	global stopWords
	stopWords = getStopWordList()

	count = 0 
	# Get tweet words
	print "\nPreProcessing Tweets : "
	tweets = []
	for row in inpTweets:
		count = count+1
		print " ", count
		sentiment = row[0]
		tweet = row[1]
		processedTweet = processTweet(tweet)
		featureVector = getFeatureVector(processedTweet)	
		featureList.extend(featureVector)
		tweets.append((featureVector, sentiment));
	#end loop

	print "\nRemoving featureList duplicates..."	
	featureList = list(set(featureList))

	# Extract feature vector for all tweets in one shote
	#training_set = nltk.classify.util.apply_features(extract_features, tweets)
	

	
	#training of the system - not to be executed again
	#already trained 
	print "\nCreating SVM Feature Vector And Labels..."
	result = getSVMFeatureVectorAndLabels(tweets,featureList)

	#print result

	print "\n## Training started"
	#Train the classifier
	print "\nDefining Classes and corresponding Vectors..."
	problem = svm_problem(result['labels'], result['feature_vector'])
	#'-q' option suppress console output
	print "\nDefining SVM parameters..."
	param = svm_parameter('-q')
	param.kernel_type = LINEAR
	classifier = svm_train(problem, param)
	svm_save_model(classifierDumpFile, classifier)

	print("#######Testing Output ##########")
	#load_model
	classifier = svm_load_model(classifierDumpFile)
	#Test the classifier
	test_feature_vector = getSVMFeatureVector(tweets, featureList)
	#p_labels contains the final labeling result

	#print "\n\n", test_feature_vector
	p_labels, p_accs, p_vals = svm_predict([0] * len(test_feature_vector),test_feature_vector, classifier)

	print "\np_labels 	: ", p_labels[0]
	print "\np_accs		: ", p_accs[0]
	#print "\np_vals		: ", p_vals


#have to change this function
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



def getSVMFeatureVectorAndLabels(tweets, featureList):
    sortedFeatures = sorted(featureList)
    map = {}
    feature_vector = []
    labels = []
    for t in tweets:
        label = 0
        map = {}
        #Initialize empty map
        for w in sortedFeatures:
            map[w] = 0

        tweet_words = t[0]
        tweet_opinion = t[1]
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
        if(tweet_opinion == 'positive'):
            label = 0
        elif(tweet_opinion == 'negative'):
            label = 1
        elif(tweet_opinion == 'neutral'):
            label = 2
        labels.append(label)
    #return the list of feature_vector and labels
    return {'feature_vector' : feature_vector, 'labels': labels}
#end

################################################# training using marked tweets




class DL_Task(Task):
    def run(self, query,limit, **kwargs):
        get_tweet(query,limit)
        Process_tweet(query)

class Train(Task):
	def run(self,**kwargs):
		train_system()



tasks.register(Train)
tasks.register(DL_Task)

