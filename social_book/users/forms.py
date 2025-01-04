from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser  # Import the custom user model

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email Address")
    public_visibility = forms.BooleanField(
        required=False, 
        label="Make profile public", 
        help_text="Check this box if you want your profile to be visible to others."
    )

    class Meta:
        model = CustomUser 
        fields = ["username", "email", "password1", "password2","public_visibility"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.public_visibility = self.cleaned_data.get("public_visibility", False)
        if commit:
            user.save()
        return user
