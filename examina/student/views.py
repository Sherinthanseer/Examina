from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.contrib.auth.models import User,Group
from .models import *
from principal.models import *
from common.models import *
from teacher.models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import localtime,now
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.utils.timezone import now
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import HttpResponse
from siteadmin.models import *
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.models import Sum  
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from xhtml2pdf import pisa
from io import BytesIO



def studentlogin(request): 
    if request.user.is_authenticated:
     if request.user.groups.filter(name='student').exists():
        return redirect('studenthome')     
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None and user.groups.filter(name="student").exists():
            data=student.objects.filter(user_id=user.id,status="approved")
            if data:
                login(request,user)
                messages.info(request,'login successfull')
                return redirect('studenthome')
            else:
                messages.info(request,'account not approved')
                return render(request,'student/studentlogin.html')
    return render(request,'student/studentlogin.html')

def studenthome(request):
    notifications = Notification.objects.filter(student=request.user, is_read=False).order_by('-created_at')
    return render(request,'student/studenthome.html', {'notifications': notifications})

def mark_notification_as_read(request, notification_id):
    notification = Notification.objects.get(id=notification_id, student=request.user)
    notification.is_read = True
    notification.save()
    return redirect(studenthome)

def registerStudent(request):
    if 'id' in request.session:
        return redirect('view')
    if request.method == 'POST' :
        fname=request.POST['fname']
        lname=request.POST['lname']
        gender=request.POST['gender']
        email=request.POST['email']
        phone=request.POST['phone']
        section=request.POST['section']
        year=request.POST['year']
        grade=request.POST['grade']
        admission_no=request.POST['admission_no']
        reg_no=request.POST['reg_no']
        username=request.POST['username']
        password=request.POST['password']
        inst=request.POST['institution']
        address=request.POST['address']
        photo=request.FILES['photo'] if "photo" in request.FILES else None
        
        if User.objects.filter(username=username).exists():
                    messages.error(request,'username exist')
        elif User.objects.filter(email=email).exists():
                    messages.error(request,'email exist')
        user=User.objects.create_user(username=username,email=email,first_name=fname,last_name=lname,password=password)
        user.save()
        s=student(user=user,gender=gender,phone=phone,photo=photo,section=section,year=year,grade=grade,admission_no=admission_no,reg_no=reg_no,address=address,institute_id=inst)
        s.save()
        stud,create=Group.objects.get_or_create(name='student')
        stud.user_set.add(user)
        return redirect('studentlogin')   
    else:
        a = institute.objects.filter(status='approved') 
    return render(request,'student/registerStudent.html',{"ta": a})


@login_required
def student_exams(request):
    student1 = student.objects.get(user=request.user)
    grade = student1.grade
    exams = exam.objects.filter(grade=grade)
    
    attended_mcq_exam_ids = StudentAnswer.objects.filter(student=student1).values_list('mcq__exam', flat=True).distinct()
    attended_desc_exam_ids = DescriptiveAnswer.objects.filter(student=student1).values_list('descriptive__exam', flat=True).distinct()
    attended_exam_ids = set(attended_mcq_exam_ids).union(attended_desc_exam_ids)

    attended_exams = exams.filter(id__in=attended_exam_ids)
    not_attended_exams = exams.exclude(id__in=attended_exam_ids)

    current_datetime =localtime(now())
    current_date = current_datetime.date()
    current_time = current_datetime.time().replace(microsecond=0)
    print(f"Current Date: {current_date}, Current Time: {current_time}")
    for exam_obj in not_attended_exams:
            exam_start = exam_obj.start
            exam_date = exam_obj.date  # Ensure correct date is used
            exam_start_datetime = datetime.combine(exam_date, exam_start)  # Full datetime
            exam_end_datetime = exam_start_datetime + timedelta(minutes=exam_obj.duration)  # Add duration
            exam_end = exam_end_datetime.time()  #Extract time
            if current_date < exam_date or (current_date == exam_date and current_time < exam_start):
                exam_obj.status_text = "Exam not started"
                exam_obj.show_link = False  # Disable exam link
            elif current_date == exam_date and exam_start <= current_time < exam_end:
                exam_obj.status_text = "Take Exam"
                exam_obj.show_link = True  #Enable exam link
            else:
                exam_obj.status_text = "Exam ended"
                exam_obj.show_link = False  #Disable exam link

    context = {
            'attended_exams': attended_exams,
            'not_attended_exams': not_attended_exams,
            'current_datetime': current_datetime,
    }
    
    return render(request, 'student/student_exams.html', context)


def start_exam(exam_id):
    exams = exam.objects.get(id=exam_id)
    students = student.objects.all() 
    for i in students:
        Clock.objects.create(exams=exams,time_left=exams.duration * 60)        
             
