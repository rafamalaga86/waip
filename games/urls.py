from . import views
from django.conf.urls import url

urlpatterns = [
    # url(r'^hello/', views.helloWorld, name='hello'),
    url(r'^games/([0-9]+)$', views.getGameAjax, name='getGameAjax'),
    url(r'', views.main, name='main'),
]
