from django.db import models
from django.contrib.auth.models import User
from .models import *

class qualification1(models.Model):
    qualification_name=models.CharField(max_length=100)
    
    def __str__(self):
        return self.qualification_name

    
class teacher1(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    teaching_sub=models.CharField(max_length=100)
    gender=models.CharField(max_length=6)
    exp=models.CharField(max_length=10)
    grade=models.CharField(max_length=50)
    phone=models.CharField(max_length=12)
    tid=models.CharField(max_length=20) 
    institute=models.ForeignKey('common.institute', on_delete=models.CASCADE,default=1) 
    photo=models.ImageField(upload_to="teacher/",null=True,blank=True)
    qualificationid=models.ForeignKey(qualification1,on_delete=models.CASCADE)
    status=models.CharField(max_length=20,default="pending")

    
    def __str__(self):
        return self.user.username

class Exam_name(models.Model):
    Name=models.CharField(max_length=20)
    institute=models.ForeignKey('common.institute', on_delete=models.CASCADE,default=1) 
    def __str__(self):
        return self.Name

class exam(models.Model):
    nameid=models.ForeignKey(Exam_name,on_delete=models.CASCADE,null=True)
    code=models.CharField(max_length=100)
    start=models.TimeField()
    duration=models.IntegerField()
    marks=models.IntegerField()
    type=models.CharField(max_length=100)
    grade=models.CharField(max_length=100)
    date=models.DateField()
    discp=models.CharField(max_length=200)
    sub=models.CharField(max_length=200)
    teacher=models.ForeignKey(teacher1,on_delete=models.CASCADE)
    minimum=models.IntegerField()
    status=models.CharField(max_length=20,default="pending")
    number_of_questions=models.IntegerField(default=1)

        
    def __str__(self):
        return f"{self.sub}"
        
class MCQ(models.Model):
    exam=models.ForeignKey(exam,on_delete=models.CASCADE)
    marks=models.PositiveIntegerField()
    question=models.CharField(max_length=600)
    option1=models.CharField(max_length=200)
    option2=models.CharField(max_length=200)
    option3=models.CharField(max_length=200)
    option4=models.CharField(max_length=200)
    cat=(('option1','option1'),('option2','option2'),('option3','option3'),('option4','option4'))
    answer=models.CharField(max_length=200,choices=cat)
    
    def __str__(self):
        return f"{self.question} - {self.exam.nameid}"
    
    
class Descriptive(models.Model):
     exam=models.ForeignKey(exam,on_delete=models.CASCADE)
     marks=models.PositiveIntegerField()
     question=models.CharField(max_length=600)
     answer=models.TextField()

     def __str__(self):
        return f"{self.question} - {self.exam.nameid}"

        
class ExamAttempt(models.Model):
    student = models.ForeignKey('student.student', on_delete=models.CASCADE)
    exams = models.ForeignKey(exam, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.student.user.first_name} - {self.exams.nameid}"
    
class Grade(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Resource(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='resources/', blank=True, null=True)
    youtube_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title