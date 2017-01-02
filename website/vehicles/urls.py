from django.conf.urls import url
from .views import (VehicleList, VehicleDetail,
                    VehicleCreate, VehicleUpdate)


urlpatterns = [
    url(r'^$', VehicleList.as_view(),
        name='vehicle_list'),
    url(r'^s/(?P<pk>\d+)/$', VehicleDetail.as_view(),
        name='vehicle_detail'),
    url(r'^add/$', VehicleCreate.as_view(),
        name='vehicle_create'),
    url(r'^s/(?P<pk>\d+)/edit/$', VehicleUpdate.as_view(),
        name='vehicle_update'),
]
