from django.contrib import admin
from .models import *

from import_export.admin import ImportExportModelAdmin
# Register your models here.
admin.site.site_header = "Nouvil"
admin.site.site_title = "Nouvil"
admin.site.register(Profile)
# @admin.register(Profile)
# class ProjectImportExport(ImportExportModelAdmin):
#     pass