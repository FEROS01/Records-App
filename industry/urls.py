from django.urls import path

from . import views

app_name = 'industry'

urlpatterns = [
    path('landing/', views.LandingView.as_view(), name='index'),
    path('', views.IndexView.as_view(), name='index'),
    path('set_tz/', views.set_timezone, name='set_timezone'),
    path('service_list/<uuid:church_uuid>', views.service_list, name='service_list'),
    path('member_list/<uuid:church_uuid>', views.member_list, name='member_list'),
    path('church_delete/<uuid:pk>', views.ChurchDeleteView.as_view(), name='church_delete'),
    path('record_delete/<uuid:pk>', views.ChurchRecordDeleteView.as_view(), name='record_delete'),
    path('offering_delete/<uuid:pk>', views.OfferingDeleteView.as_view(), name='offering_delete'),
    path('service_visibility/<uuid:pk>', views.service_visibility, name='service_visibility'),
    path('member_delete/<int:pk>', views.MemberDeleteView.as_view(), name='member_delete'),

    #Church Model URLs
    path('church_list/', views.ChurchListView.as_view(), name='church_list'),
    path('church_detail/<uuid:pk>', views.ChurchDetailView.as_view(), name='church_detail'),
    path('church_create/', views.ChurchCreateView.as_view(), name='church_create'),
    path('church_update/<uuid:pk>', views.ChurchUpdateView.as_view(), name='church_update'),
    path('church_manager_update/<uuid:pk>', views.ChurchManagerUpdateView.as_view(), name='manager_update'),

    #ChurchRecord Model URLs
    path('church_record_list/<uuid:pk>', views.ChurchRecordListView.as_view(), name='church_record_list'),
    path('church_record_detail/<uuid:pk>', views.ChurchRecordDetailView.as_view(), name='church_record_detail'),
    path('church_record_create/<uuid:pk>', views.ChurchRecordCreateView.as_view(), name='record_create'),
    path('church_record_update/<uuid:pk>', views.ChurchRecordUpdateView.as_view(), name='record_update'),
    path('attendance_update/<uuid:pk>', views.AttendanceUpdateView.as_view(), name='attendance_update'),

    #Offering Model URLs
    path('offering_update/<uuid:pk>', views.OfferingUpdateView.as_view(), name='offering_update'),
    path('offering_create/<uuid:pk>', views.OfferingCreateView.as_view(), name='offering_create'),

    #Service Model URLs
    path('service_create/<uuid:pk>', views.ServiceCreateView.as_view(), name='service_create'),
    path('service_update/<uuid:pk>', views.ServiceUpdateView.as_view(), name='service_update'),
    path('service_detail/<uuid:pk>', views.ServiceDetailView.as_view(), name='service_detail'),

    #Member Model URLs
    path('member_create/<uuid:pk>', views.MemberCreateView.as_view(), name='member_create'),
]