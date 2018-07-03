from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login, name='do_the_login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^register$', views.register),
    url(r'^home$', views.home, name='home'),
    url(r'^home/(?P<user_id>\d+)$', views.show),
    url(r'^home/(?P<friend_id>\d+)/create$', views.add_friend, name='add_friend'),
    url(r'^home/(?P<friend_id>\d+)/destroy$', views.lose_friend, name='lose_friend')
]