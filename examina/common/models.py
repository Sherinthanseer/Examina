from django.db import models

# Create your models here.
class institute(models.Model):
    name=models.CharField(max_length=40)
    code=models.CharField(max_length=40)
    email=models.EmailField()
    address=models.TextField()
    status=models.CharField(max_length=12,default="pending")
    phone=models.CharField(max_length=12,default="null")
    
    def __str__(self):
        return self.name
    
class Contact(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    desc=models.TextField()
    subject=models.CharField(max_length=100)
    

class HelpDeskTicket(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    replied = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.subject} - {self.name}"
