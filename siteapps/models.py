from django.db import models
from django.contrib.auth.models import User
# Create your models here.


def file_upload_helper(instance, filename):
    return '{0}/{1}'.format(instance.organization.name, filename)


class InmergenceUser(models.Model):
    user = models.ForeignKey(User)
    dob = models.CharField(max_length=100)
    sex = models.CharField(max_length=100)
    prof = models.CharField(max_length=100)


class Organization(models.Model):
    user = models.ForeignKey(InmergenceUser)
    name = models.CharField(max_length=250)
    id = models.CharField(max_length=250, primary_key=True)


class Document(models.Model):
    organization = models.ForeignKey(Organization)
    id = models.CharField(max_length=250, primary_key=True)
    name = models.CharField(max_length=250)
    file = models.FileField(upload_to=file_upload_helper)
