from django.shortcuts import render
from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth.models import User,auth
from django.contrib import  messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.db.models import Count,Sum
from django.db.models import Q
from twilio.rest import Client
from decouple import config
import datetime
from datetime import datetime
import csv
from datetime import date
import threading
from django.db import transaction
from swiftauth.models import *
from random_id import random_id
import string 
import requests
from twilio.rest import Client
from django.conf import settings
import twilio
from management.models import *
from requests.auth import HTTPBasicAuth
from .tasks import send_bulk_emails_task
from .tasks1 import send_bulk_sms_task
from .schedule_email_tasks import schedule_bulk_emails_task
from .schedule_sms_tasks import schedule_bulk_sms_task
from .tasks2 import send_bulk_template1_emails_task
from .tasks3 import send_bulk_template2_emails_task
from .tasks4 import send_bulk_template3_emails_task
from .tasks5 import send_bulk_template4_emails_task

from django.utils import timezone
from django.core.paginator import Paginator


# basic = HTTPBasicAuth(settings.API_KEY,settings.API_SECRET)


def welcomeView(request):
    return render(request,'temp/index.html')
    
@transaction.atomic
def admin_loginView(request):
    if request.method =="POST" and request.POST['username'] and request.POST['password']:
        username = request.POST['username']
        password =request.POST['password']
                
        if not User.objects.filter(username=username).exists():
            messages.info(request,'Incorrect login credentials.')
            return redirect('/')  
        
        userlog = auth.authenticate(username=username,password=password)
        # checking if it is an existing user in the database
        
        # customise error messages handler
        if userlog is not None:
            auth.login(request, userlog)
            if request.user.is_authenticated and request.user.is_admin and request.user.is_activation:
                return redirect('/dashboard')
        else:
            messages.info(request,"Incorrect login credentials.")
            return redirect('/')
        
        if userlog is not None:
            auth.login(request, userlog)
            if request.user.is_authenticated and not request.user.is_activation:
                messages.info(request,"Your acount is not activated ")
                return redirect('/')
            
        
        if userlog is not None:
            auth.login(request, userlog)
            if request.user.is_authenticated and request.user.is_worker and request.user.is_activation:
                return redirect('/customer_dashboard')
        else:
            messages.info(request,"Incorrect login credentials.")
            return redirect('/')
                
    else:
        return redirect('/')  
    
    
# def admin_logoutView(request):
#     auth.logout(request)
#     messages.info(request,"Logout Successfully")
#     return redirect('/') 



@login_required
def admin_logoutView(request):
    for key in list(request.session.keys()):
        del request.session[key]
    auth.logout(request)
    return redirect('/') 



@login_required(login_url='/')  
def dashboardView(request):
    if request.user.is_authenticated and request.user.is_admin:
        list_of_all_users = User.objects.filter(is_customer=True).order_by('-date_joined')
        email_send_log = EmailLog.objects.filter().order_by('-created_at')
        email_send_log_count = EmailLog.objects.all().count()
        student_paginator = Paginator(email_send_log,10)
        page_number = request.GET.get('page')
        page_obj = student_paginator.get_page(page_number)
        data = {
            'list_of_all_users':list_of_all_users,
            'page_obj':page_obj,
            'email_send_log_count':email_send_log_count
        }
        return render(request,'temp/dashboard.html',context=data)



def email(request):
    return render(request,'temp/email.html')


@transaction.atomic
@login_required(login_url='/')  
def send_template1_email_view(request,id):
    if request.user.is_authenticated and request.user.is_admin:
        company_username=request.user.username
        send_bulk_template1_emails_task.delay(id,company_username)
        Template1.objects.filter(id=id).update(status=True)
        messages.info(request,"Email sending task has been queued be patient......")
        return redirect('/message')
    else:
        messages.info(request,"Email could not be sent")
        return redirect('/message')

@transaction.atomic
@login_required(login_url='/')  
def send_template2_email_view(request,id):
    if request.user.is_authenticated and request.user.is_admin:
        company_username=request.user.username
        send_bulk_template2_emails_task.delay(id,company_username)
        Template2.objects.filter(id=id).update(status=True)
        messages.info(request,"Email sending task has been queued be patient......")
        return redirect('/message')
    else:
        messages.info(request,"Email could not be sent")
        return redirect('/message')
    
@transaction.atomic
@login_required(login_url='/')  
def send_template3_email_view(request,id):
    if request.user.is_authenticated and request.user.is_admin:
        company_username=request.user.username
        send_bulk_template3_emails_task.delay(id,company_username)
        Template3.objects.filter(id=id).update(status=True)
        messages.info(request,"Email sending task has been queued be patient......")
        return redirect('/message')
    else:
        messages.info(request,"Email could not be sent")
        return redirect('/message')
    
@transaction.atomic
@login_required(login_url='/')  
def send_template4_email_view(request,id):
    if request.user.is_authenticated and request.user.is_admin:
        company_username=request.user.username
        send_bulk_template4_emails_task.delay(id,company_username)
        Template4.objects.filter(id=id).update(status=True)
        messages.info(request,"Email sending task has been queued be patient......")
        return redirect('/message')
    else:
        messages.info(request,"Email could not be sent")
        return redirect('/message')

