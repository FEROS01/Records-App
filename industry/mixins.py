from django.urls import reverse

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