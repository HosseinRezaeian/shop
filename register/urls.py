from django.urls import path
from . import views

urlpatterns = [
    path('sign-up', views.registerV.as_view(), name="signup"),
    path('login', views.loginV.as_view(), name='login'),
    path('logout', views.LogoutV.as_view(), name='logout'),
    path('email-active-code/<str:code>', views.activate.as_view(), name='active-account'),
    path('reset/<str:code>', views.resetV.as_view(), name='reset'),
    path('forget-password', views.forgetV.as_view(), name='forget'),
]
