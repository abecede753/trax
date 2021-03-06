from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
# from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from . import views
from tracks import views as tracks_views


urlpatterns = [
#    url(r'^admin/', admin.site.urls),
    url(r'^t/', include('tracks.urls')),
    url(r'^v/', include('vehicles.urls')),
    url(r'^r/', include('randomizer.urls')),
    url(r'^e/', include('events.urls')),
    url(r'^p/', include('players.urls')),
    # url(r'^$', cache_page(60*10)(views.Homepage.as_view()), name="homepage"),
    url(r'^$', views.Homepage.as_view(), name="homepage"),
    url(r'^accounts/login/$', views.login_view, name="login"),
    url(r'^accounts/logout/$', views.logout_view, name="logout"),
    url(r'^accounts/register/$', views.Registration.as_view(), name="register"),
    url(r'^imprint/$', TemplateView.as_view(template_name='trax/imprint.html'),
        name="imprint"),
    url(r'^robots.txt$', TemplateView.as_view(template_name='trax/imprint.html'),
                      name="DEVELOPMENTrobots.txt"),
    url(r'^miniutil/now$', views.timestamp_dev, name="DEVELOPMENTnow"),
    url(r'^epsilon/$', tracks_views.epsilon_detail, name="epsilon_detail"),
#    url(r'^grotti17/$', tracks_views.grotti17_detail, name="grotti17_detail"),
    url(r'^unaffordable/$', tracks_views.unaffordable_detail,
        name="unaffordable_detail"),
    url(r'^tinymce/', include('tinymce.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
