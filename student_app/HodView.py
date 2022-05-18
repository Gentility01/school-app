
from multiprocessing import context
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from datetime import datetime
from django.contrib import messages
from student_app import admin
from .forms import SessionForm
from django.core.files.storage import FileSystemStorage
from student_app.models import Attendance, AttendanceReport, CustomUser, Classes, LeaveReportStaff, LeaveReportStudent, SessionYearModel, Staff, Student, Subject, Term


def admin_home(request):
    count_all_students = Student.objects.all().count()
    count_all_subjects = Subject.objects.all().count()
    count_all_classes = Classes.objects.all().count()
    count_all_staffs = Staff.objects.all().count()
    
    # get total subjects and student in each class
    all_classes = Classes.objects.all()
    class_name_list = []
    subject_count_list = []
    student_count_list_inclass = []
    
    for classes in all_classes:
        subjects = Subject.objects.filter(class_id = classes.id).count() #class_id is from the models.py(forignkey to Classes)
        students = Student.objects.filter(s_class= classes.id).count()
        class_name_list.append(classes.class_name)
        subject_count_list.append(subjects)
        student_count_list_inclass.append(students)
        
    all_subject = Subject.objects.all()
    list_of_subjects = []
    student_count_list_in_subject = []
    
    for subject in all_subject:
        s_classes = Classes.objects.get(id=subject.class_id.id)
        student_count = Student.objects.filter(s_class=s_classes.id).count()
        list_of_subjects.append(subject.subject_name)
        student_count_list_in_subject.append(student_count)
        
    # for staffs
    staff_attendance_present_list=[]
    staff_attendance_leave_list=[]
    staff_name_list=[]
    
    staffs = Staff.objects.all()
    for staff in staffs:
        subject_id =Subject.objects.filter(staff_id=staff.admin.id)
        attendance = Attendance.objects.filter(subject_id__in = subject_id).count()
        leaves = LeaveReportStaff.objects.filter(staff_id=staff.id, leave_status=1).count()
        staff_attendance_present_list.append(attendance)
        staff_attendance_leave_list.append(leaves)
        staff_name_list.append(staff.admin.first_name)
    
    
    # For Students
    student_attendance_present_list=[]
    student_attendance_leave_list=[]
    student_name_list=[]

    students = Student.objects.all()
    for student in students:
        attendance = AttendanceReport.objects.filter(student_id=student.id, status=True).count()
        absent = AttendanceReport.objects.filter(student_id=student.id, status=False).count()
        leaves = LeaveReportStudent.objects.filter(student_id=student.id, leave_status=1).count()
        student_attendance_present_list.append(attendance)
        student_attendance_leave_list.append(leaves+absent)
        student_name_list.append(student.admin.first_name)
        
        context={
        "count_all_students": count_all_students,
        "subject_count": count_all_subjects,
        "course_count": count_all_classes,
        "staff_count": count_all_staffs,
        "class_name_list": class_name_list,
        "subject_count_list": subject_count_list,
        "student_count_list_inclass": student_count_list_inclass,
        "subject_list": list_of_subjects,
        "student_count_list_in_subject": student_count_list_in_subject,
        "staff_attendance_present_list": staff_attendance_present_list,
        "staff_attendance_leave_list": staff_attendance_leave_list,
        "staff_name_list": staff_name_list,
        "student_attendance_present_list": student_attendance_present_list,
        "student_attendance_leave_list": student_attendance_leave_list,
        "student_name_list": student_name_list,
    }
    
    
    return render(request,'hod_template/home_content.html', context )


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



# FOR ADDING Classes
def add_class(request):
    return render(request,'hod_template/add_class_template.html')

def add_class_save(request):
    if request.method != 'POST':
        return HttpResponse( 'Method not allowed ')

    else:
        student_class = request.POST.get('student_class') # these fields are the name of the fields from our (add_class_template) template
        try:
            class_model = Classes(class_name=student_class) #student_class is Classes model from the models.py
            class_model.save()
            messages.success(request, 'Successfully added Class')
            return HttpResponseRedirect('/add_class')
            
        except:
                messages.error(request, 'Failed to add Class')
                return HttpResponseRedirect('/add_class')



