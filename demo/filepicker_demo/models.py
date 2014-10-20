from django.db import models
from django import forms
import django_filepicker


class TestModel(models.Model):
    #Text field just to show how the FPFileField goes along with normal controls
    text = models.CharField(max_length=64)

    #FPFileField is a field that will render as a filepicker dragdrop widget, but
    #When accessed will provide a File-like interface (so you can do fpfile.read(), for instance)
    fpfile = django_filepicker.models.FPFileField(upload_to='uploads', additional_params={'data-fp-multiple':'true'})

class TestModelForm(forms.ModelForm):
    class Meta:
        model = TestModel
        fields = ['text','fpfile']
