
#######################
#we made this one


from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^markup/', display_markup) ,
    url(r'^readings/', display_readings),
    url(r'^registration/', display_registration)
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)