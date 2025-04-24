from typing import Any


from django.db.models import Q
from django.urls import reverse
from django.contrib import messages as Msg
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.db.models.base import Model as Model
from django.views.decorators.http import require_GET
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import (
    TemplateView, ListView, DetailView, UpdateView, CreateView, DeleteView)

from .utils import search_users, setup_context
from .mixins import *
from .models import (
    Church, ChurchRecord, Offering, Service, Member)
from .forms import ChurchRecordForm


def set_timezone(request):
    django_timezone_exist = request.session.get('django_timezone',False)
    if request.method == "POST" and not django_timezone_exist:
        request.session["django_timezone"] = request.POST["timezone"]
    return HttpResponse('')

class IndexView(TemplateView):
    template_name = 'industry/index.html'

class ChurchListView(ListView):
    model = Church
    # paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.htmx:
            data = self.request.GET.get('q','')
            return queryset.filter(name__icontains=data)
        return queryset
    
    def get_template_names(self):
        if self.request.htmx:
            return ['industry/htmx_templates/church_list.html']
        return super().get_template_names()
    

class ChurchDetailView(DetailView):
    model = Church

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        church = self.get_object()
        context['is_manager'] = self.get_object().is_manager(self.request.user)
        service_pag = Paginator(church.service.all(),4)
        member_pag = Paginator(church.members.all(),4)

        context['services'] = service_pag.get_page(1)
        context['members'] = member_pag.get_page(1)

        if self.request.htmx:
            context = setup_context(self.request, church, context)
        return context
    
    def get_template_names(self):
        if self.request.htmx:
            search_type = self.request.GET.get('type','service')
            if search_type == 'service':
                return ['industry/htmx_templates/service_list.html']
            elif search_type == 'member':
                return ['industry/htmx_templates/member_list.html']
        return super().get_template_names()

@require_GET
def service_list(request,church_uuid):
    if request.htmx:
        church = get_object_or_404(Church,uuid=church_uuid)
        service_pag = Paginator(church.service.all(),4)
        page_num = request.GET.get('page',1)
        services = service_pag.get_page(page_num)
        context = {'services':services,'church':church}
        return render(request,'industry/htmx_templates/service_list.html',context)

@require_GET
def member_list(request,church_uuid):
    if request.htmx:
        church = get_object_or_404(Church,uuid=church_uuid)
        member_pag = Paginator(church.members.all(),4)
        page_num = request.GET.get('page',1)
        members = member_pag.get_page(page_num)
        context = {'members':members,'church':church}
        return render(request,'industry/htmx_templates/member_list.html',context)

class ChurchCreateView(LoginRequiredMixin,ChurchMixin,CreateView):
    model = Church
    template_name = 'industry/church_create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        self.object.managers.add(self.request.user)
        Msg.success(self.request,f'Successfully Registered {self.object.name}')
        return HttpResponseRedirect(self.get_success_url())

class ChurchUpdateView(
    LoginRequiredMixin,ErrorMixin,ChurchMixin,UpdateView):
    model = Church
    
    def form_valid(self, form):
        Msg.success(self.request,f'Successfully updated {self.object.name}')
        return super().form_valid(form)

    def test_func(self):
        church = self.get_object()
        user_uuid = self.request.user.uuid
        is_manager = church.managers.filter(uuid=user_uuid).exists()
        return is_manager
    
class ChurchManagerUpdateView(ChurchUpdateView):
    fields = ("managers",)
    template_name = "industry/manager_update.html"

    def form_valid(self, form):
        Msg.success(self.request,f'Successfully Added Managers to {self.object.name}')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_list'] = get_user_model().objects.all()

        if self.request.htmx:
            search = self.request.GET.get('q','')
            context['user_list'] = search_users(search)
            
        church = self.get_object()
        managers = church.managers.values_list('uuid',flat=True)
        context['managers'] = {n:m for n,m in enumerate(managers)}

        return context

