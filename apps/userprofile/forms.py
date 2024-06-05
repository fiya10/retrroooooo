from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Userprofile





class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, help_text='Required. Enter your first name.')
    last_name = forms.CharField(max_length=50, required=True, help_text='Required. Enter your last name.')
    email = forms.EmailField(max_length=255, required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email


class UserprofileForm(forms.ModelForm):
    class Meta:
        model = Userprofile
        fields = ['phone', 'address', 'zipcode', 'place']
