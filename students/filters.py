import django_filters
from .models import *



class StudentFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexaxt')
    keyword = django_filters.filters.CharFilter(field_name='name',lookup_expr='icontains')

    class Meta:
        model = Student
        fields = ('name'  ,'university_id','group','specialization', 'keyword' ) # i wont to add ID field 

