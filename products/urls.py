from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'product'
urlpatterns = [
    path('', views.home, name='home'),
    path('prodacts', views.index, name='index'),
    path('prodact/<slug:ps>', views.prodact_list_view.as_view(), name="pro"),
    # path('<slug:ps1>/<slug:catp>', views.cp, name="cp"),
    path('<slug:catp1>/<slug:pr>', views.mp, name="mp"),
    # path('all/allp/prodact', views.prodact_list_view.as_view(), name="mp"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
