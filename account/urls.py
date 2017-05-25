from django.conf.urls import patterns, include, url
from django.contrib import admin

# from views import main
# from views import transmitRest

from . import views

urlpatterns = patterns('',
    url(r'^$', views.main),
    url(r'^transmit/', views.transmitRest),
)
