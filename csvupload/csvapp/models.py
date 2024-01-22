from django.db import models

# Create your models here.
# models.py
from django.db import models

class UploadedFile(models.Model):
    filename = models.FileField(upload_to='uploads/%Y/%m/%d/')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.filename)

