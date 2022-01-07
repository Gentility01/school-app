from django.contrib.auth.backends import ModelBackend, UserModel
from django.contrib.auth import get_user_model

# we willcreating authentcation fuction in this class
# now creating UserModel object  and get the moel by calling get_user_model()
class EmailBackEnd(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
# Now in try we will fetch the user from the database and in except i will  handle UserModel DoesNotExist
# and if our execution goes to  except then i will Return  None Else going to check password by calling  method.check_password and passing 
# Password if its True then i will return the user object and in the end am going to retun None
        try:
            user = UserModel.objects.get(email = username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

# Note we will register the  EmailBackend in our settings.py in line(140)

