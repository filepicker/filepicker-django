from django.db import models
from django.utils.translation import ugettext_lazy

import forms


class FPFileField(models.FileField):
    description = ugettext_lazy("A File selected using Filepicker.io")

    def __init__(self, *args, **kwargs):
        """
        Initializes the Filepicker file field.
        Valid arguments:
        * apikey. This string is required if it isn't set as settings.FILEPICKER_API_KEY
        * mimetypes. Optional, the allowed mimetypes for files. Defaults to "*/*" (all files)
        """
        self.apikey = kwargs.pop("apikey", None)
        self.mimetypes = kwargs.pop("mimetypes", None)

        super(FPFileField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.FPFileField,
                'max_length': self.max_length}

        if 'initial' in kwargs:
            defaults['required'] = False

        if self.apikey:
            defaults['apikey'] = self.apikey
        if self.mimetypes:
            defaults['mimetypes'] = self.mimetypes

        defaults.update(kwargs)
        return super(FPFileField, self).formfield(**defaults)
