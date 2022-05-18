
from django.urls import path
from School import settings
from student_app import views, HodView
from django.conf.urls.static import static

urlpatterns = [

    path('demo/', views.showDemoPage, name='home'),
    path('login/', views.ShowLoginPage),
    path('doLogin', views.doLogin),
    path('logout_user', views.logout_user),
    path('get_user_detail', views.GetUserDetails),
    # this is from HodView.py
    path('admin_home/', HodView.admin_home, name='admin_home'),

    path('add_staff/', HodView.add_staff, name='add_staff'),
    path('add_staff_save/', HodView.add_staff_save),

    path('add_class/', HodView.add_class, name='add_class'),
    path('add_class_save/', HodView.add_class_save),

    path('add_student/', HodView.add_student, name='add_student'),
    path('add_student_save/', HodView.add_student_save),

    path('add_subject/', HodView.add_subject, name='add_subject'),
    path('add_subject_save/', HodView.add_subject_save),

    path('manage_staff/', HodView.manage_staff, name='manage_staff'),
    path('manage_student/', HodView.manage_student, name='manage_student'),
    path('manage_student_byclass/<int:id>/',
         HodView.manage_student_byclass, name='manage_student_byclass'),
    path('manage_subject_byterm/<int:id>/',
         HodView.manage_subject_byterm, name='manage_subject_byterm'),

    path('manage_class/', HodView.manage_class, name='manage_class'),
    path('manage_subject/', HodView.manage_subject, name='manage_subject'),
    path('manage_subject_byclass/<int:id>/',
         HodView.manage_subject_byclass, name='manage_subject_byclass'),

    path('edit_staff/<staff_id>/', HodView.edit_staff),
    path('edit_staff_save/', HodView.edit_staff_save),

    path('edit_student/<str:student_id>/', HodView.edit_student),
    path('edit_student_save/', HodView.edit_student_save),

    path('edit_subject/<str:subject_id>', HodView.edit_subject, name='edit_subject'),
    path('edit_subject_save/', HodView.edit_subject_save),
    path('delete_subject/<subject_id>/',
         HodView.delete_subject, name="delete_subject"),

    path('edit_class/<str:class_id>/', HodView.edit_class, name='edit_class'),
    path('edit_class_save/', HodView.edit_class_save),

    path('add_term/', HodView.add_term, name='add_term'),
    path('add_term_save/', HodView.add_term_save, name='add_term_save'),
    path('manage_term/', HodView.manage_term, name='manage_term'),

    path('add_session/', HodView.add_session, name='add_session'),
    path('add_session_save/', HodView.add_session_save, name='add_session_save'),
    path('manage_session_year/', HodView.manage_session_year,
         name='manage_session_year'),
    path('edit_session/<str:session_id>/',
         HodView.edit_session, name='edit_session'),
    path('edit_session_save/', HodView.edit_session_save, name='edit_session_save'),



]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# linking up our static and our media path  from the settings.py
