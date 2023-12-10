from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
        path('signup/', views.sign_up, name='sign_up'),
        path('login/',  auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
        path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
        path('profile/', views.profile, name='profile'),
        path('create_clinic/', views.create_clinic, name='create_clinic'),
        path('create_doctor/', views.create_doctor, name='create_doctor'),
             ]
