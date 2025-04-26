from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User,Group
from django.contrib import messages
from .models import *
from common.models import *
from student.models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum  
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.urls import reverse
from collections import defaultdict



def teacherlogin(request): 
    if request.user.is_authenticated:
     if request.user.groups.filter(name='teacher').exists():
        return redirect('teacherHome') 
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None and user.groups.filter(name="teacher").exists():
            data=teacher1.objects.filter(user_id=user.id,status="approved")
            if data:
                login(request,user)
                messages.info(request,'login successfull')
                return redirect('teacherHome')
            else:
                messages.info(request,'account is not approved')
                return render(request,'teacher/teacherlogin.html')
    return render(request,'teacher/teacherlogin.html')


def teacherHome(request):
    tid=request.user.id
    print(tid)
    return render(request,'teacher/teacherHome.html')

def registerteacher(request):
    if request.method == 'POST' :
        fname=request.POST['fname']
        lname=request.POST['lname']
        quali=request.POST['qualification']
        experience=request.POST['experience']
        username=request.POST['username']
        email=request.POST['email']
        teaching_sub=request.POST['teaching_sub']
        password=request.POST['password']
        gender=request.POST['gender']
        grade=request.POST['grade']
        phone=request.POST['phone']
        tid=request.POST['tid']
        inst=request.POST['institution']
        photo=request.FILES['photo'] if "photo" in request.FILES else None
        
        if User.objects.filter(username=username).exists():
                messages.error(request,'username exist')
        elif User.objects.filter(email=email).exists():
                messages.error(request,'email exist')
        user=User.objects.create_user(username=username,email=email,first_name=fname,last_name=lname,password=password)
        user.save()
        t=teacher1(user=user,qualificationid_id=quali,exp=experience,photo=photo,teaching_sub=teaching_sub,gender=gender,phone=phone,grade=grade,tid=tid,institute_id=inst)
        t.save()
        teach,create=Group.objects.get_or_create(name='teacher')
        teach.user_set.add(user)
        return redirect('teacherlogin')
    else:
        c=qualification1.objects.all()
        a = institute.objects.filter(status='approved')
        return render(request,"teacher/registerteacher.html",{"ta": a,"c":c})




def questionpaper(request):
     m=exam.objects.filter(status="Approved")
     return render(request,'teacher/questionpaper.html',{'da':m})
 

def mcq_exam(request):
    if request.method == "POST":
        exam_id = request.POST.get("examid")
        marks = request.POST.get("marks")
        question = request.POST.get("question")
        option1 = request.POST.get("option1")
        option2 = request.POST.get("option2")
        option3 = request.POST.get("option3")
        option4 = request.POST.get("option4")
        answer = request.POST.get("answer")
        selected_exam = exam.objects.get(id=exam_id)   

        current_question_count = MCQ.objects.filter(exam=selected_exam).count()

        if current_question_count >= selected_exam.number_of_questions:
            messages.error(request, "Question limit reached for this exam.")
            return redirect(questionpaper) 

        else:
            q=MCQ.objects.create(
                exam=selected_exam,
                marks=marks,
                question=question,
                option1=option1,
                option2=option2,
                option3=option3,
                option4=option4,
                answer=answer
            )
            q.save()
            messages.info(request,'mcq exam creation successful')
            return redirect(questionpaper)
    data=request.GET['data']
    exams = Exam_name.objects.all()
    Exam_count=exam.objects.filter(id=data)
    for e in Exam_count:
        e.mcq_count=MCQ.objects.filter(exam=e).count()
    return render(request,'teacher/mcq.html',{'data':data,'exam':exams,'mcq_count':Exam_count})

def descriptive_exam(request):
    if request.method == 'POST' :
      exam_id=request.POST['examid']
      marks=request.POST['marks']
      question=request.POST['question']
      answer=request.POST['Answer']
      selected_exam = exam.objects.get(id=exam_id)
        
      current_question_count = Descriptive.objects.filter(exam=selected_exam).count()

      if current_question_count >= selected_exam.number_of_questions:
            messages.error(request, "Question limit reached for this exam.")
            return redirect(questionpaper) 
      else:
            d=Descriptive.objects.create(
                    exam=selected_exam,
                    marks=marks,
                    question=question,      
                    answer=answer
                )
            d.save()
            messages.info(request,'Descriptive exam creation successful')
            return redirect(questionpaper)
    data=request.GET['data']
    Exam_count=exam.objects.filter(id=data)
    
    for e in Exam_count:
        e.descriptive_count=Descriptive.objects.filter(exam=e).count()
    return render(request,'teacher/descriptive.html',{'data':data,'descriptive_count':Exam_count})

