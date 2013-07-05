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
        * services. Optional, the allowed services to pull from.
        * additional_params. Optional, additional parameters to be applied.
        """
        self.apikey = kwargs.pop("apikey", None)
        self.mimetypes = kwargs.pop("mimetypes", None)
        self.services = kwargs.pop("services", None)
        self.additional_params=kwargs.pop("additional_params", None)

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
        if self.services:
            defaults['services'] = self.services
        if self.additional_params:
            defaults['additional_params'] = self.additional_params

        defaults.update(kwargs)
        return super(FPFileField, self).formfield(**defaults)
        
try:
    # For South. See: http://south.readthedocs.org/en/latest/customfields.html#extending-introspection
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["django_filepicker\.models\.FPFileField"])
except ImportError:
    pass
