from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.

def reg(request):
    form = UserCreationForm()
    context = {'form':form}
    return render(request,'reg.html',context)

def register(request):
    form = CustomUserCreationForm()
    
    if request.method == 'POST':
         form = CustomUserCreationForm(request.POST)
         if form.is_valid():
             form.save()
             user = form.cleaned_data.get('username')
             messages.success(request, "Account has been created for " + user)
             return redirect('login')
             

    context = {'form':form}
    return render(request,'register.html',context)
    
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username ,password=password)

        if user is not None:
            login(request,user)
            return redirect('index')
    context={}
    return render(request,'login.html',context)
    #return HttpResponse("this is about page")   

def logoutPage(request):
    logout(request)
    return redirect('login')

def index(request):
    context = {
        'username': request.user.username,  # Pass the logged-in user's username
    }
    return render(request,'index.html',context)
    #return HttpResponse("this is about page") 