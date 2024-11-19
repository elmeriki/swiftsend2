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
import pandas as pd
from management.models import *
from requests.auth import HTTPBasicAuth
from django.core.paginator import Paginator
basic = HTTPBasicAuth(settings.API_KEY,settings.API_SECRET)
from mailjet_rest import Client
import rabbitmq_client


@login_required(login_url='/')  
def add_customerView(request):
    if request.user.is_authenticated and request.user.is_admin:
        list_of_all_users = User.objects.filter(is_customer=True).order_by('-date_joined')
        data = {
            'list_of_all_users':list_of_all_users
        }
        return render(request,'temp/add.html',context=data)
    

@transaction.atomic
@login_required(login_url='/')  
def register_customerView(request):
    if request.user.is_authenticated and request.user.is_admin and request.method == "POST" and request.POST['firstname'] and request.POST['lastname'] and request.POST['cellphone'] and request.POST['email']:
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        cellphonenumber=str(request.POST['cellphone'])
        email=request.POST['email']
        sacode="+27"
        my_dob_value = request.POST.get('dob', None)
        if my_dob_value:
            dob=request.POST['dob']
        if not my_dob_value:
            dob="2080-04-01"
        if len(cellphonenumber) > 10:
            messages.info(request,"Enter cellphone without country code")
            return redirect('/add')
        elif len(cellphonenumber) < 10:
            messages.info(request,"Incompleted cell phone number")
            return redirect('/add')
        if User.objects.filter(username=cellphonenumber).exists():
                messages.info(request,"Cell Phone Number has been used already")
                return redirect('/add')
            
        if User.objects.filter(email=email).exists():
                messages.info(request,"Email address has been used already")
                return redirect('/add')
        
        formatedcellphone = str((cellphonenumber)[1:10])
        formtaedcellphonenumber = str(f"{sacode}{formatedcellphone}")
        userid = random_id(length=8,character_set=string.digits)
        create_new_customer_account=User.objects.create_user(id=userid,username=cellphonenumber,first_name=firstname,last_name=lastname,password=cellphonenumber,is_customer=True,email=email,is_activation=True,phone=cellphonenumber,birth_date=dob)
        if create_new_customer_account:
            create_new_customer_account.save()
            messages.info(request,"Hi! New Account has been added successfully")
            return redirect('/add')

        else:
            messages.info(request,"Account could not be created successfully")
            return redirect('/add')




@login_required(login_url='/')  
def user_infoView(request,user_id):
    if request.user.is_authenticated and request.user.is_admin:
        list_of_all_users = User.objects.filter(is_customer=True).order_by('-date_joined')
        single_user_instance = User.objects.get(id=user_id)
        data = {
            'list_of_all_users':list_of_all_users,
            'single_user_instance':single_user_instance,
            'single_user_email_log':EmailLog.objects.filter(email=single_user_instance.email)[:2],
            'single_user_sms_log':Smslog.objects.filter(phone=single_user_instance.phone)[:2]

        }
        return render(request,'temp/user_info.html',context=data)
    
@login_required(login_url='/')  
def send_smsView(request):
    if request.user.is_authenticated and request.user.is_admin:
        list_of_all_users = User.objects.filter(is_customer=True).order_by('-date_joined')
        data = {
            'list_of_all_users':list_of_all_users,
            'send_sms_queue_status':Messagescontent.objects.filter(type="Sms",status="0").count()
        }
        return render(request,'temp/send_sms.html',context=data)
    
@login_required(login_url='/')  
def schedule_send_emailView(request):
    if request.user.is_authenticated and request.user.is_admin:
        list_of_all_users = User.objects.filter(is_customer=True).order_by('-date_joined')
        data = {
            'list_of_all_users':list_of_all_users,
        }
        return render(request,'temp/schedule_send_email.html',context=data)
    
@login_required(login_url='/')  
def schedule_send_smsView(request):
    if request.user.is_authenticated and request.user.is_admin:
        list_of_all_users = User.objects.filter(is_customer=True).order_by('-date_joined')
        data = {
            'list_of_all_users':list_of_all_users,
        }
        return render(request,'temp/schedule_send_sms.html',context=data)
    
