from django.conf.urls import url
from randomizer import views
from .views import StaggeredStartCreator, StaggeredStartRaceDetail, \
    participants_list, StaggeredStartRaceInvite

urlpatterns = [
    url(r'^s/$', StaggeredStartCreator.as_view(), name='sscreator'),
    url(r'^s/(?P<pk>\d+)/$', StaggeredStartRaceDetail.as_view(),
        name='staggeredstartrace_detail'),
    url(r'^s/(?P<pk>\d+)/inv/$', StaggeredStartRaceInvite.as_view(),
        name='staggeredstartrace_invite'),
    url(r'^s/(?P<pk>\d+)/participantstable.json$',
        participants_list,
        name='participantslist'),
]
