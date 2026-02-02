from django.urls import path
from .views import PDFOCRView, OCRResultView # دقت کنید که نام‌ها با کلاس‌های شما یکی باشد

urlpatterns = [
    path('', PDFOCRView.as_view(), name='ocr_upload'),
    path('result/<int:pk>/', OCRResultView.as_view(), name='ocr_result'),
]