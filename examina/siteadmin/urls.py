from django.urls import path
from siteadmin import views 
urlpatterns = [
    path('loginadmin/',views.loginadmin,name="loginadmin"),
    path('adminhome/',views.adminhome,name="adminhome"),
    path('viewinstitute/',views.viewinstitute,name="viewinstitute"),
    path('status<int:id>/',views.status,name="status"),
    path('deny<int:id>/',views.deny,name="deny"),
    path('admin_about',views.admin_about,name='admin_about'),
    path('admin_teacher',views.admin_teacher,name='admin_teacher')
]