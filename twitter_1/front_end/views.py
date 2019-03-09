from django.shortcuts import render
from django.http import HttpResponse

from django.template import loader

#Celery import

from front_end.tasks import DL_Task
from front_end.tasks import Train
from celery.result import AsyncResult



from .models import Tweet
from .models import FeatureVector
from .models import History

import os 

def train(request):
	task=Train.delay()
	return HttpResponse("Training")
	


# Create your views here.
def index(request):
	template=loader.get_template('front_end/index.html') 
	return HttpResponse(template.render())

def process(request):
	task=DL_Task.delay(query=request.GET['tw_query'], limit=request.GET['tw_limit'])
	template=loader.get_template('front_end/process.html')
	if ('stock_option' not in request.GET):
		stock_option="No"
	else:
		stock_option=request.GET['stock_option']
	return HttpResponse(template.render({'task_id': task,'tw_query': request.GET['tw_query'],'stock_option':stock_option,'stock_symbol':request.GET['stock_symbol']},request))



def view_entries(request):
	pwd = os.path.dirname(__file__)
	if('tw_query' not in request.GET):
		k = Tweet.objects.all()
		f = FeatureVector.objects.all()
		p = []
		for t in k :
			for s in f :
				if t.id_num == s.id_num :
					p.append((t,s))

		context = {
		'tweet_list' : p,
		'query' : "",
		'path' : pwd,
		'count' : len(k), 
		}
	else:
		k=Tweet.objects.filter(user_query=request.GET['tw_query'])
		h=History.objects.filter(user_query=request.GET['tw_query'])
		f=FeatureVector.objects.filter(user_query=request.GET['tw_query'])
		p = []
		for t in k :
			for s in f :
				if t.id_num == s.id_num :
					p.append((t,s))

		context = {
		'tweet_list' : p,
		'query' : request.GET['tw_query'],
		'path' : pwd,
		'history' :h,
		'last_history':h.order_by("-id")[0],
		'count' : len(k),
		}
		if('stock_option' in request.GET and 'stock_symbol' in request.GET):
			if(request.GET["stock_option"]=="on"):
				context.update({'stock_option' : request.GET["stock_option"],'stock_symbol' : request.GET["stock_symbol"]})
	response="done"
	template=loader.get_template('front_end/tweets.html')

	print("\nStored Tweets : ")
	

	return HttpResponse(template.render(context,request))	

def check_process(request):
	task_id=request.GET['task_id']
	results = DL_Task.AsyncResult(task_id) 
	if results.ready():
	    return HttpResponse("Done")
	return HttpResponse("not_ready")

def delete(request):
	if('user_query' not in request.GET):
		Tweet.objects.all().delete()
		FeatureVector.objects.all().delete()
	elif (request.GET['user_query'] == ""):
		Tweet.objects.all().delete()
		FeatureVector.objects.all().delete()
	else:
		Tweet.objects.filter(user_query=request.GET['user_query']).delete()
		FeatureVector.objects.filter(user_query=request.GET['user_query']).delete()
	response="success"
	return HttpResponse(response)


