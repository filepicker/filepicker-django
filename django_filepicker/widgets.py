from django.conf import settings
from django.forms import widgets
from django.utils.html import escape
from django.utils.translation import ugettext as _


#JS_URL is the url to the filepicker.io javascript library
JS_VERSION = 0
JS_URL = "//api.filepicker.io/v%d/filepicker.js" % (JS_VERSION)

if hasattr(settings, 'FILEPICKER_INPUT_TYPE'):
    INPUT_TYPE = settings.FILEPICKER_INPUT_TYPE
else:
    INPUT_TYPE = 'filepicker-dragdrop'


class FPFileWidget(widgets.Input):
    input_type = INPUT_TYPE
    needs_multipart_form = False

    def build_attrs(self, *args, **kwargs):
        attrs = super(FPFileWidget, self).build_attrs(*args, **kwargs)
        attrs.update({
            'data-fp-button-text': escape(_('Pick File')),
            'data-fp-drag-text': escape(_('Or drop files here')),
        })
        return attrs

    def value_from_datadict_old(self, data, files, name):
        #If we are using the middleware, then the data will already be
        #in FILES, if not it will be in POST
        if name not in data:
            return super(FPFileWidget, self).value_from_datadict(
                    data, files, name)

        return data

    class Media:
        js = (JS_URL,)
