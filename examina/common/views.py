from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import *
from django.conf import settings
from django.core import mail
from django.contrib import messages
from .models import Contact
from django.conf import settings
from django.core import mail
from django.contrib import messages
from .models import Contact
from teacher.models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import HelpDeskTicket


def index(request):
    if 'id' in request.session:
        return redirect('view')
    return render(request,'common/index.html')


def logoutadmin(request):
        logout(request)
        return redirect('index')


def instituteregister(request):
    if 'id' in request.session:
        return redirect('view')
    if request.method == 'POST' :
        name=request.POST['name']
        code=request.POST['code']
        address=request.POST['address']
        phone=request.POST['phone']
        email=request.POST['email']
        inst=institute(name=name,code=code,address=address,phone=phone,email=email)
        inst.save()
        return redirect('index')
    return render(request,"common/instituteregister.html")


def about(request):
    m=teacher1.objects.all()[:4]
    if request.user.is_authenticated:
        if request.user.groups.filter(name="teacher").exists():
            return render(request, 'teacher/about.html', {'teacher':m})
        elif request.user.groups.filter(name="principal").exists():
            return render(request, 'principal/about.html',{'teacher':m})
        elif request.user.groups.filter(name="student").exists():
            return render(request, 'student/about.html',{'teacher':m})
        else:
            return render(request, 'about.html')  # Default for users without a group
    else:
        return render(request, 'about.html') # Redirect to login if user is not authenticated

def contact(request):
    return render(request,'contact.html')


def team(request):
    m=teacher1.objects.all()[:8]
    if request.user.is_authenticated:
        if request.user.groups.filter(name="teacher").exists():
            return render(request, 'teacher/team.html', {'teacher':m})
        elif request.user.groups.filter(name="principal").exists():
            return render(request, 'principal/team.html',{'teacher':m})
        elif request.user.groups.filter(name="student").exists():
            return render(request, 'student/team.html',{'teacher':m})
        else:
            return render(request, 'team.html')  # Default for users without a group
    else:
        return render(request, 'team.html')   # Redirect to login if user is not authenticated


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        Contact.objects.create(
            name=name, 
            email=email, 
            desc=message, 
            subject=subject
        )
        from_email = settings.EMAIL_HOST_USER

        email_message = mail.EmailMessage(
            subject=f'Email is from {name}',
            body=(
                f"Hello,\n\n"
                f"You have received a new inquiry from your website's contact form. Below are the details:\n\n"
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Subject: {subject}\n"
                f"Message:\n{message}\n\n"
                f"Best regards,\nYour Website Team"
            ),
            from_email=from_email,
            to=['nakulsatheesh364@gmail.com']  
        )
        email_client = mail.EmailMessage(
            subject=f'Thank you for reaching out, {name}!',
            body=(
                f"Dear {name},\n\n"
                f"Thank you for contacting us. We have received your query:\n\n"
                f"Subject: {subject}\n\n"
                f"{message}\n\n"
                f"We'll get back to you shortly.\n\n"
                f"Best regards,\nTeam"
            ),
            from_email=from_email,
            to=[email]  
        )
        try:
            email_message.send()  
            email_client.send()  
            messages.success(request, 'Your message has been sent successfully! We will get back to you soon.')
        except Exception as e:
            messages.error(request, f'An error occurred while sending the email: {e}')
    return redirect('contact')


def create_ticket(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')        
        if not name or not email or not subject or not message:
            return HttpResponse("All fields are required.", status=400)
        ticket = HelpDeskTicket(
            name=name,
            email=email,
            subject=subject,
            message=message,)
        ticket.save()
        messages.success(request, 'Your message has been sent successfully! We will get back to you soon.')
    return render(request, 'create_ticket.html')


def ticket_list(request):
    tickets = HelpDeskTicket.objects.all().order_by('-created_at')
    return render(request, 'siteadmin/ticket_list.html', {'tickets': tickets})


def reply_ticket(request, ticket_id):
    ticket = get_object_or_404(HelpDeskTicket, id=ticket_id)

    if request.method == 'POST':
        reply_message = request.POST.get('reply_message')
        
        if not reply_message:
            return HttpResponse("Reply message cannot be empty.", status=400)
        
        send_mail(
            subject=f"Reply to Help Desk Query: {ticket.subject}",
            message=f"Query from: {ticket.name} ({ticket.email})\n\nQuery:\n{ticket.message}\n\nReply:\n{reply_message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[ticket.email],  
            fail_silently=False,
        )
        ticket.replied = True  
        ticket.save()
        return redirect('ticket_list')    
    return render(request, 'siteadmin/reply_ticket.html', {'ticket': ticket})


def handel_logout(request):
    if request.user.is_authenticated:
       logout(request)
    return redirect('index')
 
def viewteacher_exam(request):
    exams =exam.objects.all().order_by('-date')  # Fetch all exams

    name = get_object_or_404(Exam_name, id=exams[0].nameid_id)

    selected_exam = None

    # If a specific exam is requested
    exam_id = request.GET.get('exam_id')
    if exam_id:
        selected_exam = get_object_or_404(exam, id=exam_id)
    
    context = {
        'exams': exams,
        'selected_exam': selected_exam,
        'name':name
    }
    return render(request, 'principal/view_exam.html', context)      
