from django.db import models
from django.contrib.auth.models import AbstractUser
from swiftauth.models import *

class User(AbstractUser):
    is_admin = models.BooleanField(default=False,blank=True,null=True)
    is_worker = models.BooleanField(default=False,blank=True,null=True)
    is_customer = models.BooleanField(default=True,blank=True,null=True)
    is_activation=models.BooleanField(default=False,blank=True,null=True)
    companyname =  models.CharField(max_length=200,blank=True,null=True,default="None")
    address =  models.CharField(max_length=200,blank=True,null=True,default="None")
    reg =  models.CharField(max_length=200,blank=True,null=True,default="None")
    tel =  models.CharField(max_length=200,blank=True,null=True,default="None")
    whatsapp =  models.CharField(max_length=200,blank=True,null=True,default="None")
    tax =  models.CharField(max_length=200,blank=True,null=True,default="None")
    phone =  models.CharField(max_length=200,blank=True,null=True,default="None")
    city =  models.CharField(max_length=200,blank=True,null=True,default="None")
    address =  models.CharField(max_length=200,blank=True,null=True,default="None")
    logo =  models.ImageField(null=True, upload_to="company_logo/",)
    website = models.TextField(blank=True, null=True)
    birth_date = models.DateField(default='2080-01-10')
    def __str__(self):
        return self.username

    class Meta(AbstractUser.Meta):
       swappable = 'AUTH_USER_MODEL'

class Messagescontent(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField()
    sent=models.BooleanField(default=False)
    error_message = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=255,blank=True, null=True)
    status = models.CharField(max_length=255,blank=True,default="0", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.subject

class EmailLog(models.Model):
    messagecontent = models.ForeignKey(Messagescontent,null=True,blank=True,on_delete=models.CASCADE,related_name="message_content_instances")
    email = models.CharField(max_length=255,blank=True, null=True)
    fname = models.CharField(max_length=255,blank=True, null=True)
    lname = models.CharField(max_length=255,blank=True, null=True)
    subject = models.CharField(max_length=255,blank=True, null=True)
    message = models.TextField()
    sent = models.BooleanField(default=False)
    error_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

class Smslog(models.Model):
    messagecontent = models.ForeignKey(Messagescontent,null=True,blank=True,on_delete=models.CASCADE,related_name="customer_sms_log_Data")
    phone = models.CharField(max_length=255,blank=True, null=True)
    fname = models.CharField(max_length=255,blank=True, null=True)
    lname = models.CharField(max_length=255,blank=True, null=True)
    message = models.TextField()
    sent = models.BooleanField(default=False)
    error_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fname