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

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('votings.urls')),
    url(r'^cart', include('cart.urls')),
    url(r'^orders/', include('orders.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# tell django to read urls.py in example app

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_PATH)
    #urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#from django.contrib import admin
#from django.urls import include, path

#from django.conf import settings
#from django.conf.urls.static import static
#from django.views.generic import TemplateView

#urlpatterns = [
	#path('votings/', include('votings.urls')),
    #path('admin/', admin.site.urls),
#]
