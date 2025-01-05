from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate,login,logout
from .models import CustomUser
from django.http import JsonResponse
from .models import UploadedFile




# Create your views here.



def register(request):
    form = CustomUserCreationForm()
    
    if request.method == 'POST':
         form = CustomUserCreationForm(request.POST)
         if form.is_valid():
             form.save()
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

def authors_and_sellers(request):
    # Filter users with public_visibility=True
    public_users = CustomUser.objects.filter(public_visibility=True)
    context = {'public_users': public_users}
    return render(request, 'authors_and_sellers.html', context)

def dashboard(request):
    return render(request, 'dashboard.html')


from django.shortcuts import render, redirect
from .models import UploadedFile

def upload_file(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        visibility = request.POST['visibility']
        cost = request.POST['cost']
        year_of_publication = request.POST['year']
        file = request.FILES['file']

        # Save uploaded file data to the model
        uploaded_file = UploadedFile(
            title=title,
            description=description,
            visibility=visibility,
            cost=cost,
            year_of_publication=year_of_publication,
            file_name=file.name,
            file_path=file,
            file_type=file.content_type
        )
        uploaded_file.save()

        # Redirect to the same view to display updated files
        return redirect('/upload/')

    # Fetch all uploaded files to display
    uploaded_files = UploadedFile.objects.all()
    return render(request, 'dashboard.html', {'uploaded_files': uploaded_files})

