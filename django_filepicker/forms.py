from django import forms
from django.core.files import File
from django.conf import settings
from io import StringIO

try:
    from .utils import FilepickerFile
    from .widgets import FPFileWidget
except ImportError:
    from utils import FilepickerFile
    from widgets import FPFileWidget

class FPFieldMixin():
    widget = FPFileWidget
    default_mimetypes = "*/*"

    def initialize(self, apikey=None, mimetypes=None, services=None, additional_params=None):
        """
        Initializes the Filepicker field.
        Valid arguments:
        * apikey. This string is required if it isn't set as settings.FILEPICKER_API_KEY
        * mimetypes. Optional, the allowed mimetypes for files. Defaults to "*/*" (all files)
        * services. Optional, the allowed services to pull from.
        * additional_params. Optional, additional parameters to be applied.
        """

        self.apikey = apikey or getattr(settings, 'FILEPICKER_API_KEY', None)
        if not self.apikey:
            raise Exception("Cannot find filepicker.io api key." +
            " Be sure to either pass as the apikey argument when creating the FPFileField," +
            " or set it as settings.FILEPICKER_API_KEY. To get a key, go to https://filepicker.io")

        self.mimetypes = mimetypes or self.default_mimetypes
        if not isinstance(self.mimetypes, str):
            #If mimetypes is an array, form a csv string
            try:
                self.mimetypes = ",".join(iter(self.mimetypes))
            except TypeError:
                self.mimetypes = str(self.mimetypes)

        self.services = services or getattr(settings, 'FILEPICKER_SERVICES', None)
        self.additional_params = additional_params or getattr(settings, 'FILEPICKER_ADDITIONAL_PARAMS', None)

    def widget_attrs(self, widget):
        attrs = {
                'data-fp-apikey': self.apikey,
                'data-fp-mimetypes': self.mimetypes,
                }

        if self.services:
            attrs['data-fp-option-services'] = self.services

        if self.additional_params:
            attrs = dict(list(attrs.items()) + list(self.additional_params.items()))            

        return attrs


class FPUrlField(FPFieldMixin, forms.URLField):
    widget = FPFileWidget
    default_mimetypes = "*/*"

    def __init__(self, *args, **kwargs):
        """
        Initializes the Filepicker url field.
        Valid arguments:
        * apikey. This string is required if it isn't set as settings.FILEPICKER_API_KEY
        * mimetypes. Optional, the allowed mimetypes for files. Defaults to "*/*" (all files)
        * services. Optional, the allowed services to pull from.
        * additional_params. Optional, additional parameters to be applied.
        """
        self.initialize(
            apikey=kwargs.pop('apikey', None),
            mimetypes=kwargs.pop('mimetypes', None),
            services=kwargs.pop('services', None),
            additional_params=kwargs.pop('additional_params', None),
        )
        super(FPUrlField, self).__init__(*args, **kwargs)


class FPFileField(FPFieldMixin, forms.FileField):
    def __init__(self, *args, **kwargs):
        """
        Initializes the Filepicker url field.
        Valid arguments:
        * apikey. This string is required if it isn't set as settings.FILEPICKER_API_KEY
        * mimetypes. Optional, the allowed mimetypes for files. Defaults to "*/*" (all files)
        * services. Optional, the allowed services to pull from.
        * additional_params. Optional, additional parameters to be applied.
        """
        self.initialize(
            apikey=kwargs.pop('apikey', None),
            mimetypes=kwargs.pop('mimetypes', None),
            services=kwargs.pop('services', None),
            additional_params=kwargs.pop('additional_params', None),
        )
        super(FPFileField, self).__init__(*args, **kwargs)

    def to_python(self, data):
        """Takes the url in data and creates a File object"""
        try:
            fpf = FilepickerFile(data)
        except ValueError as e:
            if 'Not a filepicker.io URL' in str(e):
                # Return None for invalid URLs
                return None
            else:
                # Pass the buck
                raise e
        else:
            return fpf.get_file(self.additional_params)