@login_required(login_url='/')  
def send_emailView(request):
    if request.user.is_authenticated and request.user.is_admin:
        list_of_all_users = User.objects.filter(is_customer=True).order_by('-date_joined')
        data = {
            'list_of_all_users':list_of_all_users,
            'send_email_queue_status':Messagescontent.objects.filter(type="Email",status="0").count()

        }
        return render(request,'temp/send_email.html',context=data)
    
@login_required(login_url='/')  
def usersView(request):
    if request.user.is_authenticated and request.user.is_admin:
       # student pagination method
        list_of_all_users = User.objects.filter(is_customer=True).order_by('-date_joined')
        student_paginator = Paginator(list_of_all_users,8)
        page_number = request.GET.get('page')
        page_obj = student_paginator.get_page(page_number)
        data = {
            'list_of_all_users':list_of_all_users,
            'page_obj':page_obj
        }
        return render(request,'temp/users.html',context=data)
    
    
@login_required(login_url='/')  
def import_leadsView(request):
    if request.user.is_authenticated and request.user.is_admin:
        list_of_all_users = User.objects.filter(is_customer=True).order_by('-date_joined')
        data = {
            'list_of_all_users':list_of_all_users,
        }
        return render(request,'temp/lead_import.html',context=data)
    
    
    
@login_required(login_url='/')  
def update_userView(request,user_id):
    if request.user.is_authenticated and request.user.is_admin:
        list_of_all_users = User.objects.filter(is_customer=True).order_by('-date_joined')
        single_user_instance=User.objects.get(id=user_id)
        data = {
            'list_of_all_users':list_of_all_users,
            'single_user_instance':single_user_instance
        }
        return render(request,'temp/update.html',context=data)
    
    
@transaction.atomic
@login_required(login_url='/')  
def update_usersView(request,user_id):
    if request.user.is_authenticated and request.user.is_admin and request.method == "POST":
        first_name =request.POST['first_name']
        last_name =request.POST['last_name']
        cellphone =request.POST['cellphone']
        email =request.POST['email']
        sacode="+27"
        if len(cellphone) > 10:
            messages.info(request,"Enter cellphone without country code")
            return redirect(f'/update_user/{user_id}')
        elif len(cellphone) < 10:
            messages.info(request,"Incompleted cell phone number")
            return redirect(f'/update_user/{user_id}')
        
        formatedcellphone = str((cellphone)[1:10])
        formtaedcellphonenumber = str(f"{sacode}{formatedcellphone}")   
        customer_instance =User.objects.get(id=user_id)
        customer_instance.first_name=first_name
        customer_instance.last_name=last_name
        customer_instance.phone=cellphone
        customer_instance.email=email
        if customer_instance:
            customer_instance.save()
            messages.info(request,f"Informations for {first_name} has been successfully updated")
            return redirect(f'/update_user/{user_id}')
    return redirect('/dashboard')

@login_required(login_url='/')  
def messageView(request):
    if request.user.is_authenticated and request.user.is_admin:
        list_of_all_users = User.objects.filter(is_customer=True).order_by('-date_joined')
        data = {
            'list_of_all_users':list_of_all_users,
        }
        return render(request,'temp/message.html',context=data)


@login_required(login_url='/')  
def birthdayView(request):
    if request.user.is_authenticated and request.user.is_admin:
        list_of_all_users = User.objects.filter(is_customer=True).order_by('-date_joined')
        data = {
            'list_of_all_users':list_of_all_users,
        }
        return render(request,'temp/birthday.html',context=data)
    
@login_required(login_url='/')  
def reminderView(request):
    if request.user.is_authenticated and request.user.is_admin:
        list_of_all_users = User.objects.filter(is_customer=True).order_by('-date_joined')
        data = {
            'list_of_all_users':list_of_all_users,
        }
        return render(request,'temp/reminder.html',context=data)
    
