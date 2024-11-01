from django.urls import reverse

class OfferingMixin:
    fields = ('currency','denomination','frequency')
    
    def get_success_url(self):
        uuid = self.object.record.uuid
        return reverse('industry:church_record_detail',kwargs={'pk':uuid})
    
class ChurchMixin:
    fields = ('name','owner','head_pastor','website','date_established')
    
    def get_success_url(self):
        uuid = self.object.uuid
        return reverse('industry:church_detail',kwargs={'pk':uuid})