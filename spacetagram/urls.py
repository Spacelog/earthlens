import os
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout
from django.contrib import admin
from core.views import IndexView, ImageView, RateView, MissionView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^mission/(?P<mission>[^/]+)/$', MissionView.as_view(), name='mission'),
    url(r'^image/(?P<pk>\d+)/$', ImageView.as_view(), name='image'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^rate/$', login_required(RateView.as_view()), name='rate'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, {"next_page": "/" }, name='logout'),
) + \
  static("/static/admin/", document_root=os.path.join(os.path.dirname(admin.__file__), "static/admin/")) + \
  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
