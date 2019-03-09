import re
import csv
from svm import *
from svmutil import *
import nltk


classifierDumpFile = 'data/model.txt'


def train_system() :



	global classifierDumpFile

    #print "\n XXXX ", pwd
    #fp = open(pwd+stopWordListFileName, 'r')
	#inpTweets = csv.reader(open(pwd+'/data/sampleTweets.csv', 'rb'), delimiter=',', quotechar='|')
	
	

	inpTweets = csv.reader(open('data/full_training_dataset.csv', 'rb'), delimiter=',', quotechar='\"')
	featureList = []
	global stopWords
	stopWords = getStopWordList('data/stopwords.txt')

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
		featureVector = getFeatureVector(processedTweet,stopWords)	
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

#start getStopWordList
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

#start replaceTwoOrMore
def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)
#end

st = open('data/stopwords.txt', 'r')
#stopWords = getStopWordList('data/stopwords.txt')

train_system()