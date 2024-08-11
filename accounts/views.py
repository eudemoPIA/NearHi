from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import MyUser
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.utils import timezone
import random
from django.core.mail import send_mail
from django.shortcuts import render

def home(request):
    return render(request, 'accounts/home.html')

def login_view(request):
    if request.method == 'POST':
        identifier = request.POST.get('username')
        password = request.POST.get('password')

        #check if the input is an email
        if '@' in identifier:
            try:
                user_obj = MyUser.objects.get(email=identifier)
                username = user_obj.username
            except MyUser.DoesNotExist:
                messages.error(request, "This email is not registered. Please sign up first")
                return render(request, 'accounts/login.html')
        else:
            try:
                user_obj = MyUser.objects.get(username=identifier)
                username = user_obj.username
            except MyUser.DoesNotExist:
                messages.error(request, "This username does not exist. Please sign up first")
                return render(request, 'accounts/login.html')

        user = authenticate(request, username=username, password=password)
    
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Incorrect password. Please try again.')

    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'from': form})        

def register_view(request):
    if request.method =='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            stored_code = request.session.get('verification_code')
            code_sent_at = request.session.get('code_sent_at')

            if stored_code and code_sent_at:
                elapsed_time = timezone.now().timestamp() - code_sent_at
                if elapsed_time > 600:
                    form.add_error('verification_code', 'verification code has expired.')
                elif stored_code != form.cleaned_data['verification_code']:
                    form.add_error('verification_code', 'Invalid verification code.')
                else:
                    username = form.cleaned_data['username']
                    email = form.cleaned_data['email']
                    password = form.cleaned_data['password']
                    user = MyUser.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    messages.success(request, 'Registration successful!')
                    return redirect('login')
        else:
            form.add_error('verification_code', 'No verification code found. Please request a new one.')

    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})

def send_verification_code(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        code = random.randint(1000000, 999999)

        send_mail(
            'Your verification code',
            f'Your verification code is {code}',
            'zhang0129pia@gmail.com',
            [email],
            fail_silently=False,
        )

        request.session['verification_code'] = code
        request.session['code_sent_at'] = timezone.now().timestamp()

        return JsonResponse({'status': 'ok', 'message': 'Verification code sent'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

              
# Create your views here.
