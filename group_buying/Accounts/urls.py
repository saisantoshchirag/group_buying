from django.urls import path,include
from Accounts.views import auth_view, signup, signin, logout,activate,reset_password,reset_display,verify_reset_password,save_password
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.views.generic import TemplateView
# app_name = 'Accounts'
urlpatterns = [
    path('auth', auth_view, name='auth_view_reg'),
    path('register', signup, name="loginmodule_register"),
    path('login/',signin, name='login'),
    path('logout/', logout, name='logout'),
    path('activate/<uidb64>/<token>',activate,name='activate'),
    path('password_reset/',reset_password ,name='reset_password'),
    path('reset_display/',reset_display,name='reset_display'),
    path('verify_password/<uidb64>/<token>',verify_reset_password,name='verify_reset_password'),
    path('save_password/',save_password,name='save_password'),
    path('', include('social_django.urls', namespace='social')),

]
