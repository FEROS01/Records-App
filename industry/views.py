from typing import Any

from django.urls import reverse
from django.contrib import messages as Msg
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models.base import Model as Model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import (
    TemplateView, ListView, DetailView, UpdateView, CreateView)


from .mixins import OfferingMixin,ChurchMixin
from .models import (
    Church, ChurchRecord, Offering, Service)


class IndexView(TemplateView):
    template_name = 'industry/index.html'

class ChurchListView(ListView):
    model = Church

class ChurchDetailView(DetailView):
    model = Church

class ChurchCreateView(LoginRequiredMixin,ChurchMixin,CreateView):
    model = Church
    template_name = 'industry/church_create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        self.object.managers.add(self.request.user)
        Msg.info(self.request,f'Successfully Registered {self.object.name}')
        return HttpResponseRedirect(self.get_success_url())

class ChurchUpdateView(LoginRequiredMixin,ChurchMixin,UpdateView):
    model = Church

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
        context['record'] = get_object_or_404(
            ChurchRecord,uuid=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        record_uuid = self.kwargs['pk']
        record = get_object_or_404(ChurchRecord,uuid=record_uuid)
        self.object.record = record
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

# class ServiceCreateView(CreateView):
#     model = Service

# class ServiceUpdateView(CreateView):
#     model = Service