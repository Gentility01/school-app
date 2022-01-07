from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from student_app.models import CustomUser, Course, Student, Staff
# Register your models here.


# creating a blank user model  class and registering to the admin 
# if i didnt create blank UserModel,  the password will not be encypted
# note we are removing(normalizing) name email and password from HOD STAFF and STUDENT model field
#  because its storing into  Default Django  User which is CustomUSer


class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Staff)


