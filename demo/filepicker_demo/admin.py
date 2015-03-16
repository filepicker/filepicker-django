from django.contrib import admin
from models import FileModel, BasicFilesModel


class BasicFilesModelAdmin(admin.ModelAdmin):
    pass


class FileModelAdmin(admin.ModelAdmin):
    pass


admin.site.register(FileModel, FileModelAdmin)
admin.site.register(BasicFilesModel, BasicFilesModelAdmin)