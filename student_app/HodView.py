
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from datetime import datetime
from django.contrib import messages
from student_app import admin
from django.core.files.storage import FileSystemStorage
from student_app.models import CustomUser, Course, Staff, Student, Subject


def admin_home(request):
    return render(request,'hod_template/home_content.html' )


def add_staff(request):
    return render(request, 'hod_template/add_staff_template.html')


#here this page will proccess the form from the add staff if it is not = post it will show an error message but if it is thrn it will proccess the form
def add_staff_save(request):
    if request.method != 'POST':
        return HttpResponse('method not allowed ')
    
    else:
        first_name = request.POST.get("first_name") # these fields are the name of the fields from our (add_staff_template) template
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")
    # calling the CustomUser from models.py and passing the fields to them 
        try:
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                email=email,
                last_name=last_name,
                first_name=first_name,
                user_type=2
                 ) #passed 2 in user type because it is 2 in our models 
            user.staff.address=address # in the same CustomUser Object "user" i accessed the staff objects and passing the address also
            user.save()
            messages.success(request, 'Successfully added staff')
            return HttpResponseRedirect('/add_staff')
        except:
            messages.error(request, 'Failed to add staff')
            return HttpResponseRedirect('/add_staff')
            

    # note we must put the forms like this both in html and here  to avoid geting errors or not saving form to the data 



# FOR ADDING COURSES
def add_course(request):
    return render(request,'hod_template/add_course_template.html')

def add_course_save(request):
    if request.method != 'POST':
        return HttpResponse( 'Method not allowed ')

    else:
        course = request.POST.get('course') # these fields are the name of the fields from our (add_course_template) template
        try:
            course_model = Course(course_name=course) #course_name is Course model from the models.py
            course_model.save()
            messages.success(request, 'Successfully added course')
            return HttpResponseRedirect('/add_course')
            
        except:
             messages.error(request, 'Failed to add course')
             return HttpResponseRedirect('/add_course')



# FOR ADING STUDENTS        
def add_student(request):
    courses = Course.objects.all()
    return render(request,'hod_template/add_student_template.html', {"courses":courses})

def add_student_save(request):
    if request.method != 'POST':
        return HttpResponse('Method not allowed')
    else:
        first_name = request.POST.get("first_name") # these fields are the name of the fields from our (add_student_template) template
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")
        session_start = request.POST.get("session_start")
        session_end = request.POST.get("session_end")
        course_id = request.POST.get("course")
        gender = request.POST.get("gender")
        

        # now creating a profile pic file objects and read Profile pic File from by request .FILES['INPUT_NAME']
        profile_pic = request.FILES['profile_pic']
        # now creating file system storage
        fs = FileSystemStorage()
        # now saving the file and  storing the  return data in file name  calling method  fs.save((FILE_OBJECT.name,FILE_OBJECT))
        filename=fs.save(profile_pic.name, profile_pic)
        # now reading file path by calling  method fs.url(filename)
        profile_pic_url=fs.url(filename)  #continuation in line  126
        
        
        
        
        
    # calling the CustomUser from models.py and passing the fields to them 
        try:
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                email=email,
                last_name=last_name,
                first_name=first_name,
                user_type=3
                 ) #passed 3 in user type because it is 3 in our models 
            user.student.address=address # in the same CustomUser Object "user" i accessed the staff objects and passing the address also
            course_obj = Course.objects.get(id=course_id) #creating course object from course model
            user.student.course_id = course_obj # passing the couse object into the user.students.course_id
            user.student.session_start = session_start #here student_start comes from models.py(line 85)
            user.student.session_end  = session_end # setting session start and end year 
            user.student.gender = gender #gender is from the models.py and "gender" is from the html form template" same with line109 amd 108
            user.student.profile_pic=profile_pic_url

            user.save()
            messages.success(request, 'Successfully added student')
            return HttpResponseRedirect('/add_student')

        except:
            messages.error(request, 'Failed to add student')
            return HttpResponseRedirect('/add_student')


