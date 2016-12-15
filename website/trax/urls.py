from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from . import views



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^t/', include('tracks.urls')),
    url(r'^r/', include('randomizer.urls')),
    url(r'^e/', include('events.urls')),
    url(r'^$', views.Homepage.as_view(), name="homepage"),
    url(r'^accounts/login/$', views.login_view, name="login"),
    url(r'^accounts/logout/$', views.logout_view, name="logout"),
    url(r'^accounts/register/$', views.Registration.as_view(), name="register"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
