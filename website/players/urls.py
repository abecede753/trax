from django.conf.urls import url
from .views import PlayerDetail, PlayerList

urlpatterns = [
    url(r'^$', PlayerList.as_view(),
        name='player_list'),
    url(r'^(?P<pk>\d+)/$', PlayerDetail.as_view(),
        name='player_detail'),
]
