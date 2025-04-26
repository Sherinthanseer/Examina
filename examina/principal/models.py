from django.db import models
from django.contrib.auth.models import User


class qualificationP(models.Model):
    qualification_name=models.CharField(max_length=100)
    
    def __str__(self):
        return self.qualification_name

class principal(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    qualificationid=models.ForeignKey(qualificationP,on_delete=models.CASCADE,null=True)
    experience=models.CharField(max_length=5)
    photo=models.ImageField(upload_to="principal/",null=True,blank=True)
    institute=models.OneToOneField('common.institute', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
    
    

    