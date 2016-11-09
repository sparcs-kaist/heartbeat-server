"""heartbeat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from apps.core import views as core_view

urlpatterns = [
    url(r'^$', core_view.main),
    url(r'^login/$', core_view.login),
    url(r'^login/callback/$', core_view.login_callback),
    url(r'^logout/$', core_view.logout),
    url(r'^unregister/$', core_view.unregister),
    url(r'^api/update/$', core_view.update),

    url(r'^admin/', admin.site.urls),
]
