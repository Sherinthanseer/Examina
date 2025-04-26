from django.shortcuts import render,redirect,get_object_or_404
from common.models import *
from django.contrib.auth.models import User,Group
from django.contrib import messages
from .models import *
from teacher.models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.models import Sum  
from student.models import *
from django.http import HttpResponseRedirect


def loginp(request):    
    if request.user.is_authenticated:
        if request.user.groups.filter(name='principal').exists():
            return redirect('phome') 
    
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None and user.groups.filter(name="principal").exists():
            data=principal.objects.filter(user_id=user.id)
            login(request,user)
            request.session["pid"]=data[0].id
            messages.info(request,'login successfull')
            return redirect('phome')
    return render(request,'principal/loginp.html')

def principalregister(request):
    # m=qualification.objects.all()
    available_institutes = institute.objects.filter(principal__isnull=True, status="approved")  
    if 'id' in request.session:
        return redirect('view')
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        quali = request.POST['qualification']
        experience = request.POST['experience']
        username = request.POST['username']
        email = request.POST['principal_email']
        password = request.POST['password']
        inst = request.POST['institution']
        photo = request.FILES['photo'] if "photo" in request.FILES else None
        if principal.objects.filter(institute_id=inst).exists():
            messages.error(request, "This institute is already assigned to another principal.")
            return redirect('principalregister')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
        else:
            user = User.objects.create_user(
                username=username, 
                email=email, 
                first_name=fname, 
                last_name=lname, 
                password=password
            )
            user.save()
            p = principal(
                user=user, 
                qualificationid_id=quali, 
                experience=experience, 
                photo=photo, 
                institute_id=inst
            )
            p.save()
            princi, create = Group.objects.get_or_create(name='principal')
            princi.user_set.add(user)
            return redirect('loginp')

    a = institute.objects.filter(status='approved')
    qu = qualificationP.objects.all()
    return render(request, 'principal/principalregister.html', {"ta": a, 'q': qu})


def phome(request):
    pid=request.user.id
    print(pid)
    return render(request,'principal/phome.html')
    
           
def viewteacher(request):
    pid=request.session["pid"]
    inst_id=principal.objects.filter(id=pid)
    tcr=teacher1.objects.filter(institute_id=inst_id[0].institute)
    return render(request,'principal/viewteacher.html',{"da":tcr})

def t_details(request):
    tid=request.GET['id']
    tcr=teacher1.objects.filter(id=tid)
    return render(request,'principal/t_details.html',{"da":tcr})

def deleteteacher(request,tid):
    teacher=teacher1.objects.get(id=tid)
    user=User.objects.get(id=teacher.user_id)
    user.delete()
    return redirect('t_details')





def forgot_password_principal(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = get_user_model().objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            reset_url = request.build_absolute_uri(
                reverse('reset_password_principal', kwargs={'uidb64': uid, 'token': token})
            )
            subject = 'Password Reset Request'
            message = render_to_string('principal/princi_reset_email.html', {
                'user': user,
                'reset_url': reset_url,
            })
            try:
                send_mail(subject, message, 'snehasatheesh176@gmail.com', [user.email])
                messages.success(request, 'Password reset link has been sent to your email.')
            except Exception as e:
                messages.error(request, f'Error sending email: {e}')
            return redirect('forgot_password_principal')
        else:
            messages.error(request, 'No account found with that email.')
    return render(request, 'principal/princi_forgot_password.html')


def reset_password_principal(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST['password']
            user.set_password(new_password)
            user.save()
            messages.success(request,'Password has been reset successfully. You can now log in with your new password.')
            return redirect('loginp')  
        return render(request, 'principal/princi_reset_password.html', {'uidb64': uidb64, 'token': token})
    else:
        messages.error(request, 'The link is invalid or has expired.')
        return redirect('forgot_password_principal')
    
def principal_view_grades_list(request):
    grades = (ExamResult.objects.values_list('exams__grade', 'exams__nameid__Name','').distinct().order_by('exams__grade'))    
    context = {
        'grades': grades
        }
    print(list(grades))  
    return render(request, 'principal/grades.html', context)


def principal_view_highest_mark_by_grade(request, grade,institute):
 students_aggregated = (
        ExamResult.objects.filter(exams__grade=grade,student__institute=institute)
        .select_related('student__user', 'student__institute')
        .values(
            'student__user__username', 
            'student__institute__name'
        )
        .annotate(annotated_total_marks=Sum('total_marks'))  # Rename annotation
        .order_by('-annotated_total_marks')
    )
 top_student = students_aggregated[0] if students_aggregated else None

 context = {
        'top_student': top_student,
        'students_aggregated': students_aggregated,
        'grade': grade,  # Pass grade for template use
    }    
 return render(request, 'principal/highest_student.html', context)

def principal_about(request):
    return render(request,'principal/about.html')

def principal_team(request):
    m=teacher1.objects.all()[:8]
    return render(request,'principal/team.html',{'teacher':m})

def update_principal(request):
    user=request.user
    y=get_object_or_404(principal,user=user)
    if request.method == 'POST':
        y.user.first_name=request.POST['first_name']
        y.user.last_name=request.POST['last_name']
        if 'photo' in request.FILES:
            y.photo=request.FILES["photo"]
        y.institute_id=request.POST['institute']
        y.experience=request.POST['experience']
        y.qualificationid_id=request.POST['qualification_name']
        y.save()
        y.user.save()
        messages.info(request,'updated succesfully')
        return redirect(phome)
    y=principal.objects.filter(user=user)
    a = institute.objects.filter(status='approved')
    qu = qualificationP.objects.all()
    
    return render(request,'principal/update_principal.html',{'y':y,'u':a,'d':qu})

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

def approve_exam(request,id):
     exams=get_object_or_404(exam,id=id)
     exams.status="Approved"
     exams.save()
     return redirect(viewteacher_exam)
def reject_exam(request,id):
     exams=get_object_or_404(exam,id=id)
     exams.status="Rejected"
     exams.save()
     return redirect(viewteacher_exam)
def approve_teacher(request,id):
     y=get_object_or_404(teacher1,id=id)
     y.status="approved"
     y.save()
     return redirect(viewteacher)
def deny_teacher(request,id):
     y=get_object_or_404(teacher1,id=id)
     y.status="denied" 
     y.save()
     return redirect(viewteacher)  
      
 
 