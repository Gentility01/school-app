from django.db import models
from django.db.models import manager
from django.db.models.enums import IntegerChoices
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

# Create your models here.

# OVERRIDING  DEFAULT DJANGO DEFAULT AUTH USER  AND ADDING MORE FILELD TO IT
#now all the admins(HOD, Staff and student) work with django default login  so am going to relate the main auth User Model to other models by admins id
# means that  Students, Staff, hod will relate to admin table by its id

#MAKE SURE TO REGISTER CUSTOMER USER MODELS IN SETTINGS(LINE 138)
class CustomUser(AbstractUser):
    user_type_data = ((1,"HOD"), (2,"Staff"), (3,"Student"))  #setting a tuple for the admins 1 for Admin, 2 for Staffs and 3 for Student 
    user_type = models.CharField(default = 1, choices = user_type_data, max_length=10)
#ADMIN HOD MODEL
class AdminHOD(models.Model):
    id             = models.AutoField(primary_key=True)
    admin          = models.OneToOneField(CustomUser, on_delete=models.CASCADE) # a relationship between HOD and CustomUSer
    # name           = models.CharField( max_length=250)
    # email          = models.CharField( max_length=250)
    # password       = models.CharField( max_length=50)
    created_at     = models.DateTimeField( auto_now_add=True)
    updated_at     = models.DateTimeField( auto_now_add=True)
    objects        = models.Manager() #this field is used to return current object data


#STAFFS MODEL
class Staff(models.Model):
    id             = models.AutoField(primary_key=True)   
    admin          = models.OneToOneField(CustomUser, on_delete=models.CASCADE) # a relationship between Staff and CustomUSer
    # name           = models.CharField( max_length=250) 
    # email          = models.CharField( max_length=250)
    # password       = models.CharField( max_length=50)
    address        = models.TextField()
    created_at     = models.DateTimeField( auto_now_add=True)
    updated_at     = models.DateTimeField( auto_now_add=True)
    objects         = models.Manager() 



# COURSE MODEL
class Course(models.Model):
    id             = models.AutoField(primary_key=True)   
    course_name    = models.CharField( max_length=250) 
    created_at     = models.DateTimeField( auto_now_add=True)
    updated_at     = models.DateTimeField( auto_now_add=True) 
    objects        = models.Manager() 


    def __str__(self):
        return self.course_name



# SUBJECT MODEL
class Subject(models.Model):
    id             = models.AutoField(primary_key=True)   
    subject_name   = models.CharField( max_length=250) 
    course_id      = models.ForeignKey(Course, on_delete=models.CASCADE, default=1)
    staff_id       = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at     = models.DateTimeField( auto_now_add=True)
    updated_at     = models.DateTimeField( auto_now_add=True) 
    objects        = models.Manager() 





# STUDENT MODEL
class Student(models.Model):
    id             = models.AutoField(primary_key=True)
    admin          = models.OneToOneField(CustomUser, on_delete=models.CASCADE) # a relationship between Student and CustomUSer
    # name           = models.CharField( max_length=250)
    # email          = models.CharField( max_length=250)
    # password       = models.CharField( max_length=250)
    gender         = models.CharField( max_length=250)
    profile_pic    = models.FileField()
    address        = models.TextField()
    courses_id     = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    created_at     = models.DateTimeField( auto_now_add=True)
    updated_at     = models.DateTimeField( auto_now_add=True) 
    session_start  = models.DateField()
    session_end    = models.DateField()
    objects        = models.Manager() 

    


# ATTENDABCE MODEL
class Attendance(models.Model):
    id             = models.AutoField(primary_key=True)
    subject_id     = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    attendance_date= models.DateTimeField( auto_now_add=True)
    created_at     = models.DateTimeField( auto_now_add=True)
    objects        = models.Manager() 



#ATTENDANCE REPORT
class AttendanceReport(models.Model):
    id             = models.AutoField(primary_key=True)
    student_id     = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    attendance_id  = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status         = models.BooleanField(default=False)
    created_at     = models.DateTimeField( auto_now_add=True)
    updated_at     = models.DateTimeField( auto_now_add=True)
    objects         = models.Manager() 


# LEAVE MODELS
class LeaveReportStudent(models.Model):
    id             = models.AutoField(primary_key=True) 
    student_id     = models.ForeignKey(Student, on_delete=models.CASCADE)  
    leave_date     = models.CharField(max_length=50)  
    leave_message  = models.TextField()
    created_at     = models.DateTimeField( auto_now_add=True)
    updated_at     = models.DateTimeField( auto_now_add=True)
    objects        = models.Manager() 