def get_timer(request):
    exam_id = request.GET.get('examid') 
    if request.user.is_authenticated:
        try:
            clock = Clock.objects.get(students__user=request.user,exams=exam_id)
            time_elapsed = (now() - clock.time_start).total_seconds()  
            time_left_seconds = max(0, (clock.time_left * 3600) - time_elapsed)  
            return JsonResponse({"time_left": int(time_left_seconds)})  
        except Clock.DoesNotExist:
            return JsonResponse({"error": "Clock not found"}, status=404)
    else:
        return JsonResponse({"error": "User not authenticated"}, status=403)

@login_required
def student_exams_detail(request, exam_id):
    clock_obj=Clock.objects.first()
    get_time=clock_obj.time_left
    students = student.objects.get(user=request.user)
    student_grade = students.grade    
    selected_exam = exam.objects.get(id=exam_id)
    mcqs = MCQ.objects.filter(exam=selected_exam)
    attempt = ExamAttempt.objects.filter(student=students, exams=selected_exam, is_completed=False).first()        
    attended_mcqs = StudentAnswer.objects.filter(student=students).values_list('mcq_id', flat=True)
    attended_mcqs_set = set(attended_mcqs)
    mcqs_with_status = []
    for mcq in mcqs:
        mcqs_with_status.append({
            'mcq': mcq,
            'is_attended': mcq.id in attended_mcqs_set
        })
    context = {
        'mcqs_with_status': mcqs_with_status,
        'exam': selected_exam,
        'get_time':get_time
    }
    return render(request, 'student/student_exam_detail.html', context)


def get_count_ajax(request):
    count=Clock.objects.first()
    if count.time_left>0:
        count.time_left -=1
    count.save()
    return JsonResponse({'live_counter':count.time_left})


@login_required
def submit_mcq(request, exam_id):
    selected_exam = get_object_or_404(exam, id=exam_id)
    student1 = get_object_or_404(student, user=request.user)
    if request.method == "POST":
        answers = [] 
        for key, value in request.POST.items():
            if key.startswith("mcq_"):
                mcq_id = key.split("_")[1]
                selected_option = value
                selected_mcq = MCQ.objects.get(id=mcq_id)
                is_correct = (selected_option == selected_mcq.answer)
                
                answers.append(
                    StudentAnswer(student=student1, mcq=selected_mcq, selected_option=selected_option, is_correct=is_correct)
                )
        
        StudentAnswer.objects.bulk_create(answers)
        attempt, created = ExamAttempt.objects.get_or_create(
        student=student1,
        exams=selected_exam,
        defaults={'start_time': now()})
        attempt.is_completed = True
        attempt.end_time = now()
        attempt.save()
        messages.success(request, "Your answers have been submitted.")
        return redirect('student_exams')  
    return render(request, 'submit_mcq.html', {'exam': selected_exam})


@login_required
def student_exams_detail2(request, exam_id):
    students = student.objects.get(user=request.user)
    student_grade = students.grade
    selected_exam = exam.objects.get(id=exam_id)
    relevant_exams = exam.objects.filter(grade=student_grade)
    descriptives = Descriptive.objects.filter(exam=selected_exam)
    attended_descriptives = DescriptiveAnswer.objects.filter(student=students).values_list('descriptive_id', flat=True)
    attended_descriptives_set = set(attended_descriptives)
    descriptives_with_status = []
    for descriptive in descriptives:
        descriptives_with_status.append({
            'descriptive': descriptive,
            'is_attended': descriptive.id in attended_descriptives_set})
    context = {
        'descriptives_with_status': descriptives_with_status,'exam': selected_exam,}
    return render(request, 'student/student_exam_detail2.html', context)


@login_required
def submit_descriptive(request, exam_id):
    selected_exam = get_object_or_404(exam, id=exam_id)
    if request.method == "POST":
        student = request.user.student 
        answers = []
        for key, value in request.POST.items():
            if key.startswith("descriptive_"):
                try:
                    desc_id = int(key.split("_")[1]) 
                    answer_text = value.strip()  
                    if answer_text: 
                        descriptive = get_object_or_404(Descriptive, id=desc_id)
                        answers.append(DescriptiveAnswer(student=student,descriptive=descriptive,answer_text=answer_text))
                except (ValueError, Descriptive.DoesNotExist):
                    continue
        if answers:
            DescriptiveAnswer.objects.bulk_create(answers)
        attempt, created = ExamAttempt.objects.get_or_create(
        student=student,
        exams=selected_exam,
        defaults={'start_time': now()})
        attempt.is_completed = True
        attempt.end_time = now()
        attempt.save()
        return redirect('student_exams')  
    return redirect('student_exam_detail', exam_id=exam_id)


@login_required
def start_exam(request, exam_id):
    student = request.user.student
    selected_exam = exam.objects.get(id=exam_id)
    existing_attempt = ExamAttempt.objects.filter(student=student, exam=selected_exam, is_completed=False).first()
    if not existing_attempt:
        ExamAttempt.objects.create(student=student, exam=selected_exam, start_time=timezone.now())
    return redirect('exam_details', exam_id=exam_id)



