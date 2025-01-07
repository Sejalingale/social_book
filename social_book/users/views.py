from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate,login,logout
from .models import CustomUser
from django.http import JsonResponse
from .models import UploadedFile
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib import messages
from .serializers import UploadedFileSerializer
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
import random
import string



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

#generate otp function
def generate_otp():
    """Generate a 6-digit OTP"""
    otp = ''.join(random.choices(string.digits, k=6))
    return otp

def send_otp_email(user_email, otp):
    """Send OTP to the user's email address"""
    send_mail(
        'Your OTP for login',
        f'Your OTP for login is: {otp}',
        settings.EMAIL_HOST_USER,  # Make sure this is your email in settings.py
        [user_email],
        fail_silently=False,
    )
    
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)  # Log in the user to start a session
            
            # Generate JWT token
            serializer = TokenObtainPairSerializer(data={"username": username, "password": password})
            if serializer.is_valid():
                tokens = serializer.validated_data
                access_token = tokens['access']
                refresh_token = tokens['refresh']
                
                request.session['access_token'] = access_token
                request.session['refresh_token'] = refresh_token
                
                response = redirect('verify_otp')  # Redirect to OTP verification page after token generation
                response.set_cookie('access_token', access_token)  # Store token in cookies if needed
                response.set_cookie('refresh_token', refresh_token)  # Store refresh token
                
                # Generate OTP and send it to the user's email
                otp = generate_otp()
                send_otp_email(user.email, otp)

                # Store OTP and user ID in session for later OTP verification
                request.session['otp'] = otp
                request.session['user_id'] = user.id

                return response  # Send the user to OTP verification page
            else:
                messages.error(request, 'Token generation failed')
                return redirect('login')  # Redirect back to login if token generation fails

        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')  # Redirect back to login on failed authentication 
    
    return render(request, 'login.html')

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        
        # Get OTP and user ID from session
        stored_otp = request.session.get('otp')
        user_id = request.session.get('user_id')

        if entered_otp == stored_otp:
            # OTP matches, log the user in
            user = CustomUser.objects.get(id=user_id)
            login(request, user)

            # Clear OTP and user id from session
            del request.session['otp']
            del request.session['user_id']

            # Redirect to the dashboard or home page
            return redirect('index')  # or 'index'

        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('verify_otp')  # Redirect back to OTP verification page
    
    return render(request, 'verify_otp.html')


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





def upload_file(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        visibility = request.POST['visibility']
        cost = request.POST['cost']
        year_of_publication = request.POST['year']
        file = request.FILES['file']

        # Save uploaded file data to the model with logged in user
        uploaded_file = UploadedFile(
            user=request.user,
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
    
    # Fetch all uploaded files by logged in user to display
    uploaded_files = UploadedFile.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'uploaded_files': uploaded_files})



class UserUploadedFilesView(APIView):
  permission_classes = [IsAuthenticated]

def get(self, request):
# Fetch files uploaded by the logged-in user
    files = UploadedFile.objects.filter(user=request.user)
    serializer = UploadedFileSerializer(files, many=True)
    return Response(serializer.data)


