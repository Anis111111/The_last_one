from django.urls import path
from . import views
from . import api_view


urlpatterns = [
    path('students/',api_view.StudentsAPIList.as_view(), name = 'api_students'),
    path('student/<str:pk>/', api_view.StudentAPIDetail.as_view() , name = 'api_get_by_id'),
    path('student/new/', api_view.new_student , name = 'api_new_student'),
    path('student/update/<str:pk>/', api_view.StudentAPIDetail.as_view() , name = 'api_update_student'),
    path('student/delete/<str:pk>/', api_view.StudentAPIDetail.as_view() , name = 'api_delete_student'),

]
