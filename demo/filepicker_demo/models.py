from django.db import models
from django import forms
import django_filepicker


class BasicFilesModel(models.Model):
    text = models.CharField(max_length=64)

    def __unicode__(self):
        return 'Files chain {}. ID:{}'.format(self.text, self.pk)


class FileModel(models.Model):
    mid = models.ForeignKey(BasicFilesModel)
    fpfile = django_filepicker.models.FPFileField(
        upload_to='uploads', additional_params={'data-fp-multiple': 'true'})
    fpurl = models.URLField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return 'File from chain {}:id-{}. ID:{}'.format(
            self.mid.text, self.mid.pk, self.pk)

    def image_tag(self):
        return u'<img src="%s" />' % self.fpurl
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True


class BasicFilesForm(forms.ModelForm):
    class Meta:
        model = BasicFilesModel
        fields = ['text']


class FileForm(forms.ModelForm):
    class Meta:
        model = FileModel
        fields = ['fpfile']