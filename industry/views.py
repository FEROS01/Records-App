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
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse, Http404
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
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.htmx:
            data = self.request.GET.get('q','')
            if data:
                churches = Church.objects.filter(name__icontains=data)
                context['church_list'] = churches
        return context    

    def get_template_names(self):
        if self.request.htmx:
            return ['industry/htmx_templates/church_list.html']
        return super().get_template_names()
    

class ChurchDetailView(DetailView):
    model = Church

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        church = self.get_object()
        is_manager = self.get_object().is_manager(self.request.user)
        members = church.members.all()
        services = church.service.all()

        if not is_manager:
            services = services.exclude(visible=False)
        
        member_pag = Paginator(members,4)
        service_pag = Paginator(services,4)
        

        context['services'] = service_pag.get_page(1)
        context['members'] = member_pag.get_page(1)

        if self.request.htmx:
            context = setup_context(self.request, members, services, context)
        context['is_manager'] = is_manager
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

class ChurchDeleteView(LoginRequiredMixin,ErrorMixin,DeleteView):
    model = Church
    template_name = 'industry/htmx_templates/confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url = reverse('industry:church_delete',kwargs={'pk':self.get_object().pk})
        context['url'] = url
        context['info'] = f'Are you sure you want to delete {self.get_object().name}?'
        context['add_info'] = 'This action is irreversible'
        return context

    def get_success_url(self):
        Msg.success(self.request,f'Successfully deleted {self.get_object().name}')
        return reverse('industry:church_list')

    def test_func(self):
        church = self.get_object()
        return church.is_manager(self.request.user)

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
            context = {'page':False}
            
            records = ChurchRecord.objects.filter(
                Q(church__uuid=self.church_uuid),
                Q(service__name__icontains=data)|
                Q(sermon_title__icontains=data)
            )
    
            if not data:
                record_pag = Paginator(records,self.paginate_by)
                records = record_pag.get_page(page)
                context['page'] = True

            context["records"] = records
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
        return reverse('industry:church_record_detail',kwargs={'pk':self.object.uuid})
    
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

class ChurchRecordDeleteView(LoginRequiredMixin,ErrorMixin,DeleteView):
    model = ChurchRecord
    template_name = 'industry/htmx_templates/confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url = reverse('industry:record_delete',kwargs={'pk':self.get_object().pk})
        context['url'] = url
        context['info'] = f'Are you sure you want to delete record from {self.get_object().service.name} service?'
        return context

    def get_success_url(self):
        Msg.success(self.request,'Successfully deleted record')
        return reverse('industry:church_record_list',kwargs={'pk':self.object.church.uuid})
    
    def test_func(self):
        church = self.get_object().church
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
    template_name = 'industry/htmx_templates/confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url = reverse('industry:offering_delete',kwargs={'pk':self.get_object().pk})
        context['url'] = url
        context['info'] = f'Are you sure you want to remove {self.get_object().denomination}?'
        context['add_info'] = 'This action is irreversible'
        return context

    def get_success_url(self):
        record_uuid = self.object.record.uuid
        Msg.success(self.request,f'Successfully deleted {self.object.denomination} {self.object.currency}')
        return reverse(
            'industry:church_record_detail',kwargs={'pk':record_uuid})

    def test_func(self):
        church = self.get_object().record.church
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        church = self.get_object().church
        context['is_manager'] = church.is_manager(self.request.user)
        service_records = self.get_object().service_record.all()
        record_pag = Paginator(service_records,4)
        records = record_pag.get_page(1)
    
        if self.request.htmx:
                data = self.request.GET.get('q','')
                page = self.request.GET.get('page',1)
                context['page'] = True

                if data:
                    records = service_records.filter(
                        sermon_title__icontains=data
                    )
                    context['page'] = False
                else:
                    records = record_pag.get_page(page)
        
        context['records'] = records
        return context
    
    def get_template_names(self):
        if self.request.htmx:
            return ['industry/htmx_templates/record_list.html']
        return super().get_template_names()

class ServiceDeleteView(LoginRequiredMixin,ErrorMixin,DeleteView):
    model = Service
    template_name = 'industry/htmx_templates/confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url = reverse('industry:service_delete',kwargs={'pk':self.get_object().pk})
        context['url'] = url
        context['info'] = f'Are you sure you want to delete {self.get_object().name} service?'
        return context

    def get_success_url(self):
        Msg.success(self.request,f'Successfully deleted {self.get_object().name}')
        church_uuid = self.get_object().church.uuid
        return reverse('industry:church_detail',kwargs={'pk':church_uuid})
    
    def test_func(self):
        church = self.get_object().church
        return church.is_manager(self.request.user)

@login_required
def service_visibility(request,pk):
    service = get_object_or_404(Service,uuid=pk)
    context = {}
    church = service.church

    if not church.is_manager(request.user):
        return redirect('core:restricted')

    elif request.method == 'GET':
        url = reverse('industry:service_visibility',kwargs={'pk':service.pk})
        context['url'] = url
        context['info'] = f'Are you sure you want to hide {service.name} service?'
        context['add_info'] = 'Users will not be able view this service'
        return render(request,'industry/htmx_templates/confirm_delete.html',context=context)
    
    elif request.method == 'POST':
        service.visible = False if service.visible else True
        service.save()
        Msg.success(request,f'{service.name} has been updated')
        return redirect('industry:service_detail',pk=service.uuid)

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

class MemberDeleteView(LoginRequiredMixin,ErrorMixin,DeleteView):
    model = Member
    template_name = 'industry/htmx_templates/confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url = reverse('industry:member_delete',kwargs={'pk':self.get_object().pk})
        context['url'] = url
        context['info'] = f'Are you sure you want to remove {self.get_object().full_name}?'
        context['add_info'] = 'This action is irreversible'
        return context

    def get_success_url(self):
        Msg.success(self.request,f'Successfully deleted {self.get_object().full_name}')
        church_uuid = self.church.uuid
        return reverse('industry:church_detail',kwargs={'pk':church_uuid})

    def test_func(self):
        self.church = self.get_object().church_industry.first()
        return self.church.is_manager(self.request.user)