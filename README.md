django-filepicker
=================

A django plugin to make integrating with Filepicker.io even easier

##Installation
`pip install django-filepicker`

##Demo
To see how all the pieces come together, see the example code in demo/, which you can run with the standard
`python manage.py runserver` command

###models.py
    import django_filepicker
    class TestModel(models.Model):
        #FPFileField is a field that will render as a filepicker dragdrop widget, but
        #When accessed will provide a File-like interface (so you can do fpfile.read(), for instance)
        fpfile = django_filepicker.models.FPFileField(upload_to='uploads')

###views.py
    #building the form - automagically turns the uploaded fpurl into a File object
    form = models.TestModelForm(request.POST, request.FILES)
    if form.is_valid():
        #Save will read the data and upload it to the location defined in TestModel
        form.save()

Be sure to also provide your Filepicker.io api key, either as a parameter to the FPFileField or in settings.py as `FILEPICKER_API_KEY`

##Components
###Models
The filepicker django library defines the `FPFileField` model field so you can get all the benefits of using Filepicker.io as a drop-in replacement for the standard django `FileField`. No need to change any of your view logic.

###Forms
Similarly with the `FPFileField` for models, the filepicker django library defines a `FPFileField` for forms as well, that likewise serves as a drop-in replacement for the standard django `FileField`

###Middleware
Also included is a middleware library that will take any Filepicker.io urls passed to the server, download the contents, and place the result in request.FILES. This way, you can keep your backend code for handling file uploads the same as before while adding all the front-end magic that Filepicker.io provides

If you have any questions, don't hesitate to reach out at [contact@filepicker.io](mailto:contact@filepicker.io). For more information, see [https://filepicker.io](https://www.filepicker.io)

Open-sourced under the MIT License. Pull requests encouraged!
