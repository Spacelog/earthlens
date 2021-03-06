import os
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout
from django.contrib import admin
from django.views.generic import TemplateView
from core.views import IndexView, ImageView, RateView, MissionView, TagView, TaggerView, LeaderboardView, MissionTimelineView, UserAwesomeView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^mission/(?P<mission>[^/]+)/$', MissionView.as_view(), name='mission'),
    url(r'^mission/(?P<mission>[^/]+)/timeline/$', MissionTimelineView.as_view(), name='mission-timeline'),
    url(r'^tag/(?P<slug>[^/]+)/$', TagView.as_view(), name='tag'),
    url(r'^image/(?P<code>[^/]+)/$', ImageView.as_view(), name='image'),
    url(r'^user/(?P<username>[^/]+)/awesome/$', UserAwesomeView.as_view(), name='user-awesome'),

    url(r'^leaderboard/$', login_required(LeaderboardView.as_view()), name='rate'),
    url(r'^rate/$', login_required(RateView.as_view()), name='rate'),
    url(r'^tagger/$', login_required(TaggerView.as_view()), name='tagger'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, {"next_page": "/" }, name='logout'),
    url(r'^about/$', TemplateView.as_view(template_name="about.html"), name='about'),

    url(r'^admin/', include(admin.site.urls)),
) + \
  static("/static/admin/", document_root=os.path.join(os.path.dirname(admin.__file__), "static/admin/")) + \
  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
