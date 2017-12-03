from django.conf.urls import url
from .views import PlayerDetail, PlayerList, change_password

urlpatterns = [
    url(r'^$', PlayerList.as_view(),
        name='player_list'),
    url(r'^(?P<pk>\d+)/$', PlayerDetail.as_view(),
        name='player_detail'),
    url(r'^pw/(?P<hash>.+)/$', change_password,
        name='password_changer'),
]
