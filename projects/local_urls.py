from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from django.contrib.auth import views as authViews
from . import views



urlpatterns = [
    path('', views.home , name='home'),
    path('project/', views.project,name='project'),
    # path('about/', views.about,name='about'),
    
    # path('create/', views.create,name='create'),
    # path('create/<str:pk>', views.create , name='create'),
    # {% url "update" item.id  %}
    # path('update/<str:pk>', views.update , name='update'),
    # # {% url "delete" item.id  %}
    # path('delete/<str:pk>', views.delete , name='delete'),

    # # path('register/',views.register,name="register"), 
    # path('login/', views.userLogin , name='login'),
    # path('logout/', views.userLogout , name='logout'),

    # path('user/', views.userProfile , name='user_profile'),

    # path('reset_password/', authViews.PasswordResetView.as_view() , name='reset_password'),
    # path('reset_password_sent/', authViews.PasswordResetDoneView.as_view() , name='reset_password_done'),
    # path('reset/<uidb64><token>', authViews.PasswordResetConfirmView.as_view() , name='reset_password_confirm'),
    # path('reset_password_complete/', authViews.PasswordResetCompleteView.as_view() , name='reset_password_complete'),
]
static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)