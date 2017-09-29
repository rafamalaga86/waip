from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.auth import views as auth_views
from users import views as users_views
from games import views as games_views

urlpatterns = [
    # Admin
    url(r'^admin/', admin.site.urls),

    # Home
    url(r'^$', games_views.list_user_games, name='home'),

    # User
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='log_in'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='log_out'),
    url(r'^register/$', users_views.register, name='register'),

    # Games
    url(r'^games/add$', games_views.add_game, name='add_game'),

    # TODO take this one out
    url(r'^ajax/games/scrap-ddg-mc$', games_views.scrap_ddg_mc_ajax),

    # Ajax Urls
    url(r'^ajax/games/scrap-metacritic$', games_views.scrap_metacritic_ajax),
    url(r'^ajax/games/scrap-hltb$', games_views.scrap_hltb_ajax),
    url(r'^ajax/games/([0-9]+)$', games_views.getGameAjax),
    url(r'^ajax/games/([0-9]+)/finish$', games_views.finishGameAjax),
]

if settings.DEBUG:  # Added for Debug Bar
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