class ChurchRecordListView(ListView):
    model =  ChurchRecord
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        church = get_object_or_404(Church,uuid=self.church_uuid)
        context['church'] = church
        context['is_manager'] = church.is_manager(self.request.user)

        if self.request.htmx:
            data = self.request.GET.get('q','')
            page = self.request.GET.get('page',1)
            
            records = ChurchRecord.objects.filter(
                Q(church__uuid=self.church_uuid),
                Q(service__name__icontains=data)|
                Q(sermon_title__icontains=data)
            )
            if not data:
                record_pag = Paginator(records,self.paginate_by)
                records = record_pag.get_page(page)
            context = {"records":records}
        return context

    def get_template_names(self):
        if self.request.htmx:
            return ['industry/htmx_templates/record_list.html']
        return super().get_template_names()

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

class ChurchRecordCreateView(
    LoginRequiredMixin,ErrorMixin,RecordMixin,CreateView):
    model = ChurchRecord
    template_name = 'industry/churchrecord_create.html'
    create = True
    
    def form_valid(self, form):
        Msg.success(self.request,f'Successfully added record')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('industry:church_record_list',kwargs={'pk':self.kwargs['pk']})
    
    def test_func(self):
        church = get_object_or_404(Church,uuid=self.kwargs['pk'])
        self.church = church
        return church.is_manager(self.request.user)
    
class ChurchRecordUpdateView(
    LoginRequiredMixin,ErrorMixin,RecordMixin,UpdateView):
    model = ChurchRecord
    create = False
    
    def form_valid(self, form):
        Msg.success(self.request,f'Successfully updated record')
        return super().form_valid(form)

    def get_success_url(self):
        uuid = self.object.uuid
        return reverse('industry:church_record_detail',kwargs={'pk':uuid})
    
    def test_func(self):
        record = self.get_object()
        church = record.church
        self.church = church
        return church.is_manager(self.request.user)

class AttendanceUpdateView(LoginRequiredMixin,ErrorMixin,UpdateView):
    model =  ChurchRecord
    template_name = 'industry/attendance_form.html'
    fields = ('male','female','children')

    def form_valid(self, form):
        Msg.success(self.request,f'Successfully updated attendance')
        return super().form_valid(form)

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

    def form_valid(self, form):
        Msg.success(self.request,f'Successfully updated offerring')
        return super().form_valid(form)

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
        Msg.success(self.request,f'Successfully added offerring')
        return HttpResponseRedirect(self.get_success_url())

    def test_func(self):
        record = self.get_record_object()
        church = record.church
        user = self.request.user
        return church.is_manager(user)

class OfferingDeleteView(LoginRequiredMixin,ErrorMixin,DeleteView):
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
            Msg.success(self.request,f'Successfully added {self.object.name} service')

            return HttpResponseRedirect(self.get_success_url())
        return HttpResponseRedirect(reverse('core:restricted'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['church'] = get_object_or_404(Church,uuid=self.kwargs['pk'])
        return context

class ServiceUpdateView(LoginRequiredMixin,ErrorMixin,ServiceMixin,UpdateView):
    model = Service
     
    def form_valid(self, form):
        Msg.success(self.request,f'Successfully updated {self.object.name} service')
        return super().form_valid(form) 
    def test_func(self):
        service = self.get_object()
        church = service.church
        user = self.request.user
        return church.is_manager(user)

class ServiceDetailView(DetailView):
    model = Service

class MemberCreateView(LoginRequiredMixin,ErrorMixin,CreateView):
    model = Member
    template_name = 'industry/member_create.html'
    fields = ('first_name','last_name','position')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        church_uuid = self.kwargs['pk']
        church = get_object_or_404(Church,uuid=church_uuid)
        context['church'] = church
        return context
    
    def form_valid(self, form):        
        church = get_object_or_404(Church,uuid=self.kwargs['pk'])
        self.object = form.save()
        church.members.add(self.object)
        Msg.success(self.request,f'Successfully added {self.object.full_name}')
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        church_uuid = self.kwargs['pk']
        return reverse('industry:church_detail',kwargs={'pk':church_uuid})
        
    def test_func(self):
        church = get_object_or_404(Church,uuid=self.kwargs['pk'])
        user = self.request.user
        return church.is_manager(user)