from django.urls import path

from . import views

urlpatterns = [
    path('predict/', views.predict, name='predict'),
    path('predict/calender.html', views.calender, name='calender'),
    path('predict/eventD.html', views.eventD, name='eventD'),
    path('predict/dynamic.html', views.dynamic, name='dynamic'),
    path('predict/list1', views.list1, name='list1')
]

