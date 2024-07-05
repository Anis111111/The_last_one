from django.contrib import admin
from .models import *

from import_export.admin import ImportExportModelAdmin

# Register your models here.

admin.site.register(Student)
# @admin.register(Student)
# class ProjectImportExport(ImportExportModelAdmin):
#     pass

class StudentGroupAdmin(admin.ModelAdmin):
    _meta = "__all__"
    readonly_fields = ('is_published',) 
    list_display = ('project_idea', 'admin', 'is_published')

admin.site.register(StudentGroup,StudentGroupAdmin)

