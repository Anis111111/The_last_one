from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from .models import *



# Register your models here.
admin.site.site_header = "Azax" # Azax , Nouvil
admin.site.site_title = "Azax"

class ProfilesAdv(admin.ModelAdmin):
    _meta = "__all__"
    readonly_fields = ('id',) 
    list_display = ['id','user','age','phone','address','img' ]

    list_display_links = ['user']
    list_editable = ['phone','address','age'] # you should do this : if you add field in list_display_links do NOT add it here

    search_fields = ['user','phone']
    list_filter = ['age', 'address']

    # fields = ['admin','project_idea']

admin.site.register(Profile,ProfilesAdv)


# @admin.register(Profile)
# class ProjectImportExport(ImportExportModelAdmin):
#     pass

