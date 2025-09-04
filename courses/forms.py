from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["title", "description", "price"]

class SignupForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ("username", "email", "role", "password1", "password2")
