from django.shortcuts import render

import models


def home(request):
    if request.method == "POST":
        print 'create'
        form = models.TestModelForm(request.POST, request.FILES)
        print request.POST
        if form.is_valid():
            print "valid"
            form.save()
    else:
        form = models.TestModelForm()

    return render(request, "home.html", {'form': form})
