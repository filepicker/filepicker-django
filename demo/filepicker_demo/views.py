from django.shortcuts import render,redirect
from django.views.generic.base import View
from django.views.generic.base import TemplateView
from django.db import models
from django_filepicker.utils import FilepickerFile

try:
	from .models import TestModelForm
except ImportError:
	from models import TestModelForm

def pick(request):
    message = None
    if request.method == "POST":

        #building the form - automagically turns the uploaded fpurl into a File object
        form = TestModelForm(request.POST, request.FILES)
        if form.is_valid():
            #Save will read the data and upload it to the location defined in TestModel
            form.save()

            #Reading the contents of the file
            fpfile = form.cleaned_data['fpfile']
            #Since we already read from it in save(), we'll want to seek to the beginning first
            fpfile.seek(0)

            message = "Save successful. URL for %s: %s" % (fpfile.name, request.POST['fpfile'])
        else:
            message = "Invalid form"
    else:
        form = TestModelForm()

    return render(request, "home.html", {'form': form, 'message': message})