from django.shortcuts import redirect
from .models import UploadedFile

def has_uploaded_files(view_func):
    def wrapper_func(request, *args, **kwargs):
        # Check if the logged-in user has uploaded any files
        if UploadedFile.objects.filter(user=request.user).exists():
            # User has uploaded files, allow access
            return view_func(request, *args, **kwargs)
        else:
            # User has not uploaded files, redirect to the index page to upload
            return redirect('index')  # Ensure 'index' is the correct URL name for your index view
    return wrapper_func