@transaction.atomic
@login_required(login_url='/')  
def delete_userView(request,user_id):
    if request.user.is_authenticated and request.user.is_admin:
        list_of_all_users = User.objects.filter(is_customer=True).order_by('-date_joined')
        delete_single_user=User.objects.filter(id=user_id).delete()
        if delete_single_user:
            messages.info(request,"User Account is Deleted Successfully")
        return render(request,'temp/message.html',{'list_of_all_users':list_of_all_users})
    else:
        return redirect(f'/user_info/{user_id}')
    
    
@transaction.atomic
@login_required(login_url='/')  
def search_userView(request):
    if request.user.is_authenticated and request.user.is_admin and request.method == "POST":
        cellphone=request.POST['cellphone']
        if not User.objects.filter(phone=cellphone).exists():
            messages.info(request,"No Data Found for that user")
            return redirect('/message')
        if User.objects.get(phone=cellphone):
            user_id = User.objects.filter(phone=cellphone).values_list('id', flat=True).first() 
            return redirect(f'/user_info/{user_id}')
    else:
        return redirect(f'/dashboard')
    

@transaction.atomic
@login_required(login_url='/') 
def import_leadView(request):
    if request.user.is_authenticated and request.user.is_admin and request.method == 'POST' and request.FILES['excel_lead']:
        excel_file = request.FILES['excel_lead']
        try:
            # Assuming the file is an Excel file
            df = pd.read_excel(excel_file)
            # Iterate through each row and create a YourModel object
            for index, row in df.iterrows():
                import_user_instance=User(
                    username=row['phone'],
                    password=row['phone'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    phone=row['phone'],
                    email=row['email'],
                    # Map the fields to your model fields accordingly
                )
                import_user_instance.save()
            messages.info(request,"Data has been successfully Imported")
            return redirect('/message')
        except Exception as e:
            error_message = str("Either the data you are trying to import already exists in the database, or you have not followed the columns and rows data properly.")
            messages.info(request,error_message)
            return redirect('/message')
    return render(request, 'import_form.html')



@login_required(login_url='/')  
def sms_logView(request):
    if request.user.is_authenticated and request.user.is_admin:
        list_of_all_users = User.objects.filter(is_customer=True).order_by('-date_joined')
        sms_log = Smslog.objects.filter().order_by('-created_at')
        sms_log_count = Smslog.objects.all().count()
        student_paginator = Paginator(sms_log,20)
        page_number = request.GET.get('page')
        page_obj = student_paginator.get_page(page_number)
        data = {
            'list_of_all_users':list_of_all_users,
            'page_obj':page_obj,
            'sms_log_count':sms_log_count
        }
        return render(request,'temp/sms_log.html',context=data)
    
@login_required(login_url='/')  
def email_logView(request):
    if request.user.is_authenticated and request.user.is_admin:
        list_of_all_users = User.objects.filter(is_customer=True).order_by('-date_joined')
        email_log = EmailLog.objects.filter().order_by('-created_at')
        email_log_count = EmailLog.objects.all().count()
        student_paginator = Paginator(email_log,20)
        page_number = request.GET.get('page')
        page_obj = student_paginator.get_page(page_number)
        data = {
            'list_of_all_users':list_of_all_users,
            'page_obj':page_obj,
            'email_log_count':email_log_count
            
        }
        return render(request,'temp/email_log.html',context=data)
    
    
@login_required(login_url='/')  
def my_logView(request):
    if request.user.is_authenticated and request.user.is_admin:
        list_of_all_users = User.objects.filter(is_customer=True).order_by('-date_joined')
       # student pagination method
        my_log = Messagescontent.objects.filter().order_by('-created_at')
        student_paginator = Paginator(my_log,15)
        page_number = request.GET.get('page')
        page_obj = student_paginator.get_page(page_number)
        data = {
            'list_of_all_users':list_of_all_users,
            'page_obj':page_obj,
            
        }
        return render(request,'temp/my_log.html',context=data)

@login_required(login_url='/')  
def delete_logView(request,id):
    if request.user.is_authenticated and request.user.is_admin:
        message_log_instance =Messagescontent.objects.get(id=id)
        Messagescontent.objects.filter(id=id).delete()
        EmailLog.objects.filter(messagecontent=message_log_instance).delete()
        messages.info(request,"Sent log deleted successfully")
        return redirect('/my_log')
    
@login_required(login_url='/')  
def my_log_completedView(request,id):
    if request.user.is_authenticated and request.user.is_admin:
        Messagescontent.objects.filter(id=id).update(status=1)
        return redirect('/my_log')
    
    
@login_required(login_url='/')  
def my_log_unmarkView(request,id):
    if request.user.is_authenticated and request.user.is_admin:
        Messagescontent.objects.filter(id=id).update(status=0)
        return redirect('/my_log')
    
api_key ='872d27df7562262acdeab75013e79b95'
api_secret ='a2b6bc70877ac1e8880d2694256cae4c'
    
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


@login_required(login_url='/')  
def template_galeryView(request):
    if request.user.is_authenticated and request.user.is_admin:
        list_of_all_users = User.objects.filter(is_customer=True).order_by('-date_joined')
        sms_log = Smslog.objects.filter()
        student_paginator = Paginator(sms_log,20)
        page_number = request.GET.get('page')
        page_obj = student_paginator.get_page(page_number)
        data = {
            'list_of_all_users':list_of_all_users,
            'page_obj':page_obj
        }
        return render(request,'temp/templates.html',context=data)

@login_required(login_url='/')  
def template1View(request):
    if request.user.is_authenticated and request.user.is_admin:
        return render(request,'templates/templates1.html')
    
@login_required(login_url='/')  
def template2View(request):
    if request.user.is_authenticated and request.user.is_admin:
        return render(request,'templates/templates2.html')
    
@login_required(login_url='/')  
def template3View(request):
    if request.user.is_authenticated and request.user.is_admin:
        return render(request,'templates/templates3.html')
    
@login_required(login_url='/')  
def template4View(request):
    if request.user.is_authenticated and request.user.is_admin:
        return render(request,'templates/templates4.html')
    
@login_required(login_url='/')  
def update_template_1(request,id):
    if request.user.is_authenticated and request.user.is_admin:
        template_instance =Template1.objects.get(id=id)
        list_of_all_users = User.objects.filter(is_customer=True).order_by('-date_joined')
        data = {
            'template_instance':template_instance,
            'list_of_all_users':list_of_all_users
        }
        return render(request,'temp/update_template1.html',context=data)
    
@login_required(login_url='/')  
def update_template_2(request,id):
    if request.user.is_authenticated and request.user.is_admin:
        template_instance =Template2.objects.get(id=id)
        list_of_all_users = User.objects.filter(is_customer=True).order_by('-date_joined')
        data = {
            'template_instance':template_instance,
            'list_of_all_users':list_of_all_users
        }
        return render(request,'temp/update_template2.html',context=data)

@login_required(login_url='/')  
def update_template_3(request,id):
    if request.user.is_authenticated and request.user.is_admin:
        template_instance =Template3.objects.get(id=id)
        list_of_all_users = User.objects.filter(is_customer=True).order_by('-date_joined')
        data = {
            'template_instance':template_instance,
            'list_of_all_users':list_of_all_users
        }
        return render(request,'temp/update_template3.html',context=data)
    
@login_required(login_url='/')  
def update_template_4(request,id):
    if request.user.is_authenticated and request.user.is_admin:
        template_instance =Template4.objects.get(id=id)
        list_of_all_users = User.objects.filter(is_customer=True).order_by('-date_joined')
        data = {
            'template_instance':template_instance,
            'list_of_all_users':list_of_all_users
        }
        return render(request,'temp/update_template4.html',context=data)
    
@login_required(login_url='/')  
def customise_template_2View(request):
    if request.user.is_authenticated and request.user.is_admin:
        list_of_all_users = User.objects.filter(is_customer=True).order_by('-date_joined')
        data = {
            'list_of_all_users':list_of_all_users
        }
        return render(request,'temp/customise_template2.html',context=data)
    
    
@login_required(login_url='/')  
def customise_template_3View(request):
    if request.user.is_authenticated and request.user.is_admin:
        list_of_all_users = User.objects.filter(is_customer=True).order_by('-date_joined')
        data = {
            'list_of_all_users':list_of_all_users
        }
        return render(request,'temp/customise_template3.html',context=data)
    
@login_required(login_url='/')  
def customise_template_4View(request):
    if request.user.is_authenticated and request.user.is_admin:
        list_of_all_users = User.objects.filter(is_customer=True).order_by('-date_joined')
        data = {
            'list_of_all_users':list_of_all_users
        }
        return render(request,'temp/customise_template4.html',context=data)
    
@login_required(login_url='/')  
def customise_template_1View(request):
    if request.user.is_authenticated and request.user.is_admin:
        list_of_all_users = User.objects.filter(is_customer=True).order_by('-date_joined')
        data = {
            'list_of_all_users':list_of_all_users
        }
        return render(request,'temp/customise_template1.html',context=data)
    
@login_required(login_url='/')  
def preview_draft_template(request,id):
    if request.user.is_authenticated and request.user.is_admin:
        template_instance =Template1.objects.get(id=id)
        template1_product_list = Product.objects.filter(template1=template_instance)
        data = {
            'template_instance':template_instance,
            'template1_product_list':template1_product_list
        }
        return render(request,'temp/templates1_design.html',context=data)
    
@login_required(login_url='/')  
def preview_draft_template3(request,id):
    if request.user.is_authenticated and request.user.is_admin:
        template_instance =Template3.objects.get(id=id)
        data = {
            'template_instance':template_instance,
        }
        return render(request,'temp/templates3_design.html',context=data)
    
    
@login_required(login_url='/')  
def preview_draft_template4(request,id):
    if request.user.is_authenticated and request.user.is_admin:
        template_instance =Template4.objects.get(id=id)
        admin_instance = request.user.username
        company_instance =User.objects.get(username=admin_instance)
        data = {
            'template_instance':template_instance,
            'company_instance':company_instance,
            'template4_paragraph':paragraphtemplate4.objects.filter(template4=template_instance)

        }
        return render(request,'temp/templates4_design.html',context=data)
    
@login_required(login_url='/')  
def preview_draft_template2(request,id):
    if request.user.is_authenticated and request.user.is_admin:
        template_instance =Template2.objects.get(id=id)
        data = {
            'template_instance':template_instance,
            'template2_list':Listtemplate2.objects.filter(template2=template_instance)

        }
        return render(request,'temp/templates2_design.html',context=data)
    
@login_required(login_url='/')  
def template2_draftView(request):
    if request.user.is_authenticated and request.user.is_admin:
        list_of_all_users = User.objects.filter(is_customer=True).order_by('-date_joined')
        template = Template2.objects.all()
        data = {
            'list_of_all_users':list_of_all_users,
            'template':template
        }
        return render(request,'temp/template2_draft.html',context=data)
    
@login_required(login_url='/')  
def template3_draftView(request):
    if request.user.is_authenticated and request.user.is_admin:
        list_of_all_users = User.objects.filter(is_customer=True).order_by('-date_joined')
        template = Template3.objects.all()
        data = {
            'list_of_all_users':list_of_all_users,
            'template':template
        }
        return render(request,'temp/template3_draft.html',context=data)
    
@login_required(login_url='/')  
def template4_draftView(request):
    if request.user.is_authenticated and request.user.is_admin:
        list_of_all_users = User.objects.filter(is_customer=True).order_by('-date_joined')
        template = Template4.objects.all()
        data = {
            'list_of_all_users':list_of_all_users,
            'template':template
        }
        return render(request,'temp/template4_draft.html',context=data)
    
@login_required(login_url='/')  
def template1_draftView(request):
    if request.user.is_authenticated and request.user.is_admin:
        list_of_all_users = User.objects.filter(is_customer=True).order_by('-date_joined')
        template = Template1.objects.all()
        data = {
            'list_of_all_users':list_of_all_users,
            'template':template
        }
        return render(request,'temp/template1_draft.html',context=data)
    
@login_required(login_url='/')  
def update_template_1_(request,id):
    if request.user.is_authenticated and request.user.is_admin and request.method=="POST":
        template_instance = Template1.objects.get(id=id)
        template_instance.templatename = request.POST['templatename']
        template_instance.banner = request.FILES['banner']
        template_instance.title = request.POST['title']
        template_instance.abouttext = request.POST['abouttext']
        template_instance.moreinfo = request.POST['moreinfo']
        template_instance.websites = request.POST['website']
        template_instance.productitle = request.POST['producttext']
        template_instance.save()
        messages.info(request,"Template has been Updated successfully")
        return redirect(f'/update_template_1/{id}')
    else:
        return redirect(f'/update_template_1/{id}')
    
    
@login_required(login_url='/')  
def update_template_2_(request,id):
    if request.user.is_authenticated and request.user.is_admin and request.method=="POST":
        template_instance = Template2.objects.get(id=id)
        template_instance.templatename = request.POST['templatename']
        template_instance.banner = request.FILES['banner']
        template_instance.title = request.POST['title']
        template_instance.deartext = request.POST['greetingtext']
        template_instance.abouttext = request.POST['dectext']
        template_instance.exploretext = request.POST['listext']
        template_instance.dontmisstext = request.POST['dontmisstext']
        template_instance.link = request.POST['link']
        template_instance.moreinfo = request.POST['moreinfo']
        template_instance.save()
        messages.info(request,"Template has been Updated successfully")
        return redirect(f'/update_template_2/{id}')
    else:
        return redirect(f'/update_template_2/{id}')
    
    
@login_required(login_url='/')  
def update_template_3_(request,id):
    if request.user.is_authenticated and request.user.is_admin and request.method=="POST":
        template_instance = Template3.objects.get(id=id)
        template_instance.templatename = request.POST['templatename']
        template_instance.banner = request.FILES['banner']
        template_instance.title = request.POST['title']
        template_instance.deartext = request.POST['greetingtext']
        template_instance.abouttext = request.POST['dectext']
        template_instance.eventheading = request.POST['eventdetail']
        template_instance.date = request.POST['date']
        template_instance.time = request.POST['time']
        template_instance.dontmiss = request.POST['dontmissout']
        template_instance.location = request.POST['location']
        template_instance.link = request.POST['link']
        template_instance.moreinfo = request.POST['moreinfo']
        template_instance.save()
        messages.info(request,"Template has been Updated successfully")
        return redirect(f'/update_template_3/{id}')
    else:
        return redirect(f'/update_template_3/{id}')
    
@login_required(login_url='/')  
def update_template_4_(request,id):
    if request.user.is_authenticated and request.user.is_admin and request.method=="POST":
        template_instance = Template4.objects.get(id=id)
        template_instance.templatename = request.POST['templatename']
        template_instance.banner = request.FILES['banner']
        template_instance.title = request.POST['title']
        template_instance.deartext = request.POST['greetingtext']
        template_instance.email = request.POST['email']
        template_instance.phone = request.POST['telephone']
        template_instance.address = request.POST['address']
        template_instance.whatsapp = request.POST['whatsapp']
        template_instance.save()
        messages.info(request,"Template has been Updated successfully")
        return redirect(f'/update_template_4/{id}')
    else:
        return redirect(f'/update_template_4/{id}')
    
@login_required(login_url='/')  
def create_template1View(request):
    if request.user.is_authenticated and request.user.is_admin and request.method=="POST":
        templatename = request.POST['templatename']
        banner = request.FILES['banner']
        title = request.POST['title']
        abouttext = request.POST['abouttext']
        moreinfo = request.POST['moreinfo']
        websites = request.POST['website']
        productitle = request.POST['producttext']
        
        if Template1.objects.filter(templatename=templatename).exists():
            messages.info(request,"Template name has been used already")
            return redirect('/customise_template_1')
        if not Template1.objects.filter(templatename=templatename).exists():
            create_new_template =Template1(templatename=templatename,banner=banner,title=title,abouttext=abouttext,moreinfo=moreinfo,websites=websites,productitle=productitle)
            create_new_template.save()
            return redirect('/template1_draft')
    else:
        return redirect('/customise_template_1')
    
    
@login_required(login_url='/')  
def create_template2View(request):
    if request.user.is_authenticated and request.user.is_admin and request.method=="POST":
        templatename = request.POST['templatename']
        banner = request.FILES['banner']
        title = request.POST['title']
        greetingtext = request.POST['greetingtext']
        dectext = request.POST['dectext']
        listext = request.POST['listext']
        dontmisstext = request.POST['dontmisstext']
        link = request.POST['link']
        moreinfo = request.POST['moreinfo']
        
        if Template2.objects.filter(templatename=templatename).exists():
            messages.info(request,"Template name has been used already")
            return redirect('/customise_template_2')
        if not Template2.objects.filter(templatename=templatename).exists():
            create_new_template =Template2(templatename=templatename,banner=banner,title=title,deartext=greetingtext,abouttext=dectext,exploretext=listext,dontmisstext=dontmisstext,link=link,moreinfo=moreinfo)
            create_new_template.save()
            return redirect('/template2_draft')
    else:
        return redirect('/customise_template_2')
    
    
@login_required(login_url='/')  
def create_template3View(request):
    if request.user.is_authenticated and request.user.is_admin and request.method=="POST":
        templatename = request.POST['templatename']
        banner = request.FILES['banner']
        title = request.POST['title']
        greetingtext = request.POST['greetingtext']
        dectext = request.POST['dectext']
        eventdetail = request.POST['eventdetail']
        date = request.POST['date']
        time = request.POST['time']
        location = request.POST['location']
        dontmissout = request.POST['dontmissout']
        link = request.POST['link']
        moreinfo = request.POST['moreinfo']
        
        if Template3.objects.filter(templatename=templatename).exists():
            messages.info(request,"Template name has been used already")
            return redirect('/customise_template_3')
        if not Template3.objects.filter(templatename=templatename).exists():
            create_new_template =Template3(templatename=templatename,banner=banner,title=title,deartext=greetingtext,abouttext=dectext,eventheading=eventdetail,date=date,time=time,dontmiss=dontmissout,location=location,link=link,moreinfo=moreinfo)
            create_new_template.save()
            return redirect('/template2_draft')
    else:
        return redirect('/customise_template_3')
    
    
@login_required(login_url='/')  
def create_template4View(request):
    if request.user.is_authenticated and request.user.is_admin and request.method=="POST":
        templatename = request.POST['templatename']
        banner = request.FILES['banner']
        title = request.POST['title']
        deartext = request.POST['greetingtext']
        email = request.POST['email']
        phone = request.POST['telephone']
        address = request.POST['address']
        whatsapp = request.POST['whatsapp']
        
        if Template4.objects.filter(templatename=templatename).exists():
            messages.info(request,"Template name has been used already")
            return redirect('/customise_template_4')
        if not Template4.objects.filter(templatename=templatename).exists():
            create_new_template =Template4(templatename=templatename,banner=banner,title=title,deartext=deartext,email=email,phone=phone,address=address,whatsapp=whatsapp)
            create_new_template.save()
            return redirect('/template4_draft')
    else:
        return redirect('/customise_template_4')
    
    
@login_required(login_url='/')  
def delete_template1View(request,id):
    if request.user.is_authenticated and request.user.is_admin:
        delete_template =Template1.objects.get(id=id).delete()
        if delete_template:
            return redirect('/template1_draft')
    else:
        return redirect('/template1_draft')
    
@login_required(login_url='/')  
def delete_template2View(request,id):
    if request.user.is_authenticated and request.user.is_admin:
        delete_template =Template2.objects.get(id=id).delete()
        if delete_template:
            return redirect('/template2_draft')
    else:
        return redirect('/template2_draft')
    
@login_required(login_url='/')  
def delete_template3View(request,id):
    if request.user.is_authenticated and request.user.is_admin:
        delete_template =Template3.objects.get(id=id).delete()
        if delete_template:
            return redirect('/template3_draft')
    else:
        return redirect('/template3_draft')
    
@login_required(login_url='/')  
def delete_template4View(request,id):
    if request.user.is_authenticated and request.user.is_admin:
        delete_template =Template4.objects.get(id=id).delete()
        if delete_template:
            return redirect('/template4_draft')
    else:
        return redirect('/template4_draft')
    
@login_required(login_url='/')  
def add_list_template2(request,id):
    if request.user.is_authenticated and request.user.is_admin:
        list_of_all_users = User.objects.filter(is_customer=True).order_by('-date_joined')
        template_2_instance = Template2.objects.get(id=id)
        data = {
            'list_of_all_users':list_of_all_users,
            'id':id,
            'list':Listtemplate2.objects.filter(template2=template_2_instance)
        }
        return render(request,'temp/customise_add_list.html',context=data)
    
    
@login_required(login_url='/')  
def paragraph_template4(request,id):
    if request.user.is_authenticated and request.user.is_admin:
        list_of_all_users = User.objects.filter(is_customer=True).order_by('-date_joined')
        template_4_instance = Template4.objects.get(id=id)
        data = {
            'list_of_all_users':list_of_all_users,
            'id':id,
            'paragraph':paragraphtemplate4.objects.filter(template4=template_4_instance)
        }
        return render(request,'temp/customise_add_paragraph.html',context=data)
    
@login_required(login_url='/')  
def add_product_template1View(request,id):
    if request.user.is_authenticated and request.user.is_admin:
        list_of_all_users = User.objects.filter(is_customer=True).order_by('-date_joined')
        template_1_instance = Template1.objects.get(id=id)
        data = {
            'list_of_all_users':list_of_all_users,
            'id':id,
            'product_list':Product.objects.filter(template1=template_1_instance)
        }
        return render(request,'temp/customise_add_products.html',context=data)
    
    
    
@login_required(login_url='/')  
def save_product_template1View(request,id):
    if request.user.is_authenticated and request.user.is_admin and request.method=="POST":
        image = request.FILES['image']
        productname = request.POST['productname']
        description = request.POST['description']
        symbol = request.POST['symbol']
        price = request.POST['price']
        website = request.POST['website']
        template_1_instance = Template1.objects.get(id=id)
        add_product_to_template_1=Product(template1=template_1_instance,productimage=image,productname=productname,productdesc=description,symbol=symbol,price=price,link=website)
        add_product_to_template_1.save()
        return redirect(f'/product_template1/{id}')
    else:
        return redirect(f'/product_template1/{id}')

@login_required(login_url='/')  
def save_list_template2View(request,id):
    if request.user.is_authenticated and request.user.is_admin and request.method=="POST":
        list = request.POST['list']
        template_2_instance = Template2.objects.get(id=id)
        add_list_to_template_2=Listtemplate2(template2=template_2_instance,list=list)
        add_list_to_template_2.save()
        return redirect(f'/list_template2/{id}')
    else:
        return redirect(f'/list_template2/{id}')


@login_required(login_url='/')  
def save_paragraph_template4(request,id):
    if request.user.is_authenticated and request.user.is_admin and request.method=="POST":
        parapgrah = request.POST['parapgrah']
        template_4_instance = Template4.objects.get(id=id)
        save_paragraph_template4=paragraphtemplate4(template4=template_4_instance,parapgrah=parapgrah)
        save_paragraph_template4.save()
        return redirect(f'/paragraph_template4/{id}')
    else:
        return redirect(f'/paragraph_template4/{id}')

@login_required(login_url='/')  
def delete_template1_productView(request,id):
    if request.user.is_authenticated and request.user.is_admin:
        delete_template1_single_product =Product.objects.get(id=id).delete()
        if delete_template1_single_product:
            return redirect('/product_template1')
    else:
        return redirect('/template1_draft')
    
    
@login_required(login_url='/')  
def delete_template2_listView(request,id):
    if request.user.is_authenticated and request.user.is_admin:
        delete_template1_single_list =Listtemplate2.objects.get(id=id).delete()
        if delete_template1_single_list:
            return redirect('/template2_draft')
    else:
        return redirect('/template2_draft')
    
@login_required(login_url='/')  
def delete_template4_paragraphView(request,id):
    if request.user.is_authenticated and request.user.is_admin:
        delete_template4_single_line_paragraph =paragraphtemplate4.objects.get(id=id).delete()
        if delete_template4_single_line_paragraph:
            return redirect('/template4_draft')
    else:
        return redirect('/template4_draft')