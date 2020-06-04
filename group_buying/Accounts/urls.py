from django.urls import path
from Accounts.views import auth_view, signup, signin, logout,activate
from django.contrib.auth import views as auth_views
from django.conf.urls import url

app_name = 'Accounts'
urlpatterns = [
    path('auth', auth_view, name='auth_view_reg'),
    path('register', signup, name="loginmodule_register"),
    path('login/',signin, name='login'),
    path('logout/', logout, name='logout'),
    # url(r'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',activate, name='activate'),
    path('activate/<uidb64>/<token>',activate,name='activate')
    # path( 'register/', register, name='register'),
]
