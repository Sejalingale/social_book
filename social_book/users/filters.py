import django_filters
from .models import CustomUser

class CustomUserFilter(django_filters.FilterSet):
    class Meta:
        model = CustomUser
        fields = {
            'username': ['icontains'],  # Filter by username (case-insensitive)
            'email': ['icontains'],     # Filter by email (case-insensitive)
        }
