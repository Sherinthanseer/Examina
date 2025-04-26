from django.urls import path
from student import views 
urlpatterns = [
    path('studentlogin/',views.studentlogin,name="studentlogin"),
    path('studenthome/',views.studenthome,name="studenthome"),
    path('student_exams/', views.student_exams, name='student_exams'),
    path('exam/<int:exam_id>/submit_mcq/', views.submit_mcq, name='submit_mcq'),  # Add exam_id here
    path('submit_descriptive/<int:exam_id>', views.submit_descriptive, name='submit_descriptive'),
    path('mcq_exam/<int:exam_id>/', views.student_exams_detail, name='student_exams_detail'),  # Detail for MCQs
    path('discriptive_exam/<int:exam_id>/', views.student_exams_detail2, name='student_exams_detail2'),  # Detail for Descriptive
    path('get_counter_live',views.get_count_ajax,name='get_ajax'),
    path('get_timer',views.get_timer,name='get_timer'),
    path('student_view_result',views.student_view_result,name="student_view_result"),
    path('class_room',views.class_room,name="class_room"),
    path('subject/<int:subject_id>/', views.subject_detail, name='subject_detail'),
    path('student_exams/log_activity/', views.log_activity, name="log_activity"),
    path('forgot-password', views.forgot_password_student, name='forgot_password_student'),
    path('reset-password/<uidb64>/<token>/', views.reset_password_student, name='reset_password_student'),
    path('change-password/', views.change_password_student, name='change_password_student'),
    path('student_team',views.student_teacher,name='student_team'),
    path('highest-mark/<int:grade>/', views.highest_mark_by_grade, name='highest_mark_by_grade'),
    path('grades/', views.grades_list, name='grades_list'),
    path('updatestudent',views.updatestudent,name='updatestudent'),
    path('registerStudent/',views.registerStudent,name="registerStudent"),
    path('mark_notification_as_read/<int:notification_id>/',views.mark_notification_as_read,name="mark_notification_as_read"),
    
    
   
    







]