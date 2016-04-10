
#######################
#we made this one


from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^markup/', display_markup) 
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)