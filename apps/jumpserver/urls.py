# ~*~ coding: utf-8 ~*~
from __future__ import unicode_literals

"""jumpserver URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static

from .views import IndexView


urlpatterns = [
    url(r'^captcha/', include('captcha.urls')),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^users/', include('users.urls.views_urls', namespace='users')),
    url(r'^assets/', include('assets.urls.views_urls', namespace='assets')),
    url(r'^perms/', include('perms.urls.views_urls', namespace='perms')),
    url(r'^audits/', include('audits.urls.views_urls', namespace='audits')),
    url(r'^applications/', include('applications.urls.views_urls', namespace='applications')),
    url(r'^ops/', include('ops.urls.view_urls', namespace='ops')),

    # Api url view map
    url(r'^api/users/', include('users.urls.api_urls', namespace='api-users')),
    url(r'^api/assets/', include('assets.urls.api_urls', namespace='api-assets')),
    url(r'^api/perms/', include('perms.urls.api_urls', namespace='api-perms')),
    url(r'^api/audits/', include('audits.urls.api_urls', namespace='api-audits')),
    url(r'^api/applications/', include('applications.urls.api_urls', namespace='api-applications')),
    url(r'^api/ops/', include('ops.urls.api_urls', namespace='api-ops')),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

