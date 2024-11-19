from django.contrib import admin
from django.contrib.auth.models import User,auth
from swiftauth.models import *

admin.site.register(User)
admin.site.register(EmailLog)
admin.site.register(Messagescontent)
admin.site.register(Smslog)
