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
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

api_key ='872d27df7562262acdeab75013e79b95'
api_secret ='a2b6bc70877ac1e8880d2694256cae4c'


@shared_task
def send_bulk_template4_emails_task(id,company_username):
    admin_instance=User.objects.get(username=company_username)
    template_instance=Template4.objects.get(id=id)
    unique_badge_id=random_id(length=9,character_set=string.digits)        
    save_email = Messagescontent(id=unique_badge_id,subject=template_instance.templatename,message=template_instance.templatename,sent=True,error_message="None",type="Email")
    save_email.save() 
    users = User.objects.filter(is_customer=True)
    for user in users:
        try:
            email_data = {
            'template_instance':template_instance,
            'admin_instance':admin_instance,
            'template4_paragraph':paragraphtemplate4.objects.filter(template4=template_instance)
            }
            html_content =render_to_string('temp/templates4_design.html', context=email_data)
            mailjet = Client(auth=(api_key,api_secret), version='v3.1')
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
            "Subject":template_instance.templatename,
            # "TextPart": "Greetings from Mailjet!",
            "HTMLPart":html_content}]}
            mailjet.send.create(data=data)
            # Save record in database for each email sent
            email_sent_instance=Messagescontent.objects.get(id=unique_badge_id)
            save_email_log=EmailLog(messagecontent=email_sent_instance,subject=template_instance.templatename,email=user.email,fname=user.first_name,lname=user.last_name,message=template_instance.templatename,sent=True,error_message="None")
            save_email_log.save()
        except Exception as e:
            # Handle exceptions
            email_sent_instance=Messagescontent.objects.get(id=unique_badge_id)
            save_email_log=EmailLog(messagecontent=email_sent_instance,subject=template_instance.templatename,email=user.email,fname=user.first_name,lname=user.last_name,message=template_instance.templatename,sent=False,error_message=str(e))
            save_email_log.save()      


