
from django.urls import path
from . import views

urlpatterns = [
   path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
  
    path('upload-resume/', views.upload_resume, name='upload_resume'),

    path('role-match/', views.role_match, name='role_match'),
    path('role/<str:role_name>/', views.role_detail, name='role_detail'),
    path('analyze/<str:role_name>/', views.analyze_resume, name='analyze_resume'),

]
