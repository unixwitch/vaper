# vim:set sw=4 ts=4 et:
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout
import vaper.views

app_name = 'vaper'

vaper_urlpatterns = ([
    url(r'^$',                          vaper.views.index, name='index'),
    url(r'^recipe/(?P<id>[0-9]+)/$',    vaper.views.recipe, name='recipe'),
    url(r'^flavour/(?P<id>[0-9]+)/$',   vaper.views.flavour, name='flavour'),
    url(r'^login/$',    login, name='login', kwargs = {
        'template_name': 'vaper/login.html',
    }),
    url(r'^logout/$',   logout, name='logout', kwargs = {
        'next_page': '/',
    }),
], 'vaper')

urlpatterns = [
    url(r'^admin/',     admin.site.urls),
    url(r'', include(vaper_urlpatterns)),
]
