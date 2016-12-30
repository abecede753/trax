from django.conf.urls import url
from randomizer import views
from .views import StaggeredStartCreator, StaggeredStartRaceDetail, \
    participants_list, enlist, StaggeredStartRaceStatus

from .views import SSECreator

urlpatterns = [
    url(r'^s/$', StaggeredStartCreator.as_view(), name='sscreator'),
    url(r'^s/(?P<pk>\d+)/$', StaggeredStartRaceDetail.as_view(),
        name='staggeredstartrace_detail'),
    url(r'^s/(?P<pk>\d+)/participantstable.json$',
        participants_list,
        name='participantslist'),
    url(r'^s/(?P<pk>\d+)/enlist$',
        enlist,
        name='staggeredstartrace_enlist'),
    url(r'^s/(?P<pk>\d+)/get_status/$',
        StaggeredStartRaceStatus.as_view(),
        name='get_status'),

    ####################### NEW STUFF

    url(r'^ss/$',
        SSECreator.as_view(),
        name='sse_create'),
]
