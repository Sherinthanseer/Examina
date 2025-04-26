from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import localtime
import pytz
from django.conf import settings

class student(models.Model):
      user=models.OneToOneField(User,on_delete=models.CASCADE)
      photo=models.ImageField(upload_to="student/",null=True,blank=True)
      gender=models.CharField(max_length=6)
      dob=models.CharField(max_length=20)
      phone=models.CharField(max_length=12)
      reg_no=models.CharField(max_length=6)
      grade=models.CharField(max_length=20)
      admission_no=models.CharField(max_length=20)
      section=models.CharField(max_length=10)
      year=models.CharField(max_length=5)
      address=models.TextField()
      status=models.CharField(max_length=20,default="pending")
      institute=models.ForeignKey('common.institute', on_delete=models.CASCADE,default=1) 
      
      def __str__(self):
          return self.user.first_name

class StudentAnswer(models.Model):
    student = models.ForeignKey('student.student', on_delete=models.CASCADE)
    mcq = models.ForeignKey('teacher.MCQ', on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=10)
    is_correct = models.BooleanField(default=False)
    marks_awarded = models.PositiveIntegerField(default=0)  

    def __str__(self):
        return f"{self.student.user.username} - {self.mcq.question}"

class DescriptiveAnswer(models.Model):
    student = models.ForeignKey('student.student', on_delete=models.CASCADE)
    descriptive = models.ForeignKey('teacher.Descriptive', on_delete=models.CASCADE)
    answer_text = models.TextField()
    marks_awarded = models.PositiveIntegerField(default=0) 

    def __str__(self):
        return f"{self.student.user.username} - {self.descriptive.question}"


class Clock(models.Model):
    students = models.ForeignKey('student.student', on_delete=models.CASCADE)  
    exams = models.ForeignKey('teacher.exam', on_delete=models.CASCADE)  
    time_left=models.FloatField(default=1.0)
    time_start=models.DateTimeField()
    def save(self, *args, **kwargs):
        ist = pytz.timezone(settings.TIME_ZONE)  # Get Asia/Kolkata timezone
        self.time_start = localtime().astimezone(ist)  # Store local time
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.students.user.username} - {self.exams.nameid}"


class ExamResult(models.Model):
    student = models.ForeignKey('student.student', on_delete=models.CASCADE)
    exams = models.ForeignKey('teacher.exam', on_delete=models.CASCADE)
    total_marks = models.PositiveIntegerField(default=0)
    pass_status = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.student.user.username} - {self.exams.nameid}"
    
class Subscribe(models.Model):
    email=models.EmailField()
    name=models.CharField(max_length=30)
    
    def __str__(self):
        return f"{self.email} - {self.name}"
    
class Notification(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE) 
    exam = models.ForeignKey('teacher.exam', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Notification for {self.student.username} - {self.message}"
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    