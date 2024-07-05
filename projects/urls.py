from django.urls import path
from . import views
from . import api_view


urlpatterns = [
    #path('/', views. , name = 'home'),
    path('projects/', api_view.ProjectsAPIList.as_view() , name = 'api_projects'),
    path('project/<str:pk>/', api_view.ProjectsAPIDetail.as_view() , name = 'api_get_by_id'),
    path('project/new/', api_view.ProjectsAPIList.as_view() , name = 'api_new_project'),
    path('project/update/<str:pk>/', api_view.ProjectsAPIDetail.as_view() , name = 'api_update_project'),
    path('project/delete/<str:pk>/', api_view.ProjectsAPIDetail.as_view() , name = 'api_delete_project'),

    path('<str:pk>/reviews/', api_view.add_review , name = 'api_add_review'),
    path('<str:pk>/reviews/delete/', api_view.delete_review , name = 'api_delete_review'),

]
