from django.conf.urls import url
from .ssr_views import StaggeredStartRaceCreator, StaggeredStartRaceDetail, \
    participants_list, enlist, StaggeredStartRaceStatus, check_for_newer_ssr
from .pitassistant_views import PitAssistantCreator, PitAssistantDetail

urlpatterns = [
    url(r'^s/add/$', StaggeredStartRaceCreator.as_view(),
        name='ssr_add'),
    url(r'^s/(?P<pk>\d+)/$', StaggeredStartRaceDetail.as_view(),
        name='staggeredstartrace_detail'),
    url(r'^s/(?P<pk>\d+)/participantstable.json$',
        participants_list,
        name='participantslist'),
    url(r'^s/(?P<pk>\d+)/enlist/(?P<vehicle_pk>\d+)/$',
        enlist,
        name='staggeredstartrace_enlist'),
    url(r'^s/(?P<pk>\d+)/get_status/$',
        StaggeredStartRaceStatus.as_view(),
        name='get_status'),
    url(r'^s/(?P<pk>\d+)/check_for_newer/$',
        check_for_newer_ssr,
        name='check_for_newer_ssr'),
    url(r'^p/add/$', PitAssistantCreator.as_view(),
        name='pita_add'),
    url(r'^p/(?P<pk>\d+)/$', PitAssistantDetail.as_view(),
        name='pita_detail'),
]