# For adding subjects
def add_subject(request):
    courses = Course.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
   
    return render(request, 'hod_template/add_subject_template.html', {"courses":courses, "staffs":staffs})


def add_subject_save(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Method not allowed</h2>")  
    else:
        subject_name =request.POST.get("subject_name")
        course_id =  request.POST.get("course") # creating course_id variable(course here is from the add_subject_template)
        course =Course.objects.get(id=course_id) # creating Course objects from Course ID
        staff_id =request.POST.get("staff")  # creating staff_id variable(staff here is from the add_subject_template)
        staff = CustomUser.objects.get(id=staff_id)

        try:
            subject = Subject(
                subject_name=subject_name,  #subject_name is from the Subject in models.py line 61 and  the other subject_name is from the template
                course_id=course,
                staff_id=staff
            )
            subject.save()
            messages.success(request, 'Successfully added Subject')
            return HttpResponseRedirect('/add_subject')
            
        except:
             messages.error(request, 'Failed to add subject')
             return HttpResponseRedirect('/add_subject')


# For manage Staffs
def manage_staff(request):
    #We are reading all the staffs data by calling method staff.objects.all that means we are trying to show it in the website
    staffs = Staff.objects.all()
    context ={
        'staffs':staffs
    }
    return render (request, 'hod_template/manage_staff_template.html', context)

 
# for managing students
def manage_student(request):
    students = Student.objects.all()
    context = {
        'students':students
    }
    return render(request, 'hod_template/manage_student_template.html', context)

#for managing courses
def manage_course(request):
    courses = Course.objects.all()
    context = {
        'courses':courses
    }
    return render(request, 'hod_template/manage_course_template.html', context)


# for managing subjects
def manage_subject(request):
    subjects = Subject.objects.all()
    context = {
        'subjects':subjects
    }
    return render(request, 'hod_template/manage_subject_template.html', context)


# editing  staff
def edit_staff(request, staff_id):
#    Accessing the current staff  object by method Staff.objects.get(admin=Staff_ID)
    staff = Staff.objects.get(admin=staff_id) # here admin is from the models.py line 21
    context = {
        'staff':staff
    }
    return render(request, 'hod_template/edit_staff_template.html', context)


def edit_staff_save(request):
    if request.method != 'POST':
        return HttpResponse('<h2>Method not allowed</h2>')
    else:
        # creating variable for all the  form data(processing the form and update the staff data)
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        staff_id = request.POST.get('staff_id') 
        username = request.POST.get('username')
        address = request.POST.get('address')
        
        # now accessing CustomerUser objects by id  calling method  CustomUser .objects.get(id=staff_id) and setting the values 
        
        try:
            #this fields are from the normal forms in the customuser
            user = CustomUser.objects.get(id=staff_id)
            user.first_name=first_name
            user.last_name=last_name
            user.username=username
            user.email=email
            user.save()
            
            # Now accessing Staff Object to save Address data this comes from aditional data from CustomUser
            # first acces the staff object by method Staff.objects.get(admin=staff_id)
            staff_model = Staff.objects.get(admin=staff_id)
            staff_model.address=address
            staff_model.save()
            
            messages.success(request, 'Successfully edited Staff')
            return HttpResponseRedirect('/edit_staff/'+staff_id)
        except:
            messages.error(request, 'Failed to edit staff')
            return HttpResponseRedirect('/edit_staff/'+staff_id)
         
         
#Editing student
def edit_student(request, student_id):  #the student_id is coming from the urls.py
    courses = Course.objects.all()
    student = Student.objects.get(admin=student_id)
    context = {
        'student':student,
        'courses':courses
    }
    return render(request, 'hod_template/edit_student_template.html', context)



def edit_student_save(request):
    if request.method != 'POST':
        return HttpResponse("<h2>This method is not allowed</h2>")
    
    else:
        #processing the form
        student_id = request.POST.get('student_id')
        first_name = request.POST.get("first_name") # these fields are the name of the fields from our (edit_student_template) template
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        address = request.POST.get("address")
        session_start = request.POST.get("session_start")
        session_end = request.POST.get("session_end")
        course_id = request.POST.get("course")
        gender = request.POST.get("gender")
        
        
        # now creating a profile pic file objects and read Profile pic File from by request .FILES['INPUT_NAME']
        # now adding  a condition for profile pics if file is selected then i will save  new picture else i will not update old picture
        if request.FILES['profile_pic']:
            profile_pic = request.FILES['profile_pic']
            # now creating file system storage
            fs = FileSystemStorage()
            # now saving the file and  storing the  return data in file name  calling method  fs.save((FILE_OBJECT.name,FILE_OBJECT))
            filename=fs.save(profile_pic.name, profile_pic)
            # now reading file path by calling  method fs.url(filename)
            profile_pic_url=fs.url(filename)  #continuation in line  126
        else:
            # in else condition the url = NONE
            profile_pic_url = None
            
            
        
        try:
            #now updating the CustomUserobject by setting Form variable data
            user = CustomUser.objects.get(id=student_id)
            user.first_name=first_name
            user.last_name=last_name
            user.username=username
            user.email=email
            user.save()
            
            #now accessing the Student by  admin by calling  Method Students.objects.get(admin=student_id)
            student = Student.objects.get(admin=student_id)
            student.address =address
            student.session_start =session_start #session_start and others following it are from the Student Model and the ones after the = is from the templates
            student.session_end =session_end
            student.gender = gender
            student.save()
            
            #now accessing the Couerse Object  to set the course in student
            course = Course.objects.get(id=course_id)
            student.courses_id=course
            # sorounding this profile with if profile_pic_url Path is not None 
            if profile_pic_url != None:
                student.profile_pic= profile_pic_url
            
            student.save()
            messages.success(request, 'successfully edited student')
            return HttpResponseRedirect('/edit_student/'+student_id)
        except:
            messages.error(request, 'failed to edit student')
            return HttpResponseRedirect('/edit_student/'+student_id)
            
  
  
  #Edit subject
  
        
# Editing subject
def edit_subject(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    courses = Course.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    context  = {
        'subject':subject,
        'courses':courses,
        'staffs':staffs
    }
    return render(request, 'hod_template/edit_subject_template.html', context)

def edit_subject_save(request):
    if request.method != 'POST':
        return HttpResponse("<h2>This method is not allowed</h2>")
    
    else:
        print('one')
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subject_name')
        staff_id = request.POST.get('staff')
        course_id = request.POST.get('course')
        print('two')
        try:
            subject = Subject.objects.get(id=subject_id)
            subject.subject_name = subject_name
            staff = CustomUser.objects.get(id=staff_id)
            subject.staff_id = staff
            course = Course.objects.get(id=course_id)
            subject.course_id = course
            print('three')
            subject.save()
            messages.success(request, 'Successfuly edited Subject')
            return HttpResponseRedirect('/edit_subject/'+subject_id)
        except:
            messages.error(request, 'Failed to edit Suubject')
            return HttpResponseRedirect('/edit_subject/'+subject_id)



def edit_course(request, course_id):
    course = Course.objects.get(id=course_id)
    
    context = {
        'course':course
    }
    return render(request, 'hod_template/edit_course_template.html', context)

def edit_course_save(request):
    if request.method != 'POST':
        return HttpResponse("<h2>This method is not allowed</h2>")
    
    else:
        course_id = request.POST.get('course_id')
        course = request.POST.get('course')
        
        try:
            courses = Course.objects.get(id=course_id)
            courses.course_name = course  #course_name is from the Course model and the course is the form name in the template
            courses.save()
            messages.success(request, 'Successfuly edited Course')
            return HttpResponseRedirect('/edit_course/'+course_id)
        except:
            messages.error(request, 'Failed to edit Course')
            return HttpResponseRedirect('/edit_course/'+course_id)
        
            
    


   
