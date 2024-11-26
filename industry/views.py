from typing import Any

from django.contrib import messages as Msg
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.db.models.base import Model as Model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin as TestMixin
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_uuid = self.request.user.uuid
        church = context['object'].church
        is_manager = church.managers.filter(uuid=user_uuid).exists()
        context['is_manager'] = is_manager
        return context

class OfferingUpdateView(
    LoginRequiredMixin,ErrorMixin,OfferingMixin,UpdateView):
    model = Offering

    def test_func(self):
        offering_uuid = self.kwargs['pk']
        offering = get_object_or_404(Offering,uuid=offering_uuid)
        church = offering.record.church
        user_uuid = self.request.user.uuid
        is_manager = church.managers.filter(uuid=user_uuid).exists()
        return is_manager

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
        user_uuid = self.request.user.uuid
        is_manager = church.managers.filter(uuid=user_uuid).exists()
        return is_manager

class OfferingDeleteView(DeleteView):
    model = Offering

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

class ServiceCreateView(LoginRequiredMixin,ServiceMixin,CreateView):
    model = Service
    template_name = 'industry/service_create.html'

    def form_valid(self, form):        
        church = get_object_or_404(Church,uuid=self.kwargs['pk'])
        self.object = form.save(commit=False)
        self.object.church = church
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['church'] = get_object_or_404(Church,uuid=self.kwargs['pk'])
        return context

class ServiceUpdateView(LoginRequiredMixin,ServiceMixin,UpdateView):
    model = Service

class ServiceDetailView(DetailView):
    model = Service

class PageErrorView(TemplateView):
    template_name = 'industry/error.html'