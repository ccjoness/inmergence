from django.contrib import admin
from .models import InmergenceUser, Organization, Document
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
# Register your models here.
# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton


class InmergenceUserInline(admin.StackedInline):
    model = InmergenceUser
    can_delete = False
    # verbose_name_plural = 'employee'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (InmergenceUserInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


admin.site.register(InmergenceUser)
admin.site.register(Organization)
admin.site.register(Document)
