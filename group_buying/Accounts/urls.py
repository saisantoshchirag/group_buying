from django.urls import path
from Accounts.views import auth_view, register, login, logout
from django.contrib.auth import views as auth_views
from django.conf.urls import url

app_name = 'Accounts'
urlpatterns = [
    path('auth', auth_view, name='auth_view_reg'),
    path('register', register, name="loginmodule_register"),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
]
