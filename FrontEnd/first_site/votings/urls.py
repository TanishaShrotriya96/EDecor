from django.conf.urls import url
from votings import views

urlpatterns = [
    url(r'^$', views.IndexPageView.as_view(), name='index'), # Notice the URL has been named
    url(r'^cat', views.CatPageView.as_view(template_name="polls/cat.html"), name='cat'),

]



'''from django.urls import path

from . import views


urlpatterns = [
    path('xs', views.index, name='index'),
    path('b', views.basefunc, name='basefunction'),
    ]'''