from django.urls import path

import api.views as views

urlpatterns = [
    path('/json', views.index),
    path('/xml', views.xml),
    path('/logs', views.logs),
    path('', views.index),
]