from django.urls import path

from . import views

app_name = 'industry'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('church_list/', views.ChurchListView.as_view(), name='church_list'),
    path('church_detail/<uuid:pk>', views.ChurchDetailView.as_view(), name='church_detail'),
    path('church_create/', views.ChurchCreateView.as_view(), name='church_create'),
    path('church_update/<uuid:pk>', views.ChurchUpdateView.as_view(), name='church_update'),
    path('church_record_list/<uuid:pk>', views.ChurchRecordListView.as_view(), name='church_record_list'),
    path('church_record_detail/<uuid:pk>', views.ChurchRecordDetailView.as_view(), name='church_record_detail'),
    path('offering_update/<uuid:pk>', views.OfferingUpdateView.as_view(), name='offering_update'),
    path('offering_create/<uuid:pk>', views.OfferingCreateView.as_view(), name='offering_create'),
]