from django.contrib import admin
from .models import *

from import_export.admin import ImportExportModelAdmin

# Register your models here.

class ProjectFields(admin.ModelAdmin):
    _meta = "__all__"
    readonly_fields = ['status','description']
    list_display = ['title','description','project_type','status','FramworksFrontend', 'FramworksMobileApps','FramworksBackend','created_at','updated_at','is_published' ]

    list_display_links = ['title']
    list_editable = ['status','FramworksFrontend', 'FramworksMobileApps','FramworksBackend'] # you should do this : if you add field in list_display_links do NOT add it here

    search_fields = ['title','FramworksFrontend', 'FramworksMobileApps','FramworksBackend']
    list_filter = ['is_published','created_at','updated_at']

    # fields = ['admin','project_idea']

admin.site.register(Project,ProjectFields)

# admin.site.register(Project)
# @admin.register(Project)
# class ProjectImportExport(ImportExportModelAdmin):
#     pass