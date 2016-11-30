from django.conf.urls import url
from randomizer import views

urlpatterns = [
    url(r'^racelist/$', views.Racelist.as_view(), name='randomracelist'),
]
