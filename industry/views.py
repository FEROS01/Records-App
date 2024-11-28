from typing import Any

from django.contrib import messages as Msg
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.db.models.base import Model as Model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import (
    TemplateView, ListView, DetailView, UpdateView, CreateView, DeleteView)

from .mixins import (
    OfferingMixin, ChurchMixin, ServiceMixin, ErrorMixin)
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

class ChurchUpdateView(
    LoginRequiredMixin,ErrorMixin,ChurchMixin,UpdateView):
    model = Church

    def test_func(self):
        church = self.get_object()
        user_uuid = self.request.user.uuid
        is_manager = church.managers.filter(uuid=user_uuid).exists()
        return is_manager

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        church = context['object'].church
        context['is_manager'] = church.is_manager(user)
        return context

class ChurchRecordUpdateView(ErrorMixin,UpdateView):
    model =  ChurchRecord
    fields = ('male','female','children')

    def get_success_url(self):
        uuid = self.object.uuid
        return reverse('industry:church_record_detail',kwargs={'pk':uuid})
    
    def test_func(self):
        record = self.get_object()
        church = record.church
        user = self.request.user
        return church.is_manager(user)

class OfferingUpdateView(
    LoginRequiredMixin,ErrorMixin,OfferingMixin,UpdateView):
    model = Offering

    def test_func(self):
        offering = self.get_object()
        church = offering.record.church
        user = self.request.user
        return church.is_manager(user)

class OfferingCreateView(
    LoginRequiredMixin,ErrorMixin,OfferingMixin,CreateView):
    model =  Offering
    template_name = 'industry/offering_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['record'] = get_object_or_404(
            ChurchRecord,uuid=self.kwargs['pk'])
        return context

    def get_record_object(self):
        record_uuid = self.kwargs['pk']
        record = get_object_or_404(ChurchRecord,uuid=record_uuid)
        return record

    def form_valid(self, form):
        self.object = form.save(commit=False)
        record = self.get_record_object()
        self.object.record = record
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def test_func(self):
        record = self.get_record_object()
        church = record.church
        user = self.request.user
        return church.is_manager(user)

class OfferingDeleteView(ErrorMixin,DeleteView):
    model = Offering
    template_name = 'core/confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        record_uuid = self.kwargs['pk2']
        church_record = get_object_or_404(ChurchRecord,uuid=record_uuid)
        context['record'] = church_record
        return context

    def get_success_url(self):
        record_uuid = self.kwargs['pk2']
        return reverse(
            'industry:church_record_detail',kwargs={'pk':record_uuid})
    
    def test_func(self):
        record_uuid = self.kwargs['pk2']
        record = get_object_or_404(ChurchRecord,uuid=record_uuid)
        church = record.church
        user = self.request.user
        return church.is_manager(user)

class ServiceCreateView(LoginRequiredMixin,ServiceMixin,CreateView):
    model = Service
    template_name = 'industry/service_create.html'

    def form_valid(self, form):        
        church = get_object_or_404(Church,uuid=self.kwargs['pk'])
        user = self.request.user
        is_manager = church.managers.filter(uuid=user.uuid).exists()
        if is_manager:
            self.object = form.save(commit=False)
            self.object.church = church
            self.object.save()
            return HttpResponseRedirect(self.get_success_url())
        return HttpResponseRedirect(reverse('core:restricted'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['church'] = get_object_or_404(Church,uuid=self.kwargs['pk'])
        return context

class ServiceUpdateView(LoginRequiredMixin,ErrorMixin,ServiceMixin,UpdateView):
    model = Service

    def test_func(self):
        service = self.get_object()
        church = service.church
        user = self.request.user
        return church.is_manager(user)

class ServiceDetailView(DetailView):
    model = Service
