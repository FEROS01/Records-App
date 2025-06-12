from django.urls import path,include
from django.contrib.auth.views import LoginView,LogoutView,PasswordResetView


from . import views
from .forms import NewPasswordResetForm

app_name = 'authentication'

urlpatterns = [
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('login/', LoginView.as_view(), name='login'),
    path('log_out/', LogoutView.as_view(), name='logout'),
    path('password_reset/', PasswordResetView.as_view(
        html_email_template_name='registration/password_reset_email.html',
        email_template_name='registration/password_reset_email.html',
        template_name='registration/password_reset_form.html',
        form_class=NewPasswordResetForm), name='password_reset'),
    path("", include("django.contrib.auth.urls")),
]