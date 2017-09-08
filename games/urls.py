from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # url(r'^hello/', views.helloWorld, name='hello'),
    url(r'^games/([0-9]+)$', views.getGameAjax, name='getGameAjax'),
    url(r'^$', views.main, name='main'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
