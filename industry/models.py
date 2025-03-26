from uuid import uuid4

from django.utils import timezone
from django.utils.functional import cached_property
from django.db import models
from django.db.models.functions import Cast
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Member(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    position = models.CharField(default='Member', blank=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name


class Industry(models.Model):
    name = models.CharField(unique=True)
    managers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,related_name='%(class)s_industry')
    members = models.ManyToManyField(
        Member,related_name='%(class)s_industry',blank=True)
    owner = models.CharField(_('Founder'),max_length=200)
    uuid = models.UUIDField(primary_key=True,editable=False,default=uuid4)
    website = models.URLField(
        blank=True, 
        help_text='Prefix url scheme to website e.g https://www.example.com'
        )
    date_established = models.DateField(
        _('Established'),
        default=timezone.now,
        help_text= "Format: yyyy-mm-dd"
        )
    about = models.TextField(default='', blank=True)

    def __str__(self):
        return self.name
    
    @property
    def number_of_members(self):
        return self.members.count()
    
    def is_manager(self,user):
        is_manager = self.managers.filter(uuid=user.uuid).exists()
        return is_manager

    class Meta:
        abstract = True

class Church(Industry):
    head_pastor = models.CharField(_("pastor"),max_length=300)

class Service(models.Model):
    class DayChoices(models.TextChoices):
        MON = 'Monday'
        TUE = 'Tuesday'
        WED = 'Wednesday'
        THU = 'Thursday'
        FRI = 'Friday'
        SAT = 'Saturday'
        SUN = 'Sunday'

    uuid = models.UUIDField(default=uuid4,primary_key=True,editable=False)
    church = models.ForeignKey(
        Church,on_delete=models.CASCADE,related_name='service')
    name = models.CharField()
    description = models.TextField()
    start_time = models.TimeField(default='00:00')
    end_time = models.TimeField(default='00:00')
    day = models.CharField(choices=DayChoices,default=DayChoices.MON)

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
    male = models.PositiveIntegerField(_('number of males'),default=0)
    female = models.PositiveIntegerField(_('number of females'),default=0)
    children = models.PositiveIntegerField(_('number of children'),default=0)

    def __str__(self):
        return f"{self.church}_{self.service.name}_{self.service_date.date()}"

    @cached_property
    def total_offering(self):
        if self.offering.exists():
            add = models.F('frequency')*models.F('denomination')
            offerings = self.offering.annotate(add=Cast(add,output_field=models.FloatField()))
            offerings = offerings.values_list('add',flat=True)
            return sum(offerings)
        return None

    def total_attendance(self):
        return self.male + self.female + self.children
    
    def get_currency(self):
        if self.offering.exists():
            return self.offering.first().currency


class Offering(models.Model):
    class CurrrencyChoices(models.TextChoices):
        US_DOLLAR = 'USD'
        NIGERIAN_NAIRA = 'NGN'
        EURO = 'EUR'
        JAPANESE_YEN = 'JPY'
        POUND_STERLING = 'GBP'
        AUSTRALIAN_DOLLAR = 'AUD'
        CANADIAN_DOLLAR = 'CAD'
        SWISS_FRANC = 'CHF'
        CHINESE_RENMINBI = 'CNH'
        HONG_KONG_DOLLAR = 'HKD'
        NEW_ZEALAND_DOLLAR = 'NZD'

    uuid = models.UUIDField(default=uuid4,primary_key=True,editable=False)
    record = models.ForeignKey(
        ChurchRecord, on_delete=models.CASCADE, related_name='offering',default=None)
    currency = models.CharField(
        choices=CurrrencyChoices.choices,default=CurrrencyChoices.US_DOLLAR)
    denomination = models.DecimalField(decimal_places=2,max_digits=6,unique=True)
    frequency = models.PositiveIntegerField(default=0)
    
    @property
    def total(self):
        return self.frequency*self.denomination

    def __str__(self):
        return f'{self.denomination}x{self.frequency}'
    
    class Meta:
        ordering = ['denomination']