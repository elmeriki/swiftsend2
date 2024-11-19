
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('swift/', admin.site.urls),
    path('', include('swiftauth.urls')),
    path('', include('customer.urls'))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    
handler404 ='swiftauth.views.pagenotfoundView'
handler500 = 'swiftauth.views.my_custom_error_view'
# handler403 = 'swiftauth.views.my_custom_permission_denied_view'
# handler400 = 'swiftauth.views.my_custom_bad_request_view'