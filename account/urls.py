from django.conf.urls import patterns, include, url
from django.contrib import admin

from views import main
from views import transmitRest

urlpatterns = patterns('',
    url(r'^$', main),
    url(r'^transmit/', transmitRest),
)