@login_required
def student_view_result(request):
    result = ExamResult.objects.filter(student__user=request.user)
    if not result:
        return HttpResponse("No results found.", status=404)
    name = get_object_or_404(Exam_name, id=result[0].exams.nameid_id)
    students = get_object_or_404(student, user=request.user)
    institution = students.institute
    candidate_fail = result.filter(pass_status=0).exists()
    grand_total = sum([i.total_marks for i in result])
    
    context = {
        'institution': institution,
        'result': result,
        'student': students,
        'examname': name,
        'candidate_fail': candidate_fail,}
    
    if 'download' in request.GET:
        html_content = render_to_string('student/pdf_exam_result.html', context)

        buffer = BytesIO()
        pisa_status = pisa.CreatePDF(html_content, dest=buffer)
        buffer.seek(0)

        if pisa_status.err:
            return HttpResponse('An error occurred while generating the PDF', status=500)

        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="exam_result.pdf"'
        return response

    return render(request, 'student/my_examResult.html', context)


def class_room(request):
    students=get_object_or_404(student,user=request.user)
    grade=Grade.objects.get(name=students.grade)
    subjects = Subject.objects.filter(grade=grade.id)
    return render(request, 'student/subject_list.html', {'subjects': subjects})


def subject_detail(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)  
    resources = Resource.objects.filter(subject=subject)  
    return render(request, 'student/subject_detail.html', {
        'subject': subject,
        'resources': resources})

        
def log_activity(request):
    if request.method == "POST":
        print("hi")
        student_id = request.user.id 
        activity = request.POST.get("activity", "Unknown activity")
        timestamp = now()
        ActivityLog.objects.create(student_id=student_id, activity=activity, timestamp=timestamp)
        return JsonResponse({"status": "logged"})   
    return JsonResponse({"status": "error"})


def forgot_password_student(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = get_user_model().objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            reset_url = request.build_absolute_uri(
                reverse('reset_password_teacher', kwargs={'uidb64': uid, 'token': token})
            )
            subject = 'Password Reset Request'
            message = render_to_string('student/student_reset_email.html', {
                'user': user,
                'reset_url': reset_url,
            })
            try:
                send_mail(subject, message, 'snehasatheesh176@gmail.com', [user.email])
                messages.success(request, 'Password reset link has been sent to your email.')
            except Exception as e:
                messages.error(request, f'Error sending email: {e}')
            return redirect('forgot_password_student')
        else:
            messages.error(request, 'No account found with that email.')
    return render(request, 'student/student_forgot_password.html')


def reset_password_student(request, uidb64, token):
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
            return redirect('studentlogin')  
        return render(request, 'student/student_reset_password.html', {'uidb64': uidb64, 'token': token})
    else:
        messages.error(request, 'The link is invalid or has expired.')
        return redirect('forgot_password_student')
        
@login_required
def change_password_student(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        user = request.user
        if not check_password(old_password, user.password):
            messages.error(request, 'Old password is incorrect.')
        elif new_password1 != new_password2:
            messages.error(request, 'The new passwords do not match.')
        elif not new_password1:
            messages.error(request, 'The new password cannot be empty.')
        else:
            user.set_password(new_password1)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
    return render(request, 'student/student_change_password.html')





def student_teacher(request):
    m=teacher1.objects.all()[:8]
    return render(request,'student/team.html',{'teacher':m})


def grades_list(request):
    grades = (ExamResult.objects.values_list('exams__grade', 'exams__nameid__Name').distinct().order_by('exams__grade'))    
    context = {
        'grades': grades
        }
    print(list(grades))  
    return render(request, 'student/grades.html', context)


def highest_mark_by_grade(request, grade):
    students_aggregated = (
        ExamResult.objects.filter(exams__grade=grade)
        .select_related('student__user', 'student__teacherid__principalid__institute')
        .values(
            'student__user__username', 
            'student__teacherid__principalid__institute__name'
        )
        .annotate(annotated_total_marks=Sum('total_marks')) 
        .order_by('-annotated_total_marks')
    )
    top_student = students_aggregated[0] if students_aggregated else None

    context = {
        'top_student': top_student,
        'students_aggregated': students_aggregated,
        'grade': grade, 
    }
    return render(request, 'student/highest_student.html', context)

def updatestudent(request):
    sid=request.user.id
    y=get_object_or_404(student,user_id=sid)
    if request.method == 'POST':
        y.user.first_name=request.POST['fname']
        y.user.last_name=request.POST['lname']
        if 'photo' in request.FILES:
            y.photo=request.FILES["photo"]
        y.user.email=request.POST['email']
        y.gender=request.POST['gender']
        y.grade=request.POST['grade']
        y.dob=request.POST['date']
        y.phone=request.POST['phone']
        y.section=request.POST['section']
        y.reg_no=request.POST['reg_no']
        y.admission_no=request.POST['admission_no']
        y.year=request.POST['year']
        y.address=request.POST['address']
        y.institute_id=request.POST['institution']
        y.save()
        y.user.save()
        messages.info(request,'updated succesfully')
        return redirect(studenthome)
    institution=institute.objects.all()
    stu=student.objects.filter(user_id=sid)
    
    return render(request,'student/editstudent.html',{'y':stu,'insti':institution})


