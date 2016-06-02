# vim:set sw=4 ts=4 et:
from django.conf.urls import url
from django.contrib import admin
import vaper.views

urlpatterns = [
    url(r'^$',     vaper.views.index, name='index'),
    url(r'^admin/', admin.site.urls),
]
