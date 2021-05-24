from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.basic_validation(request.POST)
    # print(request.POST)
    if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect('/')    
  
    hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    newuser = User.objects.create(firstname=request.POST['firstname'], lastname=request.POST['lastname'], email=request.POST['email'], password=hash1)
    request.session['loginID']= newuser.id
    return redirect("/homepage")
def homepage(request):
    if 'loginID' not in request.session:
        return redirect('/')
    context = {
        'userlogged': User.objects.get(id = request.session['loginID'])
    }
    return render(request, 'homepage.html', context)

def user_login(request):
    userErrors = User.objects.login_validator(request.POST)
    if len(userErrors) > 0:
        for key,val in userErrors.items():
            messages.error(request,val)
        return redirect('/')
    
    user = User.objects.get(email = request.POST['email'])
    request.session['loginID'] = user.id
    return redirect('/homepage')

def logout(request):
    request.session.clear()
    return redirect("/")