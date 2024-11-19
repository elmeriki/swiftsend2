# tasks.py
from __future__ import absolute_import,unicode_literals
from celery import shared_task
from django.core.mail import send_mail
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
from mailjet_rest import Client
from django.http import HttpRequest
basic = HTTPBasicAuth(settings.API_KEY,settings.API_SECRET)


@shared_task
def schedule_bulk_sms_task(greetings,message,companu_instance_name):
    admin_instance=User.objects.get(username=companu_instance_name)
    unique_badge_id=random_id(length=9,character_set=string.digits)        
    save_email = Messagescontent(id=unique_badge_id,subject=greetings,message=message,sent=True,error_message="None",type="Ssms")
    save_email.save() 
    users = User.objects.filter(is_customer=True)
    for user in users:
        sacode="+27"
        formatedcellphone = str((user.phone)[1:10])
        formtaedcellphonenumber = str(f"{sacode}{formatedcellphone}")
        sendRequest = {
                "messages": [{"content":f"{greetings} {user.first_name}, \n{message}\n Regards {admin_instance.companyname}", 
                              "destination":formtaedcellphonenumber}]}
        try:
            sendResponse = requests.post("https://rest.smsportal.com/bulkmessages",auth=basic,json=sendRequest)
            if sendResponse.status_code == 200:
                # Save record in database for each email sent
                email_sent_instance=Messagescontent.objects.get(id=unique_badge_id)
                save_sms_log=Smslog(messagecontent=email_sent_instance,phone=user.phone,fname=user.first_name,lname=user.last_name,message=message,sent=True,error_message="None")
                save_sms_log.save()

        except Exception as e:
            # Handle exceptions
            email_sent_instance=Messagescontent.objects.get(id=unique_badge_id)
            save_sms_log=Smslog(messagecontent=email_sent_instance,phone=user.phone,fname=user.first_name,lname=user.last_name,message=message,sent=False,error_message="None")
            save_sms_log.save() 
