from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from common.models import *
from teacher.models import *


def loginadmin(request):
    if request.user.is_authenticated and request.user.is_superuser:    
        return redirect('adminhome')  
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None and user.is_superuser:
            login(request,user)
            messages.info(request,'login successfull')
            return redirect('adminhome')
    return render(request,'siteadmin/loginadmin.html')

def adminhome(request):
     return render(request,'siteadmin/admin.html')
 
def viewinstitute(request):
    data=institute.objects.all()
    return render(request,'siteadmin/viewinstitute.html',{"da":data})

def status(request,id):
    m=institute.objects.filter(id=id).update(status='approved')
    return redirect('viewinstitute')

def deny(request,id):
    n=institute.objects.filter(id=id).update(status='denied')
    return redirect('viewinstitute')
     
    
def admin_about(request):
    return render(request,'siteadmin/about.html')


def admin_teacher(request):
    m=teacher1.objects.all()[:8]
    return render(request,'siteadmin/team.html',{'teacher':m})