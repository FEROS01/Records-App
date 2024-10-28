from uuid import uuid4

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Member(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    position = models.CharField()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name


class Industry(models.Model):
    name = models.CharField(_('industry_name'),unique=True)
    managers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,related_name='%(class)s_industry')
    members = models.ManyToManyField(Member,related_name='%(class)s_industry',blank=True)
    owner = models.CharField(max_length=200)
    uuid = models.UUIDField(primary_key=True,editable=False,default=uuid4)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

class Church(Industry):
    head_pastor = models.CharField(_("pastor's_name"),max_length=300)


class Service(models.Model):
    uuid = models.UUIDField(default=uuid4,primary_key=True,editable=False)
    church = models.ForeignKey(
        Church,on_delete=models.CASCADE,related_name='service')
    name = models.CharField()
    description = models.TextField()

    def __str__(self):
        return self.name

class ChurchRecord(models.Model):
    uuid = models.UUIDField(default=uuid4,primary_key=True,editable=False)
    church = models.ForeignKey(
        Church,on_delete=models.CASCADE,related_name='church_record')
    service = models.ForeignKey(
        Service,on_delete=models.CASCADE,related_name='service_record',default=None)
    sermon_title = models.TextField()
    text = models.CharField(max_length=200)
    service_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.church}_{self.service.name}_{self.service_date.date()}"


class Offering(models.Model):
    uuid = models.UUIDField(default=uuid4,primary_key=True,editable=False)
    record = models.ForeignKey(
        ChurchRecord, on_delete=models.CASCADE, related_name='offering',default=None)
    currency = models.CharField(max_length=100)
    denomination = models.DecimalField(decimal_places=2,max_digits=6)
    frequency = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f'{self.denomination}x{self.frequency}'