from django.contrib import admin
from .models import *

from import_export.admin import ImportExportModelAdmin

# Register your models here.

# admin.site.register(Project)
@admin.register(Project)
class ProjectImportExport(ImportExportModelAdmin):
    pass