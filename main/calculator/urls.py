from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    re_path(r'^home/$', views.IndexView.as_view(), name='home'),
    re_path(r'^simple/$', views.SimpleView.as_view(), name='simple'),
    # path('home', views.index, name='home'),
    # path('simple', views.simple, name='simple'),
    #re_path(r'^calculate/$', views.calculate, name='calculate'),
    path('calculate', views.calculate, name='calculate'),
]