class LeaveReportStaff(models.Model):
    id             = models.AutoField(primary_key=True) 
    staff_id       = models.ForeignKey(Staff, on_delete=models.CASCADE)  
    leave_date     = models.CharField(max_length=50)  
    leave_message  = models.TextField()
    created_at     = models.DateTimeField( auto_now_add=True)
    updated_at     = models.DateTimeField( auto_now_add=True)
    objects        = models.Manager() 


# FEEDBACK MODEL
class FeedbackStudent(models.Model):
    id             = models.AutoField(primary_key=True) 
    student_id     = models.ForeignKey(Student, on_delete=models.CASCADE)  
    feedback       = models.TextField()  
    feedback_reply = models.TextField()
    created_at     = models.DateTimeField( auto_now_add=True)
    updated_at     = models.DateTimeField( auto_now_add=True)
    objects        = models.Manager() 


class FeedbackStaff(models.Model):
    id             = models.AutoField(primary_key=True) 
    staff_id       = models.ForeignKey(Staff, on_delete=models.CASCADE)  
    feedback       = models.TextField()  
    feedback_reply = models.TextField()
    created_at     = models.DateTimeField( auto_now_add=True)
    updated_at     = models.DateTimeField( auto_now_add=True)
    objects         = models.Manager() 



# NOTIFICATION mODELS
class NotificationStudent(models.Model):
    id             = models.AutoField(primary_key=True) 
    student_id     = models.ForeignKey(Student, on_delete=models.CASCADE)  
    message        = models.TextField()  
    created_at     = models.DateTimeField( auto_now_add=True)
    updated_at     = models.DateTimeField( auto_now_add=True)
    objects        = models.Manager() 




class NotificationStaff(models.Model):
    id             = models.AutoField(primary_key=True) 
    staff_id       = models.ForeignKey(Staff, on_delete=models.CASCADE)  
    message        = models.TextField()  
    created_at     = models.DateTimeField( auto_now_add=True)
    updated_at     = models.DateTimeField( auto_now_add=True)
    objects        = models.Manager() 



# creating signals... when new User is created i will add new row in HOD, STAFF, STUDENT with its id  in admin =_id column 
# @recieveer(post_save, sender=CustomUser) will run only when data  added in CustomUser

#this function adds data into HOD, Stff and Student table . Taking parameters sender, instance, created, here sender is class which calls this method
# instance is Current Inserted  DAta Model created is True/FAlse, True when data is inserted 
# if created is True means if data is inserted , then i will insert data  into other tables if user_type=1 then i will add row in HOD table with AdminID
#Now  calling the   AdminHod.objects.create and passing the admin=instance. here instance is the  CustomerUser

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type==1:
            AdminHOD.objects.create(admin=instance)

        if instance.user_type==2:
            Staff.objects.create(admin=instance)  #now calling the staff.objects.create and  passing the admin=instance. here instance is the  CustomerUser
        

        if instance.user_type==3:
            Student.objects.create(admin=instance, courses_id=Course.objects.get(id=1), session_start="2021-11-9", session_end="2022-1-1", address="", profile_pic="", gender="")  
            #now calling the student.objects.create and  passing the admin=instance. here instance is the  CustomerUser
            # now at courses_id(line 82) and also in Subject(line 62) we added default=1 to it(that means we are setting the default) then we set te default for course, start_session and end_session, address, profile_pic e.t.c in line 196
        

# now @ reciever(post_save, sender=CustomUser)
# def save_user_profile() this method will call after  create_userprofile()Execution4
# now using the same condition  user_type1,2,3 for saving the method  of  AdminHOD, Staff snd student
# if user type=1 then i will call instance.adminhod.save() to save  AdminModel


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()  #user type=1 then i will call instance.adminhod.save() to save  AdminModel

    if instance.user_type == 2:
        instance.staff.save()  #user type=2 then i will call instance.staff.save() to save  Staff nModel

    if instance.user_type == 3:
        instance.student.save()  #user type=3 then i will call instance.student.save() to save  Student Model


# so all  this reciever work  when  we add  new data  in CustomUser table after inserting data i will insert the current ID of   CustomerUser
# into Other TAble such as AdminHod, Staff, Student 



    



    











