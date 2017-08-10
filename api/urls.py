from djang.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
]
