from django.urls import path

import api.views as views

urlpatterns = [
    path('', views.index),
    path('json', views.index),
    path('xml', views.xml),
    path('logs', views.logs),
]