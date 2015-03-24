from django.contrib import admin
from models import FileModel, BasicFilesModel


class BasicFilesModelAdmin(admin.ModelAdmin):
    pass


class FileModelAdmin(admin.ModelAdmin):
    readonly_fields = ('image_tag',)
    list_display = ('__unicode__', 'image_tag')


admin.site.register(FileModel, FileModelAdmin)
admin.site.register(BasicFilesModel, BasicFilesModelAdmin)