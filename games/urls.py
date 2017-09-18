from . import views
from django.conf.urls import url
# from django.conf import settings
# from django.conf.urls.static import static

urlpatterns = [
    # Urls
    url(r'^$', views.main, name='main'),
    url(r'^games/new', views.newGame, name='newGame'),

    # Ajax Urls
    url(r'^ajax/games/scrap$', views.gameScrapAjax, name='gameScrapAjax'),
    url(r'^ajax/games/([0-9]+)$', views.getGameAjax, name='getGameAjax'),
    url(r'^ajax/games/([0-9]+)/finish$', views.finishGameAjax, name='getGameAjax'),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
