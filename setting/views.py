from django.urls import reverse
from django.contrib import messages as Msg
from django.views.generic import UpdateView,TemplateView,DetailView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

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

    def test_func(self):
        return self.request.user == self.get_object()