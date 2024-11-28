from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect as Redirect


from .models import Offering


class OfferingMixin:
    fields = ('currency','denomination','frequency')
    
    def get_success_url(self):
        uuid = self.object.record.uuid
        return reverse('industry:church_record_detail',kwargs={'pk':uuid})
    
class ChurchMixin:
    fields = ('name','owner','head_pastor','website','date_established','about')
    
    def get_success_url(self):
        uuid = self.object.uuid
        return reverse('industry:church_detail',kwargs={'pk':uuid})

class ServiceMixin:
    fields = ('name','description','day','start_time','end_time')

    def get_success_url(self):
        uuid = self.object.uuid
        return reverse('industry:service_detail',kwargs={'pk':uuid})
    
class ErrorMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.test_func():
            return super().dispatch(request, *args, **kwargs)
        return Redirect(reverse('core:restricted'))