from django.db import models
from django.utils.translation import ugettext_lazy

import forms


class FPFileField(models.FileField):
    description = ugettext_lazy("A File selected using Filepicker.io")

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.FPFileField,
                'max_length': self.max_length}

        if 'initial' in kwargs:
            defaults['required'] = False

        defaults.update(kwargs)
        return super(FPFileField, self).formfield(**defaults)
