import django_filters
from .models import *

# from pmarket.project.models import Project

class ProfessorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexaxt')
    keyword = django_filters.filters.CharFilter(field_name='name',lookup_expr='icontains')

    class Meta:
        model = Professor
        fields = ('name'  , 'keyword') # i wont to add ID field (, 'specialist')

