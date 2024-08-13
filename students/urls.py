from django.urls import path
from . import views
from . import api_view


urlpatterns = [
    path('students/',api_view.StudentsAPIList.as_view(), name = 'api_students'),
    path('student/<str:pk>/', api_view.StudentAPIDetail.as_view() , name = 'api_get_by_id'),
    path('student/group/new', api_view.StudentGroupAPICreateList.as_view() , name = 'api_new_student_group'),
    path('student/group/<str:pk>', api_view.StudentGroupAPIRetrieveUpdateDestroy.as_view() , name = 'api_student_group'),
    path('student/update/<str:pk>/', api_view.StudentAPIUpdate.as_view() , name = 'api_update_student'),
    path('student/delete/<str:pk>/', api_view.StudentAPIDestroy.as_view() , name = 'api_delete_student'),
]
