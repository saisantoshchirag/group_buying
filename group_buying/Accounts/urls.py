from django.urls import path
from Accounts.views import auth_view, signup, signin, logout,activate,reset_password,reset_display,verify_reset_password,save_password
from django.contrib.auth import views as auth_views
from django.conf.urls import url

app_name = 'Accounts'
urlpatterns = [
    path('auth', auth_view, name='auth_view_reg'),
    path('register', signup, name="loginmodule_register"),
    path('login/',signin, name='login'),
    path('logout/', logout, name='logout'),
    # url(r'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',activate, name='activate'),
    path('activate/<uidb64>/<token>',activate,name='activate'),
    # path( 'register/', register, name='register'),
    path('password_reset/',reset_password ,name='reset_password'),
    # path('password_reset/done',,name='password_reset_done'),
    path('reset_display/',reset_display,name='reset_display'),
    path('verify_password/<uidb64>/<token>',verify_reset_password,name='verify_reset_password'),
    path('save_password/',save_password,name='save_password')


]
