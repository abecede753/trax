from django.conf.urls import url, include
from django.contrib import admin
from tracks import views

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', views.track_detail, name='track_detail'),
    url(r'^(?P<lap_pk>\d+)/add_laptime/$', views.laptime_add, name='laptime_add'),
    url(r'^add/$', views.TrackCreate.as_view(), name='track_add'),
    url(r'^(?P<pk>\d+)/edit/$', views.TrackEdit.as_view(), name='track_edit'),
]
