from django.conf.urls import url
from . import views

app_name = 'votings'

urlpatterns = [

    # r is for raw string, ^ match beginning and $ match the ending
    url(r'^$', views.IndexPageView.as_view(template_name="polls/index.html"), name='index'), # Notice the URL has been named
    url(r'^cat', views.CatPageView.as_view(template_name="polls/cat.html"), name='cat'),
    url(r'^uploadRoom/', views.uploadRoom, name='uploadRoom'),
    url(r'^login/$',views.login,name='login'),
    url(r'^base', views.product_list, name='product_list'),
    url(r'^logout/$',views.logout,name='logout'),
    #keep at the end so that it doesn't interfere with the rest of the urls
    url(r'^(?P<category_slug>[-\w]+)/$', views.product_list, name='product_list_by_category'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail'),
    
    
   # url(r'^$', views.IndexPageView.as_view(), name='index'), # Notice the URL has been named
]



'''from django.urls import path

from . import views


urlpatterns = [
    path('xs', views.index, name='index'),
    path('b', views.basefunc, name='basefunction'),
    ]'''