# FOR ADING STUDENTS        
def add_student(request):
    student_class = Classes.objects.all()
    return render(request,'hod_template/add_student_template.html', {"student_class":student_class})

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
        class_id = request.POST.get("classes")
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
            class_obj = Classes.objects.get(id=class_id) #creating class object from class model
            user.student.class_id = class_obj # passing the couse object into the user.students.class_id
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
    student_class = Classes.objects.all()
    terms = Term.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    context = {"student_class":student_class,
               "staffs":staffs,
               "terms":terms
               }
   
    return render(request, 'hod_template/add_subject_template.html', context)


def add_subject_save(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Method not allowed</h2>")  
    else:
        subject_name =request.POST.get("subject_name")
        term_id =request.POST.get("term")
        class_term = Term.objects.get(id=term_id)
        class_id =  request.POST.get("classes") # creating class_id variable(class here is from the add_subject_template)
        classes =Classes.objects.get(id=class_id) # creating Classes objects from Classes ID
        staff_id =request.POST.get("staff")  # creating staff_id variable(staff here is from the add_subject_template)
        staff = CustomUser.objects.get(id=staff_id)

        try:
            subject = Subject(
                subject_name=subject_name,  #subject_name is from the Subject in models.py line 61 and  the other subject_name is from the template
                class_id=classes,
                term_id=class_term,
                staff_id=staff
            )
            subject.save()
            messages.success(request, 'Successfully added Subject')
            return HttpResponseRedirect('/add_subject')
            
        except:
             messages.error(request, 'Failed to add subject')
             return HttpResponseRedirect('/add_subject')
         
#for adding terms
def add_term(request):
    term = Term.objects.all()
    context = {'term': term}
    return render(request,'hod_template/add_term_template.html', context)

def add_term_save(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Method not allowed</h2>") 
    else:
        term_slug = request.POST.get("term_slug")
        terms = request.POST.get("term")
        
        try:
            class_term =Term(
                term_slug = term_slug,
                terms = terms
            )
            class_term.save()
            messages.success(request, 'Successfully added Term')
            return HttpResponseRedirect('/add_term')
        
        except:
            messages.error(request, 'Failed to add term')
            return HttpResponseRedirect('/add_term')
#manage term template      
def manage_term(request):
    terms = Term.objects.all()
    context ={'terms':terms}
    return render(request, 'hod_template/manage_team_template.html', context)

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


#manage student by class
def manage_student_byclass(request, id):
    classes = Classes.objects.all()
    class_id = get_object_or_404(Classes, id=id)
    students = Student.objects.filter(s_class=class_id)
    context = {
        'class_id': class_id,
        'students': students,
        'classes':classes
    }
    return render(request,'hod_template/manage_student_byclass.html', context)

#for managing class
def manage_class(request):
    student_class = Classes.objects.all()
    context = {
        'student_class':student_class
    }
    return render(request, 'hod_template/manage_class_template.html', context)


def manage_subject_byclass(request, id):
    subject_class_id = get_object_or_404(Classes, id=id)
    subject = Subject.objects.filter(class_id=subject_class_id)
    context = {
        'subject_id':subject_class_id,
        'subjects':subject
    }
    return render(request, 'hod_template/manage_subject_byclass.html', context)

def manage_subject_byterm(request, id):
    subject_term_id = get_object_or_404(Term, id=id)
    subject = Subject.objects.filter(term_id=subject_term_id)
    classes = Classes.objects.all()
    context = {
        'subject_id':subject_term_id,
        'subjects':subject,
        'classes':classes
    }
    
    return render(request, 'hod_template/manage_subject_byterm.html',context )


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
        'staff':staff,
        'id':staff_id
    }
    return render(request, 'hod_template/edit_staff_template.html', context)


def edit_staff_save(request):
    if request.method != 'POST':
        return HttpResponse('<h2>Method not allowed</h2>')
    else:
        # creating variable for all the  form data(processing the form and update the staff data)
        staff_id = request.POST.get('staff_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name') 
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
    student_class = Classes.objects.all()
    student = Student.objects.get(admin=student_id)
    context = {
        'student':student,
        'student_class':student_class
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
        class_id = request.POST.get("classes")
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
            
            #now accessing the Couerse Object  to set the class in student
            classes = Classes.objects.get(id=class_id)
            student.class_id=classes
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
    student_class = Classes.objects.all()
    terms = Term.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    context  = {
        'subject':subject,
        'student_class':student_class,
        'terms':terms,
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
        class_id = request.POST.get('classes')
        print('two')
        try:
            subject = Subject.objects.get(id=subject_id)
            subject.subject_name = subject_name
            staff = CustomUser.objects.get(id=staff_id)
            subject.staff_id = staff
            classes = Classes.objects.get(id=class_id)
            subject.class_id = classes
            print('three')
            subject.save()
            messages.success(request, 'Successfuly edited Subject')
            return HttpResponseRedirect('/edit_subject/'+subject_id)
        except:
            messages.error(request, 'Failed to edit Suubject')
            return HttpResponseRedirect('/edit_subject/'+subject_id)
        
        
        
        
#Delete Subject
def delete_subject(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    try:
        subject.delete()
        messages.success(request, "Subject Deleted Successfully.")
        return redirect('manage_subject')
    except:
        messages.error(request, "Failed to Delete Subject.")
        return redirect('manage_subject')




def edit_class(request, class_id):
    student_class = Classes.objects.get(id=class_id)
    
    context = {
        'student_class':student_class
    }
    return render(request, 'hod_template/edit_class_template.html', context)

def edit_class_save(request):
    if request.method != 'POST':
        return HttpResponse("<h2>This method is not allowed</h2>")
    
    else:
        class_id = request.POST.get('class_id')
        class_name = request.POST.get('classes')
        
        try:
            s_class = Classes.objects.get(id=class_id)
            s_class.class_name = class_name  #class_name is from the Classes model and the s_class is the form name in the template
            s_class.save()
            messages.success(request, 'Successfuly edited Class')
            return HttpResponseRedirect('/edit_class/'+class_id)
        except:
            messages.error(request, 'Failed to edit Class')
            return HttpResponseRedirect('/edit_class/'+class_id)
        

def add_session(request):
    return render(request, "hod_template/add_session_template.html")


def add_session_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_course')
    else:
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')
        

        try:
            sessionyear = SessionYearModel(session_start_year=session_start_year, session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request, "Session Year added Successfully!")
            return redirect("add_session")
        except:
            messages.error(request, "Failed to Add Session Year add terms first")
            return redirect("add_session")


def manage_session_year(request):
    sessions = SessionYearModel.objects.all()
    context = {'sessions':sessions}
    return render(request, "hod_template/manage_session_template.html", context)

def edit_session(request, session_id):
    get_session = SessionYearModel.objects.get(id=session_id)
    context = {'get_session':get_session}
    return render(request, 'hod_template/edit_session_template.html', context)

def edit_session_save(request):
    if request.method != 'POST':
        return HttpResponse('This method is not allowed')
    
    else:
        session_id = request.POST.get('session_id')
        session_start_year = request.POST.get('start_year')
        session_end_year = request.POST.get('end_year')
        
        try:
            school_sessions = SessionYearModel.objects.get(id=session_id)
            school_sessions.session_start_year = session_start_year
            school_sessions.session_end_year = session_end_year
            school_sessions.save()
            messages.success(request, 'Successfuly edited Session')
            return HttpResponseRedirect('/edit_session/'+session_id)
        except:
            messages.error(request, 'Failed to edit Session')
            return HttpResponseRedirect('/edit_session/'+session_id)

            
            
    


   
