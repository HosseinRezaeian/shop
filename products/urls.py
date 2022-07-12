from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index,name='index'),
    path('<slug:ps>', views.prodact, name="pro"),
    # path('<slug:ps1>/<slug:catp>', views.cp, name="cp"),
    path('<slug:catp1>/<slug:pr>', views.mp, name="mp"),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