@login_required(login_url='/')  
def send_email_view(request):
    if request.method =="POST" and request.POST['subject'] and request.POST['greetings'] and request.POST['introtext'] and request.POST['message']:
        subject =request.POST['subject']
        greetings =request.POST['greetings']
        introtext =request.POST['introtext']
        message =request.POST['message']
        companu_instance_name=request.user.username
        # Call Celery task to send bulk emails
        send_bulk_emails_task.delay(subject,message,introtext,greetings,companu_instance_name)
        messages.info(request,"Email sending task has been queued be patient......")
        return redirect('/message')
    else:
        messages.info(request,"Email could not be sent")
        return redirect('/message')
    
    
@login_required(login_url='/')  
def send_sms_view(request):
    if request.method =="POST" and request.POST['greetings'] and request.POST['message']:
        greetings =request.POST['greetings']
        message =request.POST['message']
        companu_instance_name=request.user.username
        # Call Celery task to send bulk SMS
        send_bulk_sms_task.delay(greetings,message,companu_instance_name)
        messages.info(request,"SMS sending task has been queued be patient......")
        return redirect('/message')
    else:
        messages.info(request,"SMS could not be sent")
        return redirect('/message')


def admin_profileView(request):
    list_of_all_users = User.objects.filter(is_customer=True).order_by('-date_joined')
    admin_instance_name = request.user.username
    admin_instance=User.objects.get(username=admin_instance_name)
    total_num_of_users=User.objects.all().count()
    data = {
    'list_of_all_users':list_of_all_users,
    'admin_instance':admin_instance,
    'total_num_of_users':total_num_of_users
    }
    return render(request,'temp/admin_profile.html',context=data)




@transaction.atomic
@login_required(login_url='/')  
def update_profileView(request):
    if request.user.is_authenticated and request.user.is_admin and request.method =="POST":        
        if len(request.FILES) != 0:
            admin_user = request.user.username
            admin_instance =User.objects.get(username=admin_user)
            admin_instance.logo=request.FILES['logo']
            admin_instance.companyname = request.POST['companyname']
            admin_instance.reg = request.POST['reg']
            admin_instance.tax = request.POST['tax']
            admin_instance.tel = request.POST['tel']
            admin_instance.whatsapp = request.POST['whatsapp']
            admin_instance.address = request.POST['address']
            admin_instance.website = request.POST['website']
            admin_instance.save()
            messages.info(request,"Company profile has been updated successfully")
            return redirect('/admin_profile')
        if len(request.FILES) == 0:
            admin_user = request.user.username
            admin_instance =User.objects.get(username=admin_user)
            admin_instance.companyname = request.POST['companyname']
            admin_instance.reg = request.POST['reg']
            admin_instance.tax = request.POST['tax']
            admin_instance.tel = request.POST['tel']
            admin_instance.whatsapp = request.POST['whatsapp']
            admin_instance.address = request.POST['address']
            admin_instance.website = request.POST['website']
            admin_instance.save()
            messages.info(request,"Company profile has been updated successfully")
            return redirect('/admin_profile')
    else:
        return redirect('/admin_profile')  
    


@login_required(login_url='/')  
def schedule_email_view(request):
    if request.method =="POST" and request.POST['subject'] and request.POST['greetings'] and request.POST['introtext'] and request.POST['message'] and request.POST['minutes']:
        subject =request.POST['subject']
        greetings =request.POST['greetings']
        introtext =request.POST['introtext']
        message =request.POST['message']
        minutes =int(request.POST['minutes'])
        companu_instance_name=request.user.username
        # Call Celery task to send bulk emails
        # Schedule the email task to be executed at a specific time
        # Here, we're scheduling it to be executed 5 minutes from the current time
        scheduled_time = timezone.now() + timezone.timedelta(minutes=minutes)
        schedule_bulk_emails_task.apply_async(args=[subject, message, introtext,greetings,companu_instance_name],eta=scheduled_time)
        messages.info(request,"Email Schedule task has been queued be patient......")
        return redirect('/message')
    else:
        messages.info(request,"Email Schedule task could not be sent")
        return redirect('/message')
    
@login_required(login_url='/')  
def schedule_sms_view(request):
    if request.method =="POST" and request.POST['greetings'] and request.POST['message']:
        greetings =request.POST['greetings']
        message =request.POST['message']
        companu_instance_name=request.user.username
        # Call Celery task to send bulk SMS
        schedule_bulk_sms_task.delay(greetings,message,companu_instance_name)
        messages.info(request,"SMS sending task has been queued be patient......")
        return redirect('/message')
    else:
        messages.info(request,"SMS could not be sent")
        return redirect('/message')
    
    
    
def pagenotfoundView(request, exception):
    return render(request,'error/404.html')

def my_custom_error_view(request):
    return render(request,'error/505.html',status=500)

# def my_custom_permission_denied_view(request,exception):
#     return render(request,'customer/error_message.html',status=403)

# def my_custom_bad_request_view(request,exception):
#     return render(request,'customer/error_message.html',status=400)


