from django.db import models
from django.contrib.auth.models import User
# Create your models here.


def file_upload_helper(instance, filename):
    return '{0}/{1}'.format(instance.organization.name, filename).replace(" ", "_")


class InmergenceUser(models.Model):
    user = models.OneToOneField(User)
    dob = models.CharField(max_length=100)
    sex = models.CharField(max_length=100)
    prof = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Organization(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=250)
    id = models.CharField(max_length=250, primary_key=True)

    def __str__(self):
        return self.name


class Document(models.Model):
    organization = models.ForeignKey(Organization)
    user = models.ForeignKey(InmergenceUser)
    id = models.CharField(max_length=250, primary_key=True)
    name = models.CharField(max_length=250)
    html_name = models.CharField(max_length=1000)
    file = models.FileField(upload_to=file_upload_helper)

    def __str__(self):
        return self.name
