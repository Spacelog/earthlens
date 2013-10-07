from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout
from django.contrib import admin
from core.views import IndexView, IndexAjaxView, ImageView, RateView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^ajax/more/$', IndexAjaxView.as_view(), name='index-ajax'),
    url(r'^image/(?P<pk>\d+)/$', ImageView.as_view(), name='image'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^rate/$', login_required(RateView.as_view()), name='rate'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, {"next_page": "/" }, name='logout'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
