from .models import Offering
from django.urls import reverse
from django.shortcuts import get_object_or_404

class OfferingMixin:
    fields = ('currency','denomination','frequency')
    
    def get_success_url(self):
        uuid = self.object.record.uuid
        return reverse('industry:church_record_detail',kwargs={'pk':uuid})