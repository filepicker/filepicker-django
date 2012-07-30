from django.shortcuts import render

import models


def home(request):
    if request.method == "POST":
        form = models.TestModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = models.TestModelForm()

    return render(request, "home.html", {'form': form})
