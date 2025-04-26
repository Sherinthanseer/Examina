from django.contrib import admin
from django.urls import path,include
from principal import views 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include('common.urls')),
    path("princioal/",include('principal.urls')),
    path("siteadmin/",include('siteadmin.urls')),
    path("teacher/",include('teacher.urls')),
    path("student/",include('student.urls')),
]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
