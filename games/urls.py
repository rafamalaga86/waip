from . import views
from django.conf.urls import url
# from django.conf import settings
# from django.conf.urls.static import static

urlpatterns = [
    # Urls
    url(r'^$', views.home, name='home'),
    url(r'^games/new$', views.newGame, name='newGame'),

    # TODO take this one out
    url(r'^ajax/games/scrap-ddg-mc$', views.scrap_ddg_mc_ajax),

    # Ajax Urls
    url(r'^ajax/games/scrap-metacritic$', views.scrap_metacritic_ajax),
    url(r'^ajax/games/scrap-hltb$', views.scrap_hltb_ajax),
    url(r'^ajax/games/([0-9]+)$', views.getGameAjax),
    url(r'^ajax/games/([0-9]+)/finish$', views.finishGameAjax),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