@login_required
def view_exams(request):
    tid=request.user.id
    teacher_instance = get_object_or_404(teacher1, user=request.user)
    exams=exam.objects.filter(teacher=teacher_instance)
    return render(request,'teacher/view_exam.html',{'exams':exams})

    
@login_required
def evaluate_exam(request, exam_id):
    exam_instance = get_object_or_404(exam, id=exam_id, teacher__user=request.user)
    mcq_answers = StudentAnswer.objects.filter(mcq__exam=exam_instance)
    descriptive_answers = DescriptiveAnswer.objects.filter(descriptive__exam=exam_instance)
    if request.method == "POST":
        stid = request.POST.get('studentid')
        print(f"Student ID: {stid}")
        for answer in descriptive_answers:
            marks_field = f"marks_{answer.id}"  
            if marks_field in request.POST:
                try:
                    answer.marks_awarded = int(request.POST[marks_field])
                    answer.save()  
                except ValueError:
                    print(f"Invalid marks for descriptive answer {answer.id}")

        for answer in mcq_answers:
            marks_field = f"mcq_marks_{answer.id}"  
            if marks_field in request.POST:
                try:
                    answer.marks_awarded = int(request.POST[marks_field])
                    answer.save() 
                except ValueError:
                    print(f"Invalid marks for MCQ answer {answer.id}")

        mcq_students = mcq_answers.values_list('student_id', flat=True).distinct()
        descriptive_students = descriptive_answers.values_list('student_id', flat=True).distinct()

        students = set(mcq_students).union(set(descriptive_students))
       

        for student_id in students:
            student_mcq_marks = (
                mcq_answers.filter(student_id=student_id)
                .aggregate(total=Sum('marks_awarded'))['total'] or 0
            )
            print(f"mcq{student_mcq_marks}")
            student_descriptive_marks = (
                descriptive_answers.filter(student_id=student_id)
                .aggregate(total=Sum('marks_awarded'))['total'] or 0
            )
            total_marks = student_mcq_marks + student_descriptive_marks
            pass_status = total_marks >= exam_instance.minimum

            result, created = ExamResult.objects.get_or_create(
                student_id=student_id,
                exams=exam_instance,
                defaults={
                    'total_marks': total_marks,
                    'pass_status': pass_status,
                }
            )
            if not created:
                result.total_marks = total_marks
                result.pass_status = pass_status
                result.save()

    return render(request, 'teacher/evaluate_exam.html', {
        'exam': exam_instance,
        'mcq_answers': mcq_answers,
        'descriptive_answers': descriptive_answers,
    })
  
def exam_results(request, exam_id):
    exam_instance = get_object_or_404(exam, id=exam_id)
    return render(request, 'teacher/exam_results.html', {'exam': exam_instance})


@login_required
def upload_resourses(request):    
    if request.method == 'POST':
        subject = Subject.objects.get(id=request.POST['subject'])  # Get the subject
        title = request.POST['title']
        description = request.POST.get('description', '')
        file = request.FILES.get('file')
        youtube_link = request.POST.get('youtube_link', '')

        Resource.objects.create(
            teacher=request.user,
            subject=subject,
            title=title,
            description=description,
            file=file,
            youtube_link=youtube_link
        )
        return redirect(teacherHome)  
    grades = Grade.objects.all()
    subjects = Subject.objects.all()
    return render(request, 'teacher/upload_resource.html', {'grades': grades, 'subjects': subjects})


def forgot_password_teacher(request):
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
            message = render_to_string('teacher/teacher_reset_email.html', {
                'user': user,
                'reset_url': reset_url,
            })
                        
            try:
                send_mail(subject, message, 'snehasatheesh176@gmail.com', [user.email])
                messages.success(request, 'Password reset link has been sent to your email.')
            except Exception as e:
                messages.error(request, f'Error sending email: {e}')
            return redirect('forgot_password_teacher')
        else:
            messages.error(request, 'No account found with that email.')
                
    return render(request, 'teacher/teacher_forgot_password.html')


