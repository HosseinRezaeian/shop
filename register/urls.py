from django.urls import path
from . import views


urlpatterns = [
    path('sign',views.registerV.as_view(), name="signup"),
    path('login', views.loginV.as_view(), name='login'),
    path('email-active-code/<str:code>', views.activate.as_view(), name='active-account'),
]