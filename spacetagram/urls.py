from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from core.views import IndexView, ImageView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^image/(?P<pk>\d+)/$', ImageView.as_view(), name='image'),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
