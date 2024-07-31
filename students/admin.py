from django.contrib import admin
from .models import *

from import_export.admin import ImportExportModelAdmin

# Register your models here.

# admin.site.register(Student)
@admin.register(Student)
class ProjectImportExport(ImportExportModelAdmin):
    pass

class StudentGroupAdmin(admin.ModelAdmin):
    _meta = "__all__"
    readonly_fields = ('is_published',) 
    list_display = ['project_idea', 'admin', 'is_published']

    list_display_links = ['admin']
    list_editable = ['project_idea'] # you should do this : if you add field in list_display_links do NOT add it here

    search_fields = ['admin']
    list_filter = ['is_published', 'admin']

    # fields = ['admin','project_idea']

admin.site.register(StudentGroup,StudentGroupAdmin)

