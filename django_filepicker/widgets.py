from django.forms import widgets

INPUT_TYPE = 'filepicker-dragdrop'


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
