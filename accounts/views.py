from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import MyUser
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm,  PasswordResetForm
from django.utils import timezone
import random
from django.core.mail import send_mail

def home(request):
    if request.method == 'POST':
        # Determine if the user is submitting a login or register form
        if 'username' in request.POST and 'password' in request.POST:
            # Handle login
            identifier = request.POST.get('username')
            password = request.POST.get('password')

            # Check if the input is an email
            if '@' in identifier:
                try:
                    user_obj = MyUser.objects.get(email=identifier)
                    username = user_obj.username
                except MyUser.DoesNotExist:
                    messages.error(request, "This email is not registered. Please sign up first")
                    return render(request, 'accounts/accounts.html', {'form_type': 'login'})
            else:
                try:
                    user_obj = MyUser.objects.get(username=identifier)
                    username = user_obj.username
                except MyUser.DoesNotExist:
                    messages.error(request, "This username does not exist. Please sign up first")
                    return render(request, 'accounts/home.html', {'form_type': 'login'})

            user = authenticate(request, username=username, password=password)
        
            if user is not None:
                login(request, user)
                return redirect('main')
            else:
                messages.error(request, 'Incorrect password. Please try again.')
                return render(request, 'accounts/home.html', {'form_type': 'login'})

        elif 'verification_code' in request.POST:
            # Handle registration
            form = RegisterForm(request.POST)
            if form.is_valid():
                stored_code = request.session.get('verification_code')
                code_sent_at = request.session.get('code_sent_at')

                if stored_code and code_sent_at:
                    elapsed_time = timezone.now().timestamp() - code_sent_at
                    if elapsed_time > 600:
                        form.add_error('verification_code', 'Verification code has expired.')
                    elif stored_code != form.cleaned_data['verification_code']:
                        form.add_error('verification_code', 'Invalid verification code.')
                    else:
                        username = form.cleaned_data['username']
                        email = form.cleaned_data['email']
                        password = form.cleaned_data['password']
                        user = MyUser.objects.create_user(username=username, email=email, password=password)
                        user.save()
                        messages.success(request, 'Registration successful!')
                        return redirect('home')
            else:
                messages.error(request, 'Please correct the errors below.')
            return render(request, 'accounts/accounts.html', {'form': form, 'form_type': 'register'})

    else:
        form = RegisterForm()

    return render(request, 'accounts/home.html', {'form': form, 'form_type': 'login'})

def send_verification_code(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        code = random.randint(1000000, 999999)

        send_mail(
            'Your verification code',
            f'Your verification code is {code}',
            'your-email@example.com',
            [email],
            fail_silently=False,
        )

        request.session['verification_code'] = code
        request.session['code_sent_at'] = timezone.now().timestamp()

        return JsonResponse({'status': 'ok', 'message': 'Verification code sent'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})