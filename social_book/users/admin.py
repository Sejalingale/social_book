from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import UploadedFile

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Display these fields in the user list view
    list_display = ['username', 'email', 'is_staff', 'is_active', 'birth_year', 'address', 'public_visibility','age']

    # Add the custom fields to the user edit view
    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'fields': ('birth_year', 'address', 'public_visibility'),
        }),
    )

    # Add the custom fields to the user creation view
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'fields': ('birth_year', 'address', 'public_visibility'),
        }),
    )

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('user','title', 'description', 'visibility', 'cost', 'year_of_publication', 'file_name')
    search_fields = ('title', 'description')
    list_filter = ('visibility', 'year_of_publication')