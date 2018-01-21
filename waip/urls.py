from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.auth import views as auth_views
from users import views as users_views
from games import views as games_views
from games.views import NoteDetailAjaxView

urlpatterns = [
    # Admin
    url(r'^admin/', admin.site.urls),

    # Home
    url(r'^$', games_views.list_user_games, name='home'),

    # User
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='log_out'),
    url(r'^register/$', users_views.register, name='register'),
    url(r'^me/$', users_views.modify_logged_user, name='modify_logged_user'),

    # Games
    url(r'^games$', games_views.list_user_games, name='list_games'),
    url(r'^games/add/$', games_views.add_game, name='add_game'),
    url(r'^games/([0-9]+)$', games_views.modify_game, name='modify_game'),
    url(r'^games/([0-9]+)/delete/$', games_views.delete_game, name='delete_game'),

    # Ajax Urls
    url(r'^ajax/games/scrap-metacritic$', games_views.scrap_metacritic_ajax),
    url(r'^ajax/games/scrap-hltb$', games_views.scrap_hltb_ajax),
    url(r'^ajax/games/([0-9]+)/finish$', games_views.finish_game_ajax),
    url(r'^ajax/games/([0-9]+)/add-note$', games_views.add_note_to_game_ajax),
    url(r'^ajax/games/([0-9]+)/notes/([0-9]+)$', NoteDetailAjaxView.as_view(), name='note-detail'),

    # DELETE TODO
    url(r'^debug$', games_views.debug),
]

# Added for Debug Bar
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
