from django.urls import reverse
from django.contrib import messages as Msg
from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView


from .forms import NewUserCreationForm

class SignUpView(CreateView):
    model = get_user_model()
    form_class = NewUserCreationForm
    template_name = 'registration/sign_up.html'

    def get_success_url(self):
        return reverse('authentication:login')

    def form_valid(self, form) :
        Msg.info(self.request,'Succesfully created an account')
        return super().form_valid(form)
