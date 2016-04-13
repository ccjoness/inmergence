"""inmergence_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from siteapps import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import login
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^org/(?P<org>\w+)/$', views.org, name='org'),
    url(r'^org/(?P<org>\w+)/(?P<docu>\w+-\w+-\w+-\w+-\w+)/$', views.doc, name='doc'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^login/$', login, name='login'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^upload_document/$', views.upload_document, name='upload_document'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)