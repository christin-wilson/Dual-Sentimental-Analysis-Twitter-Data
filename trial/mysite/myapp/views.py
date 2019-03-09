from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import json
from collect import *
def register(request):
	if 'username' in request.COOKIES:
		usernamejudge = request.COOKIES['username']
		return HttpResponseRedirect('/')
	if request.method == 'POST':
		a = User.objects.filter(email = request.POST['email'])
		if len(a) != 0:
			form = UserForm()
			context = {"form" : form, "msg" : "Email already registered"}
			return render(request, "signup.html", context)
		form = UserForm(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit = False)
			instance.password = form.cleaned_data['email'] + "|" + form.cleaned_data['password']
			instance.save()
			os.system("mkdir " + os.getcwd() + '/media/' + form.cleaned_data['email'])
			response = redirect('/upload')
			response.set_cookie("username", form.cleaned_data['email'])
			return response
		else:
			form = UserForm()
			context = {"form" : form, "msg" : "Form not valid"}
			return render(request, "signup.html", context)
	else:
		form = UserForm()
		return render(request, "signup.html")


@csrf_exempt
def index(request):
	if request.method == 'POST':
		# print json.loads(request.body)
		search_term=request.POST.getlist('search_term')
		post_num=request.POST.getlist('post_num')

		return HttpResponse("Processed result to be displayed")
	else:
		return render(request,"sample.html")