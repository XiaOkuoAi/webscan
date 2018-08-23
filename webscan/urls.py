"""webscan URL Configuration

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
from django.contrib import admin
from django.urls import path
from cms import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('whatcms', views.Whatcms.as_view()),
    path('portscan', views.Portscan.as_view()),
    path('domain', views.Otherdomain.as_view()),
    path('fuckcms', views.Fuckcms.as_view()),
    path('api/cms', views.api_cms),
    path('awvs', views.Awvs.as_view()),
    path('api/awvs/delscan', views.del_scan),
    path('api/awvs/stopscan', views.stop_scan),
    path('api/awvs/addscan', views.add_scan),
    path('api/awvs/Presentation', views.Presentation),
    path('api/awvs/getvulns', views.get_vluns),
    path('fofa', views.fofa),
]
