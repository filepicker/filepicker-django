from django.shortcuts import render

try:
    from .models import BasicFilesForm, FileForm
except ImportError:
    from models import BasicFilesForm, FileForm


def pick(request):
    message = None
    basic_form = BasicFilesForm()
    form = FileForm()

    if request.method == "POST":
        post = request.POST.dict()
        basic_form = BasicFilesForm(post)
        if basic_form.is_valid():
            f = basic_form.save()
            post['mid_id'] = f.id
        else:
            message = 'Invalid form'

        files_links = request.POST['fpfile'].split(',')
        if post.get('mid_id', None):
            for i, f in enumerate(request.FILES.getlist("fpfile")):
                form = FileForm(post)
                if form.is_valid():
                    fp = form.save(commit=False)
                    fp.fpfile = f
                    fp.fpurl = files_links[i]
                    fp.mid_id = post.get('mid_id')
                    fp.save()
                else:
                    message = "Invalid form"
            files = ", ".join([str(f) for f in request.FILES.getlist("fpfile")])
            message = "Save successful. URL for {0}: {1}".format(
                files, request.POST["fpfile"]) if not message else message

    return render(request, "home.html", {'form': form, 'message': message, 'basic_form': basic_form})