def reset_password_teacher(request, uidb64, token):
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
            return redirect('teacherlogin')  
        return render(request, 'teacher/teacher_reset_password.html', {'uidb64': uidb64, 'token': token})
    else:
        messages.error(request, 'The link is invalid or has expired.')
        return redirect('forgot_password_teacher')
    

def teacher_view_grades_list(request):
    grades = (ExamResult.objects.values_list('exams__grade', 'exams__nameid__Name').distinct().order_by('exams__grade'))    
    context = {
        'grades': grades
        }
    print(list(grades))  
    return render(request, 'teacher/grades.html', context)


def teacher_view_highest_mark_by_grade(request, grade,institute_id):
 students_aggregated = (
        ExamResult.objects.filter(exams__grade=grade,student_institute=institute_id)
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
 return render(request, 'teacher/highest_student.html', context)

def updateteacher(request):
    tid=request.user.id
    y=get_object_or_404(teacher1,user_id=tid)
    if request.method == 'POST':
        y.user.first_name=request.POST['first_name']
        y.user.last_name=request.POST['last_name']
        if 'photo' in request.FILES:
            y.photo=request.FILES["photo"]
        y.teaching_sub=request.POST['teaching_sub']
        y.grade=request.POST['grade']
        y.gender=request.POST['gender']
        y.exp=request.POST['exp']
        y.qualification=request.POST['qualification_name']
        y.email=request.POST['email']
        y.phone=request.POST['phone']
        y.save()
        y.user.save()
        messages.info(request,'updated succesfully')
        return redirect(teacherHome)
    y=teacher1.objects.filter(user_id=tid)
    return render(request,'teacher/editteacher.html',{'y':y})

def viewstudent(request):
    tid=request.user.id
    tea=teacher1.objects.filter(user_id=tid)
    std=student.objects.filter(institute_id=tea[0].institute)
    return render(request,'teacher/viewstudent.html',{"da":std})

def s_details(request):
    tid=request.GET['id']
    std=student.objects.filter(id=tid)
    return render(request,'teacher/s_details.html',{"da":std})

def approve_student(request,id):
     y=get_object_or_404(student,id=id)
     y.status="approved"
     y.save()
     return redirect(viewstudent)
def deny_student(request,id):
     y=get_object_or_404(student,id=id)
     y.status="denied" 
     y.save()
     return redirect(viewstudent)  
def examcreation(request):
    if 'id' in request.session:
        return redirect('view')
    if request.method == 'POST' :
        tcid=teacher1.objects.get(user_id=request.user.id).id
        name=request.POST['name']
        code=request.POST['code']
        start=request.POST['start'] 
        duration=request.POST['duration']
        date=request.POST['date']
        type=request.POST['type']
        marks=request.POST['marks']
        grade=request.POST['grade']
        discp=request.POST['discp']
        subject=request.POST['subject']
        min=request.POST['mini']
        number_question=request.POST['number_question']
        print(number_question)
        e=exam.objects.create(code=code,start=start,duration=duration,date=date,type=type,marks=marks,grade=grade,discp=discp,teacher_id=tcid,sub=subject,minimum=min,nameid_id=name,number_of_questions=number_question)
        e.save()

        students = User.objects.filter(student__grade=grade)  # Assuming students have a 'grade' field
        for student in students:
            Notification.objects.create(
                student=student,
                exam=e,
                message=f"New exam '{e.sub}' has been added for Grade {grade}."
            )
        messages.info(request,'exam creation successful')
    exam_name=Exam_name.objects.all()
    return render(request,'teacher/examcreation.html',{'name':exam_name})


def reschedule(request,id):
    if 'id' in request.session:
        return redirect('view')
    if request.method == 'POST' :
        tcid=teacher1.objects.get(user_id=request.user.id).id
        name=request.POST['name']
        code=request.POST['code']
        start=request.POST['start'] 
        duration=request.POST['duration']
        date=request.POST['date']
        type=request.POST['type']
        marks=request.POST['marks']
        grade=request.POST['grade']
        discp=request.POST['discp']
        subject=request.POST['subject']
        min=request.POST['mini']
        e=exam.objects.create(code=code,start=start,duration=duration,date=date,type=type,marks=marks,grade=grade,discp=discp,teacher_id=tcid,sub=subject,minimum=min,nameid_id=name)
        e.save()
        messages.info(request,'exam creation successful')
    exam_name=exam.objects.filter(id=id)
    return render(request,'teacher/reschedule.html',{'name':exam_name})
