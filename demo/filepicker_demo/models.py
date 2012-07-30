from django.db import models
from django import forms

import django_filepicker.models as fpmodels


class TestModel(models.Model):
    text = models.CharField(max_length=64)
    fpfile = fpmodels.FPFileField(upload_to='uploads')


class TestModelForm(forms.ModelForm):
    class Meta:
        model = TestModel
