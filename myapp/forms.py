from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import MyUser, Event
import re

class LoginForm(AuthenticationForm):
    username = forms.CharField
    password = forms.CharField(widget=forms.PasswordInput)

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True)
    verification_code = forms.CharField(max_length=6, min_length=6, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True, min_length=8)
    password_confirmation = forms.CharField(widget=forms.PasswordInput, required=True)
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if MyUser.objects.filter(email=email).exists():
            raise ValidationError('Email already registered.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")
        if password and password_confirmation and password != password_confirmation:
            raise ValidationError("The two passwords didn't match.")

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title',
            'description',
            'event_time',
            'location',
            'image',
            'category',
            'fee',
            'max_participants'
        ]

        widgets = {
            'event_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows':4}),
            'category': forms.Select(),
            'fee': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            raise forms.ValidationError('Please upload the image of the event!')
        return image

class ProfileForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['profile_picture', 'city', 'hobbies', 'bio']
        widgets = {
            'bio': forms.Textarea(
                attrs={
                    'placeholder': 'Talk about yourself :)'
                }
            ),
        }


