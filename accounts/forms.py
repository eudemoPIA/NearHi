from django import forms
from django.core.exceptions import ValidationError
import re

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True)
    verification_code = forms.CharField(max_length=6, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True, min_length=8)
    password_confirmation = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        #limitations of creating a username
        if not re.match("[A-Za-z0-9_]*$", username):
            raise ValidationError('Username can only contain letters, numbers, and underscores.')
        return username
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        #limitations of setting the password
        if len(password) < 8 or not re.search(r'[0-9]', password) or not re.search(r'[A-Za-z]', password):
            raise ValidationError("Password must contain at least 8 characters, including at least one letter and one number.")
        return password
    
    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleanded_data.get('password_confirmation')
        if password != password_confirmation:
            raise ValidationError("The two passwords didn't match.")
        return password_confirmation                          
    