from django.urls import path
from principal import views 

urlpatterns = [
    path('loginp/',views.loginp,name="loginp"),
    path('principalregister/',views.principalregister,name="principalregister"),
    path('phome/',views.phome,name="phome"),
    path('viewteacher/',views.viewteacher,name="viewteacher"),
    path('t_details',views.t_details,name="t_details"),
    path('deleteteacher/<int:tid>',views.deleteteacher,name="deleteteacher"),
    path('forgot-password', views.forgot_password_principal, name='forgot_password_principal'),
    path('reset-password/<uidb64>/<token>/', views.reset_password_principal, name='reset_password_principal'),
    path('principal_view_highest_mark_by_grade/<int:grade>/', views.principal_view_highest_mark_by_grade, name='principal_view_highest_mark_by_grade'),
    path('principal_view_grades_list/', views.principal_view_grades_list, name='principal_view_grades_list'),
    path('principal_about',views.principal_about,name='principal_about'),
    path('principal_team',views.principal_team,name='principal_team'),
    path('update_principal/', views.update_principal, name='update_principal'),
    path('viewteacher_exam/',views.viewteacher_exam,name="viewteacher_exam"),
    path('approve_exam/<int:id>',views.approve_exam,name="approve_exam"),
    path('reject_exam/<int:id>',views.reject_exam,name="reject_exam"),
    path('approve_teacher/<int:id>',views.approve_teacher,name="approve_teacher"),
    path('deny_teacher/<int:id>',views.deny_teacher,name="deny_teacher"),
]