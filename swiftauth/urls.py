
from django.urls import path,include
from swiftauth import views

urlpatterns = [
    path('', views.welcomeView, name='welcomeView'),
    path('admin_login', views.admin_loginView, name='admin_loginView'),
    path('dashboard', views.dashboardView, name='dashboardView'),
    path('email', views.email, name='email'),
    path('send_email_view', views.send_email_view, name='send_email_view'),
    path('send_sms_view', views.send_sms_view, name='send_sms_view'),
    
    path('send_template1_email/<int:id>', views.send_template1_email_view, name='send_template1_email_view'),
    path('send_template2_email/<int:id>', views.send_template2_email_view, name='send_template2_email_view'),
    path('send_template3_email/<int:id>', views.send_template3_email_view, name='send_template3_email_view'),
    path('send_template4_email/<int:id>', views.send_template4_email_view, name='send_template4_email_view'),

    
    path('schedule_email_view', views.schedule_email_view, name='schedule_email_view'),
    path('schedule_sms_view', views.schedule_sms_view, name='schedule_sms_view'),

    path('log_out', views.admin_logoutView, name='admin_logoutView'),
    path('admin_profile', views.admin_profileView, name='admin_profileView'),
    path('update_profile', views.update_profileView, name='update_profileView'),
]
