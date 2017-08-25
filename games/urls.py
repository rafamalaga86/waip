from . import views
from django.conf.urls import url

urlpatterns = [
    # url(r'^hello/', views.helloWorld, name='hello'), # OLD before implementing class based views
    url(r'^hello/', views.helloWorld, name='hello'),
    url('', views.main, name='main'),
]
