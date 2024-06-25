from django.urls import path
from . import views
from . import api_view

app_name='accounts'

urlpatterns = [    
    path('register/', api_view.register , name = 'api_register'),
    path('userinfo/', api_view.current_user , name = 'api_user_info'),  
    path('userinfo/update/', api_view.update_user , name = 'api_update_user'),  
    path('forgot_password/', api_view.forgot_password , name = 'api_forgot_password'),  
    path('reset_password/<str:token>', api_view.reset_password , name = 'api_reset_password'),  
    
    path('sign_up', views.signup , name = 'sign_up'),  
    path('profile', views.profile , name = 'profile'), 
    path('profile_edit', views.profile_edit , name = 'profile_edit'), 

]