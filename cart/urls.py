from django.conf import settings  # new
from django.urls import path  # new
from django.conf.urls.static import static  # new
from . import views

urlpatterns = [
    path('cart/c', views.usercart, name='cart'),
path('cart/cart_shop', views.cart_shoping.as_view(), name='cart_shoping'),


]
