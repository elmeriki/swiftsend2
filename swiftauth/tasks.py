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

api_key ='872d27df7562262acdeab75013e79b95'
api_secret ='a2b6bc70877ac1e8880d2694256cae4c'

@shared_task
def send_bulk_emails_task(subject, message,introtext,greetings,companu_instance_name):
    admin_instance=User.objects.get(username=companu_instance_name)
    unique_badge_id=random_id(length=9,character_set=string.digits)        
    save_email = Messagescontent(id=unique_badge_id,subject=subject,message=message,sent=True,error_message="None",type="Email")
    save_email.save() 
    users = User.objects.filter(is_customer=True)
    for user in users:
        try:
            mailjet = Client(auth=(api_key, api_secret), version='v3.1')
            data = {
            'Messages': [
                        {
                        "From": {
                        "Email": "no_reply@bolderphamallc.com",
                        "Name": admin_instance.companyname
                        },
                        "To": [
                                {
                                    "Email":user.email,
                                    "Name":user.first_name
                                }
                    ],
                "Subject": subject,
                                # "TextPart": "Greetings from Mailjet!",
                "HTMLPart":
                f"""
                <p><a href='{{admin_instance.website}}'><img src="{{admin_instance.logo.url}}" height='60px'></a> <br><br> <strong>{greetings} {user.first_name} </strong> <br><br> 
                {introtext}.<br>
                <br>
                {message}.<br>
                <br>
                
                <br>Best Regards<br> 
                <strong>{admin_instance.companyname}</strong>
                <br>Email:{admin_instance.email}
                <br>Head Office:{admin_instance.address}
                <br>Com Reg:{admin_instance.reg} | Tax No:{admin_instance.tax}
                <br>Whatsapp:{admin_instance.whatsapp} | Landline:{admin_instance.phone} | Mobile:{admin_instance.phone}
                <br>Website:{admin_instance.website}
                <hr>
                <strong>Copytighy © 2024 {admin_instance.companyname} All Right Reserved</strong>
                </p>"""}]}
            mailjet.send.create(data=data)
            # Save record in database for each email sent
            email_sent_instance=Messagescontent.objects.get(id=unique_badge_id)
            save_email_log=EmailLog(messagecontent=email_sent_instance,subject=subject,email=user.email,fname=user.first_name,lname=user.last_name,message=message,sent=True,error_message="None")
            save_email_log.save()
        except Exception as e:
            # Handle exceptions
            email_sent_instance=Messagescontent.objects.get(id=unique_badge_id)
            save_email_log=EmailLog(messagecontent=email_sent_instance,subject=subject,email=user.email,fname=user.first_name,lname=user.last_name,message=message,sent=False,error_message=str(e))
            save_email_log.save()      


