from django.urls import path
from common import views 
urlpatterns = [
      path('',views.index,name="index"),
      path('logoutadmin/',views.logoutadmin,name="logoutadmin"),
      path('instituteregister/',views.instituteregister,name="instituteregister"),
      path('about',views.about,name='about'),
      path('contact',views.contact,name='contact'),
      path('team',views.team,name='team'),
      path('contacts',views.contacts,name='contacts'),
      path('helpdesk/create/', views.create_ticket, name='create_ticket'),
      path('helpdesk/', views.ticket_list, name='ticket_list'),
      path('helpdesk/reply/<int:ticket_id>/', views.reply_ticket, name='reply_ticket'),
      path('handel_logout',views.handel_logout,name='handel_logout')
      
      

]
