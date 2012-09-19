from django.shortcuts import render

import models


def home(request):
    message = None
    if request.method == "POST":
        print "POST parameters: ", request.POST
        print "Files: ", request.FILES

        #building the form - automagically turns the uploaded fpurl into a File object
        form = models.TestModelForm(request.POST, request.FILES)
        if form.is_valid():
            #Save will read the data and upload it to the location defined in TestModel
            form.save()

            #Reading the contents of the file
            fpfile = form.cleaned_data['fpfile']
            #Since we already read from it in save(), we'll want to seek to the beginning first
            fpfile.seek(0)
            print fpfile.read()

            message = "Save successful. URL for %s: %s" % (fpfile.name, request.POST['fpfile'])

        message = "Invalid form"
    else:
        form = models.TestModelForm()

    return render(request, "home.html", {'form': form, 'message': message})
