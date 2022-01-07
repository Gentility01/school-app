"""School URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from School import settings
from student_app import views, HodView
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('demo/', views.showDemoPage, name='home'),
    path('login/', views.ShowLoginPage),
    path('doLogin', views.doLogin),
    path('logout_user', views.logout_user),
    path('get_user_detail', views.GetUserDetails),
    #this is from HodView.py
    path('admin_home', HodView.admin_home),
    
    path('add_staff', HodView.add_staff ),
    path('add_staff_save', HodView.add_staff_save),
    
    path('add_course', HodView.add_course),
    path('add_course_save', HodView.add_course_save),
    
    path('add_student', HodView.add_student),
    path('add_student_save', HodView.add_student_save),
    
    path('add_subject', HodView.add_subject),
    path('add_subject_save', HodView.add_subject_save),
    
    path('manage_staff', HodView.manage_staff),
    path('manage_student', HodView.manage_student),
    
    path('manage_course', HodView.manage_course),
    path('manage_subject', HodView.manage_subject),
    
    path('edit_staff/<str:staff_id>/', HodView.edit_staff),
    path('edit_staff_save/', HodView.edit_staff_save),
    
    path('edit_student/<str:student_id>/', HodView.edit_student),
    path('edit_student_save', HodView.edit_student_save),
    
    path('edit_subject/<str:subject_id>', HodView.edit_subject),
    path('edit_subject_save', HodView.edit_subject_save),
    
    path('edit_course/<str:course_id>/', HodView.edit_course),
    path('edit_course_save', HodView.edit_course_save),
    


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)


#linking up our static and our media path  from the settings.py

