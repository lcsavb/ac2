from . import views
from django.urls import path
from django.contrib.auth import views as users_views

app_name = 'users'

urlpatterns = [
        path('signup/', views.sign_up, name='sign_up'),
        path('login/',  users_views.LoginView.as_view(template_name='users/login.html'), name='login'),
        path('logout/', users_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
             ]
