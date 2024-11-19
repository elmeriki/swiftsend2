from django.db import models
from django.contrib.auth.models import AbstractUser
from swiftauth.models import *



class Template1(models.Model):
    templatename = models.CharField(max_length=255,blank=True, null=True)
    banner =  models.ImageField(null=True, upload_to="template1/",)
    title = models.CharField(max_length=255,blank=True, null=True)
    abouttext = models.TextField(blank=True, null=True)
    moreinfo = models.TextField(blank=True, null=True)
    websites = models.CharField(max_length=255,blank=True, null=True)
    productitle = models.TextField(blank=True, null=True)
    status =models.BooleanField(blank=True,null=True,default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.templatename
    
class Product(models.Model):
    template1 = models.ForeignKey(Template1,null=True,blank=True,on_delete=models.CASCADE,related_name="template1_product")
    productimage =  models.ImageField(null=True, upload_to="template1_product/",)
    productname = models.CharField(max_length=255,blank=True, null=True)
    productdesc = models.TextField(blank=True, null=True)
    symbol = models.CharField(max_length=255,blank=True, null=True)
    price=models.DecimalField(max_digits=11,decimal_places=2,default=0,blank=True,null=True)
    link = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.productname
    
    
class Template2(models.Model):
    templatename = models.CharField(max_length=255,blank=True, null=True)
    banner =  models.ImageField(null=True, upload_to="template2/",)
    title = models.CharField(max_length=255,blank=True, null=True)
    deartext = models.TextField(blank=True, null=True)
    abouttext = models.TextField(blank=True, null=True)
    exploretext = models.TextField(blank=True, null=True)
    dontmisstext = models.CharField(max_length=255,blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    moreinfo = models.TextField(blank=True, null=True)
    status =models.BooleanField(blank=True,null=True,default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.templatename
    
class Listtemplate2(models.Model):
    template2 = models.ForeignKey(Template2,null=True,blank=True,on_delete=models.CASCADE,related_name="template2_list")
    list = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.template1.templatename
    
    
class Template3(models.Model):
    templatename = models.CharField(max_length=255,blank=True, null=True)
    banner =  models.ImageField(null=True, upload_to="template3/",)
    title = models.CharField(max_length=255,blank=True, null=True)
    deartext = models.TextField(blank=True, null=True)
    abouttext = models.TextField(blank=True, null=True)
    eventheading = models.TextField(blank=True, null=True)
    date = models.CharField(max_length=255,blank=True, null=True)
    time = models.CharField(max_length=255,blank=True, null=True)
    location = models.CharField(max_length=255,blank=True, null=True)
    dontmiss = models.TextField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    moreinfo = models.TextField(blank=True, null=True)
    status =models.BooleanField(blank=True,null=True,default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    
class Template4(models.Model):
    templatename = models.CharField(max_length=255,blank=True, null=True)
    banner =  models.ImageField(null=True, upload_to="template5/",)
    title = models.CharField(max_length=255,blank=True, null=True)
    deartext = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    whatsapp = models.TextField(blank=True, null=True)
    status =models.BooleanField(blank=True,null=True,default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.templatename
    
class Paragraphtemplate4(models.Model):
    template4 = models.ForeignKey(Template4,null=True,blank=True,on_delete=models.CASCADE,related_name="template4_paragraph_te")
    parapgrah = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.template4.templatename