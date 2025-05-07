from django.urls import reverse
from django.contrib import messages as Msg
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_GET
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView,TemplateView,DetailView

from industry.mixins import ErrorMixin

class SettingView(LoginRequiredMixin,TemplateView):
    template_name = 'setting/settings.html'

class UserUpdateView(LoginRequiredMixin,ErrorMixin,UpdateView):
    model = get_user_model()
    fields = ('email','username','first_name','last_name')
    template_name = 'setting/user_update.html'

    def get_success_url(self):
        Msg.success(self.request,f'Successfully updated your profile')
        return reverse('setting:settings')
    
    def test_func(self):
        return self.request.user == self.get_object()

class UserDetailView(LoginRequiredMixin,ErrorMixin,DetailView):
    model = get_user_model()
    template_name = 'setting/user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        churches = self.get_object().church_industry.all()
        church_pag = Paginator(churches,4)
        church_list = church_pag.get_page(1)

        if self.request.htmx:
            data = self.request.GET.get('q','')
            page = self.request.GET.get('page',1)

            if data:
                church_list = churches.filter(name__icontains=data)
            else:
                church_list = church_pag.get_page(page)
                context['page_obj'] = church_list
        
        context['church_list'] = church_list
        return context

    def get_template_names(self):
        if self.request.htmx:
            return ['industry/htmx_templates/church_list.html']
        return super().get_template_names()

    def test_func(self):
        return self.request.user == self.get_object()