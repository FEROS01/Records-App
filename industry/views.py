from typing import Any
from django.db.models.base import Model as Model
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import (
    TemplateView, ListView, DetailView,UpdateView, CreateView)


from .models import Church, ChurchRecord,Offering
from .mixins import OfferingMixin


class IndexView(TemplateView):
    template_name = 'industry/index.html'

class ChurchListView(ListView):
    model = Church

class ChurchDetailView(DetailView):
    model = Church

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        data = super().get_context_data(**kwargs)
        print(data)
        return data
    
class ChurchRecordListView(ListView):
    model =  ChurchRecord

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        church = get_object_or_404(Church,uuid=self.church_uuid)
        context['church'] = church
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.church_uuid = self.kwargs['pk']
        church_records = queryset.filter(church__uuid=self.church_uuid)
        return church_records

class ChurchRecordDetailView(DetailView):
    model =  ChurchRecord

class OfferingUpdateView(OfferingMixin,UpdateView):
    model = Offering
    

class OfferingCreateView(OfferingMixin,CreateView):
    model =  Offering
    template_name = 'industry/offering_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['record'] = get_object_or_404(ChurchRecord,uuid=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        record_uuid = self.kwargs['pk']
        record = get_object_or_404(ChurchRecord,uuid=record_uuid)
        self.object.record = record
        print(self.object)
        self.object.save()
        print(self.object)
        return HttpResponseRedirect(self.get_success_url())