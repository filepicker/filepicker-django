from django.conf.urls import patterns, include, url
from django.contrib import admin
from filepicker_demo.views import pick


urlpatterns = patterns('',
	url(r'^$', pick, name='pick'),
)