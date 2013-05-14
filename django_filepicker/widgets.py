from django.conf import settings
from django.forms import widgets

#JS_URL is the url to the filepicker.io javascript library
JS_VERSION = getattr(settings, "FILEPICKER_JS_VERSION", 1)
JS_URL = "//api.filepicker.io/v%d/filepicker.js" % (JS_VERSION)

INPUT_TYPE = getattr(settings, "FILEPICKER_INPUT_TYPE", "filepicker-dragdrop")

class FPFileWidget(widgets.Input):
    input_type = INPUT_TYPE
    needs_multipart_form = False

    def value_from_datadict_old(self, data, files, name):
        #If we are using the middleware, then the data will already be
        #in FILES, if not it will be in POST
        if name not in data:
            return super(FPFileWidget, self).value_from_datadict(
                    data, files, name)

        return data

    class Media:
        js = (JS_URL,)
