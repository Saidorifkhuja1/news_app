from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Customer

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Customer
        fields = ('username','first_name','last_name','email','age',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Customer
        fields = ('username','first_name','last_name','email','age',)