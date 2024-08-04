from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from . import api_view

app_name='accounts'

urlpatterns = [    
    path('register/', api_view.register.as_view() , name = 'api_register'),
    path('login/', api_view.LoginView.as_view() , name = 'api_login'), # obtain_auth_token
    path('logout/', api_view.LogoutView.as_view() , name = 'api_logout'),
    path('userinfo/', api_view.current_user , name = 'api_user_info'),  
    path('userinfo/update/', api_view.update_user , name = 'api_update_user'),  
    path('forgot_password/', api_view.forgot_password , name = 'api_forgot_password'),  
    path('reset_password/<str:token>', api_view.reset_password , name = 'api_reset_password'),  
    
    path('sign_up', views.signup , name = 'sign_up'),  
    path('dashboard', views.dashboard , name = 'dashboard'), 
    path('profile_edit', views.profile_edit , name = 'profile_edit'), 

]