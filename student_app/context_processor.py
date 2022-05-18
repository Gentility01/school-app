from student_app.models import *

def class_context(request):
    return{
        'classes' : Classes.objects.all()
    }
    
def term_context(request):
    return{
        'terms': Term.objects.all()
    }
    