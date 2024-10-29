from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView


from . import views

app_name = 'authentication'

urlpatterns = [
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('login/', LoginView.as_view(), name='login'),
    path('log_out/', LogoutView.as_view(), name='logout'),
]