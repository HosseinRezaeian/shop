from django.conf import settings  # new
from django.urls import path  # new
from django.conf.urls.static import static  # new
from . import views

urlpatterns = [
    path('cart/c', views.usercart, name='cart'),
    path('cart/cart_shop', views.cart_shoping.as_view(), name='cart_shoping'),
    path('cart/remove-obj', views.shoper_par, name='remove_cart'),
    path('cart/save_count', views.save_count, name='save_count'),
    path('cart/request-pay', views.go_to_gateway_view, name='gateway'),
    path('cart/callback', views.callback_gateway_view, name='callback'),
   

]
