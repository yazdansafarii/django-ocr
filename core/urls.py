from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ocr_app.urls')), # وصل کردن اپ به پروژه
] 

# این خط برای این است که جنگو بتواند فایل‌های PDF آپلود شده را بخواند
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)