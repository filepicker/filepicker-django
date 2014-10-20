django-filepicker
=================

A django plugin to make integrating with Filepicker.io even easier

##Installation

  1.  Install the python package:

          pip install django-filepicker

  2.  Add your file picker api key to your settings.py file. You api key can be
  found in the [developer portal](https://developers.inkfilepicker.com/apps/).

          FILEPICKER_API_KEY = <your api key>

  3.  Configure your media root.

          CWD = os.getcwd()
          MEDIA_ROOT = os.path.join(CWD, 'media')

  3.  Add a filepicker field to your model and set the upload_to value.

          fpfile = django_filepicker.models.FPFileField(upload_to='uploads')

  4.  Modify your view to accept the uploaded files along with the post data.

          form = models.TestModelForm(request.POST, request.FILES)
          if form.is_valid():
              #Save will read the data and upload it to the location
              # defined in TestModel
              form.save()

  5.  Add the form.media variable above your other JavaScript calls.

          <head>
              <title>Form Template Example</title>
              <!--  Normally this would go into a block defined in base.html that
                    occurs before other JavaScript calls. -->
              {{ form.media }}
          </head>

          <body>
              <form method="POST" action="/" enctype="multipart/form-data">
                  {{ form.as_p }}
                  <input type="submit" />
              </form>
          </body>

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
Similarly with the `FPFileField` for models, the filepicker django library defines a `FPFileField` for forms as well, that likewise serves as a drop-in replacement for the standard django `FileField`. There is also the `FPUrlField` if you want to store the Filepicker.io URL instead

###Middleware
Also included is a middleware library that will take any Filepicker.io urls passed to the server, download the contents, and place the result in request.FILES. This way, you can keep your backend code for handling file uploads the same as before while adding all the front-end magic that Filepicker.io provides

If you have any questions, don't hesitate to reach out at [contact@filepicker.io](mailto:contact@filepicker.io). For more information, see [https://filepicker.io](https://www.filepicker.io)

Open-sourced under the MIT License. Pull requests encouraged!
