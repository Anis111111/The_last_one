from django.urls import path
from . import views
from . import api_view

urlpatterns = [
    path('professors/', api_view.ProfessorsAPIList.as_view(), name='api_professors'),
    path('professor/<str:pk>', api_view.ProfessorsAPIDetail.as_view(), name='api_get_by_id'),
    path('professor/new', api_view.ProfessorsAPIList.as_view(), name='api_new_professor'),
    path('professor/update/<str:pk>', api_view.ProfessorsAPIDetail.as_view(), name='api_update_professor'),
    path('professor/delete/<str:pk>', api_view.ProfessorsAPIDetail.as_view(), name='api_delete_professor'),
]