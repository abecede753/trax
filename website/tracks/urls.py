from django.conf.urls import url, include
from django.contrib import admin
from tracks import views

urlpatterns = [
    url(r'^$', views.TrackList.as_view(), name='track_list'),
    url(r'^(?P<pk>\d+)/$', views.track_detail, name='track_detail'),
    url(r'^(?P<track_pk>\d+)/laptimes.json$', views.laptime_json, name='laptime_json'),
    url(r'^tracks.json$', views.tracks_json, name='tracks_json'),
    url(r'^(?P<lap_pk>\d+)/add_laptime/$', views.laptime_add, name='laptime_add'),
    url(r'^l/(?P<lap_pk>\d+)/delete/$', views.laptime_delete, name='laptime_delete'),
    url(r'^add/$', views.TrackCreate.as_view(), name='track_add'),
    url(r'^(?P<pk>\d+)/edit/$', views.TrackEdit.as_view(), name='track_edit'),
]
