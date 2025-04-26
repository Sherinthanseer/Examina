from django.urls import path
from teacher import views 
urlpatterns = [
    path('teacherlogin/',views.teacherlogin,name="teacherlogin"),
    path('teacherHome/',views.teacherHome,name="teacherHome"),
    path('examcreation/',views.examcreation,name="examcreation"),
    path('questionpaper/',views.questionpaper,name="questionpaper"),
    path('mcq_exam',views.mcq_exam,name="mcq_exam"),
    path('descriptive_exam/',views.descriptive_exam,name="descriptive_exam"),
    path('view_exam',views.view_exams,name='view_exam'),
    path('evaluate_exam/<int:exam_id>/', views.evaluate_exam, name='evaluate_exam'),
    path('exam-results/<int:exam_id>/', views.exam_results, name='exam_results'),
    path('upload_resourses',views.upload_resourses,name="upload_resourses"),
    path('forgot-password', views.forgot_password_teacher, name='forgot_password_teacher'),
    path('reset-password/<uidb64>/<token>/', views.reset_password_teacher, name='reset_password_teacher'),
    path('teacher_view_highest_mark_by_grade/<int:grade>/', views.teacher_view_highest_mark_by_grade, name='teacher_view_highest_mark_by_grade'),
    path('teacher_view_grades_list/', views.teacher_view_grades_list, name='teacher_view_grades_list'),
    path('registerteacher/',views.registerteacher,name="registerteacher"),
    path('updateteacher/',views.updateteacher,name="updateteacher"),
    path('approve_student/<int:id>',views.approve_student,name="approve_student"),
    path('deny_student/<int:id>',views.deny_student,name="deny_student"),
    path('viewstudent/',views.viewstudent,name="viewstudent"),
    path('s_details',views.s_details,name="s_details"),
    path('reschedule/<int:id>',views.reschedule,name="reschedule"),

    ]

