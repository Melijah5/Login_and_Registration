from django.db import models
import re , bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validation(self, post_data):
        errors ={}
        if not post_data['firstname'] or not post_data['lastname'] or not post_data['password'] or not post_data['email']:
            errors['fieldes_required'] = 'all fields are required'
        if len(post_data ['firstname']) < 2:
            # print('The firstname is less than 2 char!')
            errors['firstname'] = 'First name must be at least 2 char!'
        if len(post_data ['lastname']) < 2:
            # print('The lastname is less than 2 char!')
            errors['lastname'] = 'Last name must be at least 2 char!'
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = 'Invalid Email Format'
        emailcheck =self.filter(email=post_data['email'])
        if emailcheck:
            errors['email'] = 'This Email is aleady in use'
        if len(post_data['password']) < 8:
            errors['password'] = 'Password must be greater than 8 char'
        if post_data['cpassword'] != post_data['password']:
            errors['cpassword'] = 'passwords do not match'
        return errors
    
    
    def login_validator(self, user_data):
        loginErrors = {}
        
        if len(user_data ['email']) < 1:
            # print('The email is less than 1 char!')
            loginErrors['email'] = 'Email Address is required!!'
        getEmail = User.objects.filter(email=user_data['email'])
        print(getEmail)
        if len(getEmail) == 0:
            loginErrors['emailNotexist'] = 'Invalid Email Please register!'
        else:
            user = getEmail[0]
            if not bcrypt.checkpw(user_data['password'].encode(), user.password.encode()):
                loginErrors['password'] = "Incorrect password"
                
        
        return loginErrors
    
class User(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
         return(f"{self.firstname} ")
    
    objects = UserManager()
    