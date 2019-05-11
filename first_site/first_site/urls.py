"""first_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include # Add include to the imports here
from django.contrib import admin
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from main.views import IndexPageView, ChangeLanguageView

urlpatterns = [
   
    #index page from votings app
    path('login', IndexPageView.as_view(), name='index'),
    #language related code
    path('i18n/', include('django.conf.urls.i18n')),
    path('language/', ChangeLanguageView.as_view(), name='change_language'),

    # accounts app related urls
    path('accounts/', include('accounts.urls')),

    #django admin page
    url(r'^admin/', admin.site.urls),
    #urls from cart and orders apps
    url(r'^cart/', include('cart.urls')),
    url(r'^orders/', include('orders.urls')),
    #urls from votings app
    url(r'^', include('votings.urls')),
    #keep votings urls are the end because of the regex urls


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# tell django to read urls.py in example app

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_PATH)
    #urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
