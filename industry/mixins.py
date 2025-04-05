from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect as Redirect


from .forms import ChurchRecordForm


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

class RecordMixin:
    form_class = ChurchRecordForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['church'] = self.church
        context['create'] = self.create
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['church_instance'] = self.church
        return kwargs
    
    def get_form(self, form_class = None):
        form = super().get_form(form_class)
        if self.request.method in ['POST', 'PUT']:
            form.instance.church = self.church
        return form


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