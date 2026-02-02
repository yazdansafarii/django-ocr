from django.db import models

# Create your models here.

class Document(models.Model):
    title = models.CharField(max_length=200,blank=True)
    pdf_file = models.FileField(upload_to ='pdfs/')
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title or f"Document {self.id}"