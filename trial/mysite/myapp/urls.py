from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
import views

urlpatterns = [

	url(r'^$', views.index, name = 'Index'),
	
]


if settings.DEBUG:
		urlpatterns += [
			url(r'^media/(?P<path>.*)$', serve, {
				'document_root': settings.MEDIA_ROOT,
				}),
		]