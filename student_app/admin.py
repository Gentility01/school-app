from symtable import Class
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from student_app.models import CustomUser, Classes, Student, Staff, Scores, Term, Subject, SessionYearModel
# Register your models here.


# creating a blank user model  class and registering to the admin 
# if i didnt create blank UserModel,  the password will not be encypted
# note we are removing(normalizing) name email and password from HOD STAFF and STUDENT model field
#  because its storing into  Default Django  User which is CustomUSer


class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Classes)
admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(Scores)
admin.site.register(Term)
admin.site.register(Subject)
admin.site.register(SessionYearModel)


