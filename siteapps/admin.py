from django.contrib import admin
from .models import InmergenceUser, Organization, Document
# Register your models here.

admin.site.register(InmergenceUser)
admin.site.register(Organization)
admin.site.register(Document)
