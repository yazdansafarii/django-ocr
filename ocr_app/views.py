import os
import easyocr
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from pdf2image import convert_from_path
from .models import Document
from .forms import DocumentForm

class PDFOCRView(CreateView):
    model = Document
    form_class = DocumentForm
    template_name = 'ocr_app/upload.html'
    
    # بعد از اتمام کار به کجا برود؟ (ما در اینجا از get_success_url استفاده می‌کنیم)
    def get_success_url(self):
        return reverse_lazy('ocr_result', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        # اول فایل را ذخیره می‌کنیم تا مسیر فیزیکی آن مشخص شود
        response = super().form_valid(form)
        
        # دسترسی به شیء ایجاد شده
        instance = self.object
        pdf_path = instance.pdf_file.path
        
        # --- شروع عملیات پردازش ---
        # 1. تبدیل PDF به عکس
        # نکته: اگر ویندوز هستید: poppler_path=r'C:\path\to\poppler\bin'
        path_to_poppler = r'C:\poppler\Library\bin'
        images = convert_from_path(pdf_path, poppler_path=path_to_poppler)
        
        # 2. آماده‌سازی مدل OCR (فقط یک بار لود شود)
        reader = easyocr.Reader(['fa', 'en'], download_enabled=False)
        
        extracted_pages = []
        
        for i, image in enumerate(images):
            temp_path = f"temp_{instance.id}_{i}.jpg"
            image.save(temp_path, 'JPEG')
            
            # استخراج متن
            results = reader.readtext(temp_path, detail=0)
            extracted_pages.append(" ".join(results))
            
            # حذف فایل موقت
            if os.path.exists(temp_path):
                os.remove(temp_path)
        
        # 3. به‌روزرسانی مدل با متن استخراج شده
        instance.content = "\n\n--- Page Separation ---\n\n".join(extracted_pages)
        instance.save()
        
        return response
    
    
class OCRResultView(DetailView):
    model = Document
    template_name = 'ocr_app/result.html'
    context_object_name = 'doc'