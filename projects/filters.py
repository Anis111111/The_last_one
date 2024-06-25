import django_filters
from .models import *

class ProjectFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexaxt')
    keyword = django_filters.filters.CharFilter(field_name='title',lookup_expr='icontains')

    class Meta:
        model = Project
        fields = ('title' ,'project_type','status','is_published','keyword')


